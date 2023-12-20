# cloud-clipboard

<https://clipboard.yusanshi.com>

Sync your clipboard across devices.

- Support clipboard (text/image) and file.
- Don't need to be within the same LAN (at the cost of additional online database).
- Multiple clients: webpage/iOS/Linux/Windows.

## DEMO

**Clipboard: text**

Copy text to clipboard on PC and paste on iPhone, and then reverse the process.

https://github.com/yusanshi/cloud-clipboard/assets/36265606/ff3d73cb-7af4-462f-9687-d41a98eb98a7

**Clipboard: image**

Copy an image to clipboard on PC and paste on iPhone, and then reverse the process.

https://github.com/yusanshi/cloud-clipboard/assets/36265606/1734eb8f-3873-4b70-905c-0b5ec3b73ec5

**File**

Upload a file from PC and download to iPhone, and then reverse the process.

https://github.com/yusanshi/cloud-clipboard/assets/36265606/50029f91-8355-4705-9521-c7d26b21e17c


## Database

This project uses Redis as the database and the HTTP interface provided by [webdis](https://github.com/nicolasff/webdis). These info are needed:

- `host`: the address of webdis.
- `prefix`: used to isolate difference space.
- `username` and `password` (optional, **but strongly recommended**): used for HTTP Basic Auth.

This project comes with a public webdis instance for testing. It is **(1) not secure**, (2) slow. You should always create your own webdis database before real usage.

##  Supported clients

> |                   | Clipboard: `text/plain` | Clipboard: `image/png` | Clipboard: `image/jpeg` | Clipboard: `image/heic`, `image/heif` | File (of any type) |
> | ----------------- | ----------------------- | ---------------------- | ----------------------- | ------------------------------------- | ------------------- |
> | **webpage**       | ✓                       | ✓                      | [^1] |                                       | ✓                   |
> | **iOS Shortcuts** | ✓                       | ✓                      | ✓ | ✓[^2]                               | ✓                   |
> | **Linux Desktop** | ✓                       | ✓                      | ✓                       |                                       |                     |
> | **Windows** | ✓ | ✓[^3] | ✓ | | |
>
> [^1]: Has been implemented in the code. But currently the implementations of the [Clipboard API](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API) do not support `image/jpeg`.
> [^2]: For iOS, the HEIC/HEIF images will be converted to JPG before being pushed to cloud.
> [^3]: Due to technical limit, the alpha channel is removed and filled with white (`#FFF`).

### webpage: `index.html`

<https://clipboard.yusanshi.com>

The Redis info can be set at the bottom of the webpage. These info are saved in `localStorage` so you only need to input it once for each device.

We use Redis PUB/SUB to notify the changes, so you don't need to refresh the pages to get the latest status.

The webpage should be usable for all platforms. But it requires you to open the webpage and click pulling or pushing buttons. To save some keystrokes, you can use the clients for specific platforms. For example, with the Linux/Windows client, you can bind keyboard shortcuts to "copying to cloud" and "pasting from cloud" and then copy or paste with only one hotkey stroke.

### iOS Shortcuts

**For clipboard**

- Pull to local: <https://www.icloud.com/shortcuts/d9c50b4168f84361a1ee49334a2487d4>
- Push to cloud: <https://www.icloud.com/shortcuts/7128f577745443828fa0d393533b3386>

**For file**

- Download file: <https://www.icloud.com/shortcuts/e34ffb0af26d4efea803c61b0f53b41c>
- Upload file (shown in the share sheet): <https://www.icloud.com/shortcuts/a969c3e19a0740febe890ac8f15216bb>

You can add the first three shortcuts to home screen for quick use. The last one can be triggered when you "Share" something in Files or Photos APP.

![image](https://github.com/yusanshi/cloud-clipboard/assets/36265606/cdd4b9de-04f1-406b-9649-2d4bef3ceb1c)

### Linux Desktop: `linux.py`

> Tested on Ubuntu GNOME (X11).

First install some packages:
```bash
pip install requests fire
sudo apt install xclip xdotool # if you use APT as the package manager
```
You can then bind these commands to keyboard shortcuts:

- Copy selected content (send `Ctrl+C`) and push to cloud clipboard: `python /path/to/linux.py copy --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`
- Pull from cloud clipboard and paste (send `Ctrl+V`): `python /path/to/linux.py paste --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`

### Windows: `windows.py`

> Tested on  Windows 11.

First install some packages:
```bash
pip install requests fire pyautogui Pillow pywin32
```
You can then bind these commands to keyboard shortcuts:

> Note: (1) we use `pythonw` instead of `python` to suppress the window popping up. (2) [AutoHotkey](https://www.autohotkey.com/) is recommended to bind the keyboard shortcuts.

- Copy selected content (send `Ctrl+C`) and push to cloud clipboard: `pythonw /path/to/windows.py copy --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`
- Pull from cloud clipboard and paste (send `Ctrl+V`): `pythonw /path/to/windows.py paste --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`



