# cloud-clipboard

<https://clipboard.yusanshi.com>

Sync your clipboard across devices.

## Database

This project uses Redis as the database and the HTTP interface provided by [webdis](https://github.com/nicolasff/webdis). These info are needed:

- `host`: the address of webdis.
- `prefix`: used to isolate difference space.
- `username` and `password` (optional, but strongly recommended): used for HTTP Basic Auth.

##  Supported clients

### browser: `index.html`

<https://clipboard.yusanshi.com>

Support syncing clipboard (`text/plain` and `image/png`) and file.

The Redis info can be set at the bottom of the webpage. These info are saved in `localStorage` so you only need to input it once for each device.

### Ubuntu GNOME: `main.py`

Only support syncing clipboard (`text/plain` and `image/png`). No file sync.

You should bind these commands to keyboard shortcuts:

- Copy selected content and push to cloud clipboard: `python /path/to/main.py copy --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`
  
- Pull from cloud clipboard and paste: `python /path/to/main.py paste --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`


## Supported data types

### Clipboard: `text/plain`

![image](https://github.com/yusanshi/cloud-clipboard/assets/36265606/0f830a05-6d19-409e-8c20-46af5f6faee6)

### Clipboard: `image/png`

![image](https://github.com/yusanshi/cloud-clipboard/assets/36265606/fc8b237e-cac8-400f-a578-d9a46bf1fee1)

### File

![image](https://github.com/yusanshi/cloud-clipboard/assets/36265606/b8d4bcaf-9c5d-4578-b6c4-694f5da32377)

