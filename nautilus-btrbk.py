#!/usr/bin/env python3

#
# Nautilus plugin to open specific version of a path using btrbk snapshots
#
# requires btrbk and xdg-open
#

from os import listdir, path, system
from urllib.parse import urlparse, unquote
import gi

gi.require_version('Gio', '2.0')
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')
from gi.repository import Gio, GLib, GObject

gi.require_version('Nautilus', '3.0')
from gi.repository import Nautilus as FileManager

class BtrbkExtension(GObject.Object, FileManager.MenuProvider):
    # TODO: Use load_btrbk_config instead
    snapshots_root = "/home"
    snapshots_dir = "/home/.snapshots"

    @staticmethod
    def load_btrbk_config(path="/etc/btrbk/btrbk.conf"):
        config_file = open(path, "r")
        volumes = []
        current_volume = None

        for l in config_file.readlines():
            if l.startswith("#"):
                continue
            items = l.split()
            if len(items) != 2:
                continue
            if items[0] == "volume":
                if current_volume is not None:
                    volumes += [current_volume]
                current_volume = {"name": items[1]}
                continue
            if current_volume is not None:
                current_volume[items[0]] = items[1]

        if current_volume is not None:
            volumes += [current_volume]

        # subvolume with longer file path overwrites sshorter ones
        volumes = sorted(volumes, key = lambda x:len(x["name"]))
        return(volumes)


    def __init__(self):
        self.config = BtrbkExtension.load_btrbk_config()

    def get_version(self, version_path, current_path):
        s = current_path.replace(self.snapshots_root ,"")
        version = version_path.replace(self.snapshots_dir, "").replace(s, "").replace("/", "")
        return version

    def open_path(self, menu, p):
        if path.isdir(p):
            # direct xdg-open is slow on directories
            system(f"xdg-open {p} &")
        else:
            system(f"xdg-open {p}")

    def get_file_items(self, window, files):
        current_path = unquote(urlparse(files[0].get_uri()).path)

        version_paths = []
        for snapshot in listdir(self.snapshots_dir):
            snapshot_path = current_path.replace(self.snapshots_root, f"{self.snapshots_dir}/{snapshot}")
            if path.exists(snapshot_path):
                version_paths += [snapshot_path]
        # show newest version first
        version_paths = sorted(version_paths, reverse=True)

        menu = FileManager.MenuItem(
            name='BtrbkExtension::Open',
            label="Open Versions"
        )

        # Context Submenu
        submenu = FileManager.Menu()
        menu.set_submenu(submenu)

        for version_path in version_paths:
            item = FileManager.MenuItem(
                name='BtrbkExtension::Version' + version_path,
                label= self.get_version(version_path, current_path)
            )
            item.connect('activate', self.open_path, version_path)
            submenu.append_item(item)

        return (menu,)
