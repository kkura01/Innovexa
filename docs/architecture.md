# How Innovexa is put together

Innovexa is a single window loop. It does not use a web server, a database, or a framework beyond Pygame for drawing and the speech libraries for listening and talking.

## What happens when you press C

```
idle screen
    |
    |  key C
    v
listening screen
    |
    |  microphone -> Google recognizer -> lowercase text
    v
catalog substring match
    |
    +-- no match ---------> console message, back to idle
    |
    +-- image is None ----> speak goodbye, quit
    |
    +-- image is set -----> draw portrait, speak the fact, back to idle
```

`innovexa/app.py` owns that loop.

- `idle.png` is the resting screen (`assets/images/ui/idle.png`).
- `listening.png` is shown while the microphone is open, and it stays up behind the portrait.
- The portrait is scaled into a fixed rectangle, 813 by 375 pixels, placed at (45, 145). Those numbers match the frame drawn into the listening background.
- Closing the window sets the loop flag and calls `pygame.quit()`.

Speech recognition uses `speech_recognition` with the default Google web API, so a failed network call is reported as `RequestError` and the app returns to the idle screen. Playback uses `pyttsx3`, which talks to the operating system's speech engine (SAPI on Windows). The rate is 150 words per minute.

## Catalog

`innovexa/catalog.py` is the only place that knows invention names. Each record has:

| Field | Role |
| --- | --- |
| `keyword` | Lowercase phrase searched for inside the transcript |
| `speech` | Exact sentence passed to the speech engine |
| `image` | File name under `assets/images/inventors/`, or `None` to quit |

`find_entry()` walks the list from top to bottom and returns the first keyword that occurs anywhere in the transcript. "Who invented the steam engine" matches `steam engine`. "I want to exit now" matches `exit`.

Image files are not loaded until a keyword hits, and the path is built from the repository root next to the `innovexa` package:

```
<project root>/assets/images/inventors/<image>
```

## Original files

The slide deck and the early keyword write-up are kept under `docs/` for reference:

- `docs/Innovexa-presentation.pptx`
- `docs/keywords.docx`

The running app reads `innovexa/catalog.py`, not the Word document. If those two ever disagree, the Python catalog is the one that plays.
