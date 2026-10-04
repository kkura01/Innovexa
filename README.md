# Innovexa

Innovexa is a small desktop app that listens for the name of an invention, shows a portrait of the person credited with it, and reads a short history aloud.

Press **C**, say something like "tell me about the telescope", and the window switches to Hans Lippershey while the speaker reads the entry. Say **exit** or **close** to leave.

The spoken facts are the original project text. They are short classroom summaries, not a full history of each invention.

## Requirements

- Python 3.9 or newer
- A microphone
- An internet connection (speech is transcribed by Google's web recognizer)
- Speakers, so the spoken replies are audible

## Setup

From the project root:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS or Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

`PyAudio` is what gives Python access to the microphone. On Windows, if that install fails, install a matching wheel from [PyAudio wheels for Windows](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and then rerun `pip install -r requirements.txt`.

## Run

From the project root, with the virtual environment active:

```bash
python -m innovexa
```

1. Wait until the console prints `Innovexa is ready`.
2. Click the window so it has keyboard focus.
3. Press **C**. The screen changes to the listening background.
4. Say an invention name from the table below, in a short sentence if you like.
5. The portrait appears and the fact is read aloud. The idle screen returns when the speech finishes.
6. Press **C** again for another invention, or say **exit** / **close**.

Closing the window also quits. If the recognizer cannot hear a phrase, or the phrase does not contain a known keyword, the app prints a line in the console and returns to the idle screen.

## Voice commands

Matching is a substring check on the lowercased transcript. The first keyword in this list that appears in the phrase is the one that plays.

| Say | Portrait | Subject |
| --- | --- | --- |
| bulb | Thomas Edison | Light bulb |
| printing press | Johannes Gutenberg | Printing press |
| steam engine | Thomas Savery | Steam engine |
| telescope | Hans Lippershey | Telescope |
| vaccine | Edward Jenner | Smallpox vaccine |
| antibiotic | Alexander Fleming | Antibiotics |
| computer | Charles Babbage | Analytical Engine |
| bell | Alexander Graham Bell | Telephone |
| refrigerator | William Cullen | Refrigeration |
| atomic bomb | J. Robert Oppenheimer | Trinity test |
| mirror | Justus von Liebig | Silvered-glass mirror |
| typewriter | Christopher Latham Sholes | Typewriter |
| match | John Walker | Friction match |
| duct tape | Vesta Stoudt | Duct tape |
| velcro | George de Mestral | Hook and loop |
| x-ray | Wilhelm Roentgen | X-rays |
| periodic table | Dmitri Mendeleev | Periodic table |
| measuring tape | Alvin J. Fellows | Spring tape measure |
| pasteurization | Louis Pasteur | Pasteurization |
| radio | Guglielmo Marconi | Wireless telegraph |
| eraser | Edward Nairne | Rubber eraser |
| atm | John Shepherd-Barron | Cash machine |
| exit, close | — | Speaks a goodbye and quits |

## Project layout

```
Innovexa/
├── README.md
├── requirements.txt
├── innovexa/                 # application package
│   ├── __main__.py           # python -m innovexa
│   ├── app.py                # window, microphone, speech
│   └── catalog.py            # keywords, spoken text, image names
├── assets/
│   └── images/
│       ├── ui/               # idle and listening backgrounds
│       └── inventors/        # portraits shown with each entry
└── docs/
    ├── architecture.md
    ├── Innovexa-presentation.pptx
    └── keywords.docx         # original keyword notes
```

Paths to images are resolved from the package location, so the app does not depend on the shell's current directory beyond being able to import `innovexa`.

## Add an invention

1. Put the portrait in `assets/images/inventors/`. JPG and JPEG both work; use the real filename.
2. Add an entry near the top of `CATALOG` in `innovexa/catalog.py`:

```python
{
    "keyword": "compass",
    "speech": "The sentence that should be read aloud.",
    "image": "portrait.jpg",
},
```

3. To add another way to quit, copy the `exit` entry and set `"image": None`.

Put longer, more specific keywords before shorter ones. `printing press` is safe because nothing else contains that phrase, but a keyword like `press` would also match "printing press" if it were listed first.

See [docs/architecture.md](docs/architecture.md) for how the window loop and the catalog fit together.
