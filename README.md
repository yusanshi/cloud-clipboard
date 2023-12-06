# cloud-clipboard

Sync your clipboard across devices.

##  Supported clients

### browser: `index.html`

<https://clipboard.yusanshi.com>

I use it for my iPhone.

Remember to set the Redis info ([webdis](https://github.com/nicolasff/webdis)) at the bottom of the webpage. These info are saved in `localStorage` so you only need to input it once for each device.

### Ubuntu GNOME: `main.py`

You should bind these commands to keyboard shortcuts:

- Copy selected content and push to cloud clipboard: `python /path/to/main.py copy --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`
  
- Pull from cloud clipboard and paste: `python /path/to/main.py paste --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`
  
> About Redis info: `host` is the address of webdis. `prefix` is used to isolate difference space. `username` and `password` are for HTTP Basic Auth. You should set the same info for all your clients and devices.



## Supported MIME types

### `text/plain`

  ![](https://github.com/yusanshi/cloud-clipboard/assets/36265606/ede5557f-fab9-4209-a967-066dda80dd8e)

### `image/png`

  ![](https://github.com/yusanshi/cloud-clipboard/assets/36265606/f5c62bc3-bc66-4729-b606-f894ea6a202a)



