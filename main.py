import subprocess
import fire
import re
import logging
import requests

from pathlib import Path
from time import sleep

# windows that use ctrl+shift+c/v instead of ctrl+c/v to copy/paste
CTRL_SHIFT_REGEX = [
    r'.+ Visual Studio Code \[Terminal\]$',  # vscode terminal
    '^yu@yu-ubuntu: .+',  # gnome-terminal
]

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(message)s",
                    handlers=[
                        logging.FileHandler(Path(__file__).parent / 'log.txt',
                                            mode='w'),
                        logging.StreamHandler()
                    ])


def run_get_output(command):
    return subprocess.run(command, shell=True, capture_output=True,
                          text=True).stdout.strip()


def run_get_binary_output(command):
    return subprocess.run(command, shell=True, capture_output=True).stdout


def run_silent(command):
    subprocess.run(command,
                   shell=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


def run_verbose(command):
    return subprocess.run(command,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          text=True).stdout.strip()


def get_clipboard():
    targets = run_get_output('xclip -selection clipboard -target TARGETS -out')
    targets = targets.split('\n')

    if 'image/png' in targets:
        image = run_get_binary_output(
            'xclip -selection clipboard -target image/png -out')
        return 'image', image
    elif 'text/plain' in targets:
        text = run_get_output(
            'xclip -selection clipboard -target text/plain -out')
        return 'text', text
    else:
        return None, None


def copy(host, prefix, username, password):
    logging.info('Copy')
    window_name = run_get_output('xdotool getactivewindow getwindowname')
    logging.info(f'Current active window name: {window_name}')
    if any([re.match(pattern, window_name) for pattern in CTRL_SHIFT_REGEX]):
        logging.info('Copy with Ctrl+Shift+C')
        run_silent('xdotool key ctrl+shift+c')
    else:
        logging.info('Copy with Ctrl+C')
        run_silent('xdotool key ctrl+c')
    sleep(0.4)

    type, data = get_clipboard()
    if type is None:
        logging.info('Clipboard empty')
        return

    logging.info(
        f"Clipboard data:\n\ttype: {type}\n\tlength: {len(data)}\n\tpreview: {repr(data[:64])}..."
    )

    session = requests.Session()
    session.auth = (username, password)
    if type == 'image':
        session.put(f"{host}SET/{prefix}:clipboard:image", data=data)
        session.get(f"{host}DEL/{prefix}:clipboard:text")
    elif type == 'text':
        session.put(f"{host}SET/{prefix}:clipboard:text",
                    data=data.encode('utf-8'))
        session.get(f"{host}DEL/{prefix}:clipboard:image")

    logging.info('Upload successfully')


def paste(host, prefix, username, password):
    logging.info('Paste')
    session = requests.Session()
    session.auth = (username, password)

    text = session.get(
        f"{host}GET/{prefix}:clipboard:text.txt").content.decode('utf-8')
    image = session.get(f"{host}GET/{prefix}:clipboard:image.png").content
    if text and not image:
        subprocess.run('xclip -selection clipboard -target text/plain -in',
                       shell=True,
                       input=text,
                       text=True)
        logging.info('Write text to clipboard')
    elif not text and image:
        subprocess.run('xclip -selection clipboard -target image/png -in',
                       shell=True,
                       input=image)
        logging.info('Write image to clipboard')
    else:
        logging.info(
            f'Error data from cloud:\ntext: {repr(text[:64])}...\nimage: {repr(image[:64])}...'
        )
        return

    sleep(0.4)
    window_name = run_get_output('xdotool getactivewindow getwindowname')
    logging.info(f'Current active window name: {window_name}')
    if any([re.match(pattern, window_name) for pattern in CTRL_SHIFT_REGEX]):
        logging.info('Paste with Ctrl+Shift+V')
        run_silent('xdotool key ctrl+shift+v')
    else:
        logging.info('Paste with Ctrl+V')
        run_silent('xdotool key ctrl+v')


if __name__ == '__main__':
    fire.Fire({
        'copy': copy,
        'paste': paste,
    })
