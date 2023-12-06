# cloud-clipboard

Sync your clipboard across devices.


Currently support these clients:
- `index.html` (<https://clipboard.yusanshi.com>): for browser (I use it for my iPhone).

  Remember to set the Redis info ([webdis](https://github.com/nicolasff/webdis)) at the bottom of the webpage. These info are saved in `localStorage` so you only need to input it once for each device.

- `main.py`: for Ubuntu GNOME desktop.

  You should bind these commands to keyboard shortcuts:

  - Copy selected content and push to cloud clipboard: `python /path/to/main.py copy --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`
  
  - Pull from cloud clipboard and paste: `python /path/to/main.py paste --host "https://example.com/" --prefix "prefix" --username "username" --password "password"`
  
> About Redis info: `host` is the address of webdis. `prefix` is used to isolate difference space. `username` and `password` are for HTTP Basic Auth. You should set the same info for all your clients and devices.



Currently support these MIME types:
- `text/plain`

  ![image](https://github.com/yusanshi/cloud-clipboard/assets/36265606/983b4048-54a4-4854-86fc-1fcde5ebefc7)

- `image/png`

  ![image](https://github.com/yusanshi/cloud-clipboard/assets/36265606/7734906d-bcea-45e5-8cd6-d132856960ee)





