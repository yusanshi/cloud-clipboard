import subprocess
import fire
import logging
import requests
import tkinter as tk
import win32clipboard

from pathlib import Path
from time import sleep
from pyautogui import hotkey
import PIL
import io

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(message)s",
                    handlers=[
                        logging.FileHandler(Path(__file__).parent / 'log.txt',
                                            mode='w'),
                        logging.StreamHandler()
                    ])


def get_clipboard():
    image = PIL.ImageGrab.grabclipboard()
    if isinstance(image, PIL.Image.Image):
        byte_array = io.BytesIO()
        # TODO: how to distinguish between PNG and JPG images and use different format respectively
        image.save(byte_array, format='PNG')
        image = byte_array.getvalue()
        return 'image-png', image

    try:
        root = tk.Tk()
        root.withdraw()
        text = root.clipboard_get()
        root.update()
        root.destroy()
        return 'text', text
    except Exception:
        pass

    return None, None


def copy(host, prefix, username=None, password=None):
    logging.info('Copy')
    hotkey('ctrl', 'c')
    sleep(0.2)

    type, data = get_clipboard()
    if type is None:
        logging.info('Clipboard empty')
        return

    logging.info(
        f"Clipboard data:\n\ttype: {type}\n\tlength: {len(data)}\n\tpreview: {repr(data[:64])}..."
    )

    session = requests.Session()
    if username is not None:
        session.auth = (username, password)
    if type == 'text':
        data = data.encode('utf-8')
    session.put(
        f"{host}MSET/{prefix}:clipboard:type/{type}/{prefix}:clipboard:data",
        data=data)
    session.get(f"{host}PUBLISH/{prefix}/clipboard-change")

    logging.info('Upload successfully')


def paste(host, prefix, username=None, password=None):
    logging.info('Paste')
    session = requests.Session()
    if username is not None:
        session.auth = (username, password)

    data = session.get(
        f"{host}MGET/{prefix}:clipboard:type/{prefix}:clipboard:data.raw"
    ).content
    if data == b'*2\r\n':
        logging.info('Clipboard empty')
        return

    first = data.find(b'\r\n')
    second = data.find(b'\r\n', first + 1)
    third = data.find(b'\r\n', second + 1)
    fourth = data.find(b'\r\n', third + 1)
    type = data[second + 2:third].decode('utf-8')
    data = data[fourth + 2:-2]

    if type == 'image-png' or type == 'image-jpg':
        image = PIL.Image.open(io.BytesIO(data)).convert('RGBA')
        # https://stackoverflow.com/questions/35859140/remove-transparency-alpha-from-any-image-using-pil
        background = PIL.Image.new('RGBA', image.size, (255, 255, 255))
        image = PIL.Image.alpha_composite(background, image).convert('RGB')
        byte_array = io.BytesIO()
        image.save(byte_array, format='DIB')
        image = byte_array.getvalue()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, image)
        win32clipboard.CloseClipboard()
        logging.info('Write image to clipboard')
    elif type == 'text':
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(data.decode('utf-8'),
                                        win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        logging.info('Write text to clipboard')
    else:
        logging.info(f'Unknown type {type}')
        return

    sleep(0.2)
    hotkey('ctrl', 'v')


if __name__ == '__main__':
    fire.Fire({
        'copy': copy,
        'paste': paste,
    })
