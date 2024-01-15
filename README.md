# Forvo TTS

Text-to-speech with voice samples from [Forvo](https://forvo.com/).

Its a fun project!

## Showcase

See [here](./showcase.mp4) (enable sound).

## Installation

```bash
apt update
apt install -y python3 python3-pip

python3 -m pip install -Ur requirements.txt

python3 main.py  # Run the program
```

## Created with

[https://static00.forvo.com/_presentation/assets/js/scripts.js?v=400](https://static00.forvo.com/_presentation/assets/js/scripts.js?v=400)

```js
function Play(a, b, c, d, e, f, g, h, i) {
    if (_SERVER_HOST == _AUDIO_HTTP_HOST) {
        var b = defaultProtocol + "//" + _SERVER_HOST + "/player-mp3Handler.php?path=" + b,
            c = defaultProtocol + "//" + _SERVER_HOST + "/player-oggHandler.php?path=" + c;
        if ("undefined" != typeof e && void 0 !== e && null !== e && "" !== e) var e = defaultProtocol + "//" + _SERVER_HOST + "/player-mp3-highHandler.php?path=" + e;
        else var e = "";
        if ("undefined" != typeof f && void 0 !== f && null !== f && "" !== f) var f = defaultProtocol + "//" + _SERVER_HOST + "/player-ogg-highHandler.php?path=" + f;
        else var f = ""
    } else {
        var b = defaultProtocol + "//" + _AUDIO_HTTP_HOST + "/mp3/" + base64_decode(b),
            c = defaultProtocol + "//" + _AUDIO_HTTP_HOST + "/ogg/" + base64_decode(c);
        if ("undefined" != typeof e && void 0 !== e && null !== e && "" !== e) var e = defaultProtocol + "//" + _AUDIO_HTTP_HOST + "/audios/mp3/" + base64_decode(e);
        else var e = "";
        if ("undefined" != typeof f && void 0 !== f && null !== f && "" !== f) var f = defaultProtocol + "//" + _AUDIO_HTTP_HOST + "/audios/ogg/" + base64_decode(f);
        else var f = ""
    }
    if ("undefined" == typeof g || void 0 == g || null == g || "" == g) var g = "l";
    var j = !!document.createElement("audio").canPlayType;
    if (d = d ? !0 : !1, j) {
        var k = navigator.userAgent.toLowerCase(),
            l = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(k);
        createAudioObject(a, b, c, l, d, e, f, g)
    } else {
        var m = '<object type="application/x-shockwave-flash" data="' + player_path + '" width="1" height="1"><param name="movie" value="' + player_path + '" /><param name="flashvars" value="path=' + b + "&amp;_SERVER_HTTP_HOST=" + _SERVER_HOST + '" /></object>',
            n = document.getElementById("player");
        n.innerHTML = m
    }
    return isNaN(a) && -1 != a.indexOf("_map") && (a = a.split("_", 1)), sumHit(a), sendInfoGoogleDataLayer("play", {
        word: h,
        lang: i
    }), showAcademyChallengePopup && $.ajax({
        type: "POST",
        dataType: "json",
        url: "/xmas-promo-mfp/",
        data: {
            "function": "checkAcademyChallengePopupStatus",
            id: a
        },
        success: function(a) {
            if (1 == a.error && console.warn(a.errorMsg), 1 == a.showAcademyChallengePopup) {
                showAcademyChallengePopup = 0;
                var b = "mfp_academy-xmas-promo-popup",
                    c = "xmas";
                sendInfoGoogleDataLayer("view_popup", {
                    type: c,
                    word: h,
                    language: i
                }), !isLoggedUser && showLoginSignupPopup && (secondsToRenderLoginSignupPopup += 60), isLoggedUser && showUserInterestPopup && (secondsToRenderUserInterestPopup += 60), $.magnificPopup.open({
                    items: {
                        src: "foo.jpg"
                    },
                    type: "ajax",
                    ajax: {
                        settings: {
                            url: "/xmas-promo-mfp.php"
                        }
                    },
                    mainClass: b,
                    closeOnBgClick: !1,
                    showCloseBtn: !0,
                    modal: !1
                }, 0)
            }
        }
    }), !0
}
```
