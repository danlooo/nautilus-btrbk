# nautilus-btrbk: Open file versions in nautilus context menu

## Setup

First, install btrbk and create some snapshots.
Then, install the extension for the Nautilus file manager:

```
sudo apt install -y python3-nautilus xdg-utils
curl https://raw.githubusercontent.com/danlooo/nautilus-btrbk/main/nautilus-btrbk.py > ~/.local/share/nautilus-python/extensions/nautilus-btrbk.py
chmod +rx ~/.local/share/nautilus-python/extensions/nautilus-btrbk.py
```
Now, there is a context menu entry called "Open Versions" in Nautilus.

Example btrbk config file in `/etc/btrbk/btrbk.conf` with btrfs subvolumes `/` and `/home` and snapshot directories e.g. `/home/.snapshots`:

```
volume /
	subvolume .
	snapshot_name root
	snapshot_dir .snapshots

volume /home
        subvolume .
        snapshot_name home
        snapshot_dir .snapshots
```