import asyncio
import base64
import os
import random
import tempfile
from difflib import SequenceMatcher
from typing import Union
from urllib.parse import quote

import httpx

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from bs4 import BeautifulSoup


pygame.mixer.init()

client = httpx.AsyncClient(follow_redirects=True)
client.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"

preffered_language = input("Preffered language (English, German, ...): ").lower()
print("Don't use punctuation like commas, dots or question marks.")


async def search(term: str) -> bytes:
    # Search for the term
    print(f"Searching for {repr(term)}...")
    r = await client.get(f"https://de.forvo.com/searchs-ajax-load.php?term={quote(term)}")
    r.raise_for_status()
    j = r.json()
    assert isinstance(j, list)
    assert len(j) > 0

    # Find the best match
    best_entry: Union[None, str] = None
    best_similarity = 0
    for word in j:
        similarity = SequenceMatcher(None, word, term).ratio()
        if similarity > best_similarity:
            best_similarity = similarity
            best_entry = word
    print(f"Best match: {repr(best_entry)}")
    assert best_entry is not None

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
        a, b, c, d, e, f, g, h, i = args
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
    print(f"Playing {repr(best_entry)} ({repr(audio_url)})...")
    r = await client.get(audio_url)
    r.raise_for_status()
    return r.content


async def play(term: str) -> None:
    with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
        f.write(await search(term))
        f.flush()
        pygame.mixer.music.load(f.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)


async def main() -> None:
    while True:
        for term in input("> ").split(" "):
            await play(term)


asyncio.run(main())
