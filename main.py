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
        return 'image-png', image
    elif 'image/jpeg' in targets:
        image = run_get_binary_output(
            'xclip -selection clipboard -target image/jpeg -out')
        return 'image-jpg', image
    elif 'text/plain' in targets:
        text = run_get_output(
            'xclip -selection clipboard -target text/plain -out')
        return 'text', text
    else:
        return None, None


def copy(host, prefix, username=None, password=None):
    logging.info('Copy')
    window_name = run_get_output('xdotool getactivewindow getwindowname')
    logging.info(f'Current active window name: {window_name}')
    sleep(0.4)
    if any([re.match(pattern, window_name) for pattern in CTRL_SHIFT_REGEX]):
        logging.info('Copy with Ctrl+Shift+C')
        run_silent('xdotool key ctrl+shift+c')
    else:
        logging.info('Copy with Ctrl+C')
        run_silent('xdotool key ctrl+c')
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

    if type == 'image-png':
        subprocess.run('xclip -selection clipboard -target image/png -in',
                       shell=True,
                       input=data)
        logging.info('Write PNG image to clipboard')
    elif type == 'image-jpg':
        subprocess.run('xclip -selection clipboard -target image/jpeg -in',
                       shell=True,
                       input=data)
        logging.info('Write JPG image to clipboard')
    elif type == 'text':
        subprocess.run('xclip -selection clipboard -target text/plain -in',
                       shell=True,
                       input=data.decode('utf-8'),
                       text=True)
        logging.info('Write text to clipboard')
    else:
        logging.info(f'Unknown type {type}')
        return

    sleep(0.3)
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
