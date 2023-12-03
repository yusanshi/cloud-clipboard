import subprocess
import fire
import re
import logging
import pyautogui

from pathlib import Path
from time import sleep

CTRL_SHIFT_C_REGEX = [
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
        return None


def copy():
    logging.info('Copy')
    window_name = run_get_output('xdotool getactivewindow getwindowname')
    logging.info(f'Current active window name: {window_name}')
    if any([re.match(pattern, window_name) for pattern in CTRL_SHIFT_C_REGEX]):
        logging.info('Copy with Ctrl+Shift+C')
        # pyautogui.hotkey('ctrl', 'shift', 'c')
        run_silent('xdotool key ctrl+shift+c')
    else:
        logging.info('Copy with Ctrl+C')
        # pyautogui.hotkey('ctrl', 'c')
        run_silent('xdotool key ctrl+c')
    sleep(0.2)

    data = get_clipboard()
    if data is None:
        logging.info('Clipboard empty')
    else:
        logging.info(
            f"Clipboard data:\n\ttype: {data[0]}\n\tlength: {len(data[1])}\n\tpreview: {repr(data[1][:64])}{'...' if len(data[1])>64 else ''}"
        )


def paste():
    logging.info('Paste')


if __name__ == '__main__':
    fire.Fire({
        'copy': copy,
        'paste': paste,
    })
