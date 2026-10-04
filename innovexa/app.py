"""Pygame window, microphone capture, and spoken replies."""

from pathlib import Path

import pygame
import pyttsx3
import speech_recognition as speech

from innovexa.catalog import find_entry

ROOT = Path(__file__).resolve().parent.parent
UI_DIR = ROOT / "assets" / "images" / "ui"
INVENTOR_DIR = ROOT / "assets" / "images" / "inventors"

WINDOW_SIZE = (900, 600)
PORTRAIT_BOX = pygame.Rect(45, 145, 813, 375)
SPEECH_RATE = 150


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Innovexa")

    engine = pyttsx3.init()
    engine.setProperty("rate", SPEECH_RATE)

    idle = _load_background("idle.png")
    listening = _load_background("listening.png")
    _show(screen, idle)

    print("Innovexa is ready. Press C to speak, or close the window to quit.")

    running = True
    while running:
        listening_requested = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                listening_requested = True

        if not running or not listening_requested:
            continue

        _show(screen, listening)
        command = _recognize_command()
        if command is None:
            _show(screen, idle)
            continue

        print("You said: " + command)
        entry = find_entry(command)
        if entry is None:
            print("No matching invention. Try another keyword, or say exit.")
            _show(screen, idle)
            continue

        if entry["image"] is None:
            _speak(engine, entry["speech"])
            running = False
            continue

        _show_inventor(screen, listening, entry["image"])
        print(entry["speech"])
        _speak(engine, entry["speech"])
        _show(screen, idle)

    pygame.quit()


def _load_background(filename):
    image = pygame.image.load(str(UI_DIR / filename)).convert_alpha()
    return pygame.transform.scale(image, WINDOW_SIZE)


def _show(screen, image):
    screen.blit(image, (0, 0))
    pygame.display.update()


def _show_inventor(screen, background, filename):
    portrait = pygame.image.load(str(INVENTOR_DIR / filename)).convert_alpha()
    portrait = pygame.transform.scale(portrait, PORTRAIT_BOX.size)
    screen.blit(background, (0, 0))
    screen.blit(portrait, PORTRAIT_BOX.topleft)
    pygame.display.update()


def _recognize_command():
    recognizer = speech.Recognizer()
    try:
        with speech.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Speak:")
            audio = recognizer.listen(source)
        return recognizer.recognize_google(audio).lower()
    except speech.UnknownValueError:
        print("Could not understand audio")
    except speech.RequestError as error:
        print("Could not request results; {0}".format(error))
    except OSError as error:
        print("Microphone error: {0}".format(error))
    return None


def _speak(engine, text):
    engine.say(text)
    engine.runAndWait()
