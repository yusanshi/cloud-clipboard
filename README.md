# cloud-clipboard

<https://clipboard.yusanshi.com>

Sync your clipboard across devices.

## Database

This project uses Redis as the database and the HTTP interface provided by [webdis](https://github.com/nicolasff/webdis). These info are needed:

- `host`: the address of webdis.
- `prefix`: used to isolate difference space.
- `username` and `password` (optional, but strongly recommended): used for HTTP Basic Auth.

##  Supported clients

> |                   | Clipboard: `text/plain` | Clipboard: `image/png` | Clipboard: `image/jpeg` | Clipboard: `image/heic`, `image/heif` | File (of any type) |
> | ----------------- | ----------------------- | ---------------------- | ----------------------- | ------------------------------------- | ------------------- |
> | **webpage**       | ✓                       | ✓                      |                         |                                       | ✓                   |
> | **iOS Shortcuts** | ✓                       | ✓                      | ✓ | ✓[^1]                                | ✓                   |
> | **Ubuntu GNOME**  | ✓                       | ✓                      | ✓                       |                                       |                     |
>
> [^1]: For iOS, the HEIC/HEIF images will be converted to JPG before pushing to cloud.

### webpage: `index.html`

<https://clipboard.yusanshi.com>

The Redis info can be set at the bottom of the webpage. These info are saved in `localStorage` so you only need to input it once for each device.

### iOS Shortcuts

**For clipboard**
- Pull to local: <https://www.icloud.com/shortcuts/d9c50b4168f84361a1ee49334a2487d4>
- Push to cloud: <https://www.icloud.com/shortcuts/7128f577745443828fa0d393533b3386>

**For file**

- Download file: <https://www.icloud.com/shortcuts/e34ffb0af26d4efea803c61b0f53b41c>
- Upload file (shown in the share sheet): <https://www.icloud.com/shortcuts/a969c3e19a0740febe890ac8f15216bb>


### Ubuntu GNOME: `main.py`

You should bind these commands to keyboard shortcuts:

- Copy selected content and push to cloud clipboard: `python /path/to/main.py copy --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`
  
- Pull from cloud clipboard and paste: `python /path/to/main.py paste --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`

