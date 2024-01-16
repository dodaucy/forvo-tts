import asyncio
import base64
import os
import random
import tempfile
from difflib import SequenceMatcher
from typing import List, Union
from urllib.parse import quote

import colorama
import httpx

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from bs4 import BeautifulSoup


# How many audio files should be buffered before pausing the download?
BUFFER_SIZE = 2

colorama.init(autoreset=True)
pygame.mixer.init()

client = httpx.AsyncClient(follow_redirects=True)
client.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"

preffered_language = input("Preffered language (English, German, ...): ").lower()
print("Don't use punctuation like commas, dots or question marks.")


class AudioNotFound(Exception):
    pass


class Task:
    def __init__(self, sentence: str) -> None:
        self.download_finished = False
        self.playing_finished = False
        self.terms = sentence.split(" ")
        self.audio_files_to_play: List[str] = []
        self.audio_files: List[str] = []

    async def play_audio(self) -> None:
        while not self.download_finished or len(self.audio_files_to_play) > 0:
            if len(self.audio_files_to_play) > 0:
                f = self.audio_files_to_play.pop(0)
                print(f"{colorama.Fore.BLUE}Playing {repr(f)}...")
                pygame.mixer.music.load(f)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)
            else:
                await asyncio.sleep(0.1)
        self.playing_finished = True
        print(f"{colorama.Fore.YELLOW}Finished playing audio files.")

    async def run(self) -> None:
        # Download all files
        for term in self.terms:
            try:
                audio_file = await self.request(term)
                self.audio_files_to_play.append(audio_file)
                self.audio_files.append(audio_file)
                if len(self.audio_files_to_play) > BUFFER_SIZE:
                    print(f"{colorama.Fore.GREEN}Waiting for audio files to be played...")
                    await asyncio.sleep(1)
            except AudioNotFound:
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}Audio for {repr(term)} not found. Skipping...")
        self.download_finished = True
        print(f"{colorama.Fore.YELLOW}Finished downloading audio files.")

        # TODO: Optional: Merge all files into one using ffmpeg

        # Delete all files
        while not self.playing_finished:
            await asyncio.sleep(0.1)
        for f in self.audio_files:
            os.remove(f)
        print(f"{colorama.Fore.YELLOW}Finished deleting audio files.")

    async def request(self, term: str) -> str:
        # Search for the term
        print(f"{colorama.Fore.GREEN}Searching for {repr(term)}...")
        r = await client.get(f"https://de.forvo.com/searchs-ajax-load.php?term={quote(term)}")
        r.raise_for_status()
        j = r.json()
        assert isinstance(j, list)
        if len(j) == 0:
            raise AudioNotFound

        # Find the best match
        best_entry: Union[None, str] = None
        best_similarity = -1
        for word in j:
            similarity = SequenceMatcher(None, word, term).ratio()
            if similarity > best_similarity:
                best_similarity = similarity
                best_entry = word
        print(f"{colorama.Fore.GREEN}Best match: {repr(best_entry)}")

        # Get audio urls
        r = await client.get(f"https://de.forvo.com/word/{quote(best_entry)}")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        preffered_audio_urls = []
        bad_audio_urls = []
        for div in soup.find_all("div", {"class": "play"}):
            args_str = div["onclick"].split("(")[1].split(")")[0]
            args = [arg.strip("'") for arg in args_str.split(",")]
            if len(args) != 9:
                continue
            a, b, c, d, e, f, g, h, i = args  # Names from JS
            if h == best_entry:
                if e:
                    audio_url = f"https://audio12.forvo.com/audios/mp3/{base64.b64decode(e).decode()}"
                else:
                    audio_url = f"https://audio12.forvo.com/mp3/{base64.b64decode(b).decode()}"
                if i.lower() == preffered_language:
                    preffered_audio_urls.append(audio_url)
                else:
                    bad_audio_urls.append(audio_url)
        if len(preffered_audio_urls) > 0:
            audio_urls = preffered_audio_urls
        else:
            audio_urls = bad_audio_urls
        assert len(audio_urls) > 0

        # Download audio
        audio_url = random.choice(audio_urls)
        print(f"{colorama.Fore.GREEN}Downloading {repr(audio_url)}...")
        r = await client.get(audio_url)
        r.raise_for_status()

        # Save audio as file
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".mp3", delete=False) as f:
            f.write(r.content)
            f.flush()
            return f.name


async def main() -> None:
    while True:
        task = Task(input("> "))
        await asyncio.gather(
            task.run(),
            task.play_audio()
        )


asyncio.run(main())
