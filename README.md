# cloud-clipboard

<https://clipboard.yusanshi.com>

Sync your clipboard across devices.

- Support clipboard (text/image) and file.
- Don't need to be within the same LAN (at the cost of additional online database).
- Multiple clients: webpage/iOS/Linux/Windows.

## Database

This project uses Redis as the database and the HTTP interface provided by [webdis](https://github.com/nicolasff/webdis). These info are needed:

- `host`: the address of webdis.
- `prefix`: used to isolate difference space.
- `username` and `password` (optional, **but strongly recommended**): used for HTTP Basic Auth.

This project comes with a public webdis instance for testing. It is **(1) not secure**, (2) slow. You should always create your own webdis database before real usage.

##  Supported clients

> |                   | Clipboard: `text/plain` | Clipboard: `image/png` | Clipboard: `image/jpeg` | Clipboard: `image/heic`, `image/heif` | File (of any type) |
> | ----------------- | ----------------------- | ---------------------- | ----------------------- | ------------------------------------- | ------------------- |
> | **webpage**       | ✓                       | ✓                      |                         |                                       | ✓                   |
> | **iOS Shortcuts** | ✓                       | ✓                      | ✓ | ✓[^1]                                | ✓                   |
> | **Linux Desktop** | ✓                       | ✓                      | ✓                       |                                       |                     |
>
> [^1]: For iOS, the HEIC/HEIF images will be converted to JPG before being pushed to cloud.

### webpage: `index.html`

<https://clipboard.yusanshi.com>

This should be usable for all platforms.

The Redis info can be set at the bottom of the webpage. These info are saved in `localStorage` so you only need to input it once for each device.

We use Redis PUB/SUB to notify the changes, so you don't need to refresh the pages to get the latest status.

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

> Tested on Ubuntu GNOME.

First install some packages:
```bash
pip install requests fire
sudo apt install xclip xdotool
```
You can then bind these commands to keyboard shortcuts:

- Copy selected content and push to cloud clipboard: `python /path/to/linux.py copy --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`
- Pull from cloud clipboard and paste: `python /path/to/linux.py paste --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`





