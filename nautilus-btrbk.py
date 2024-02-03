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
class BtrfsExtension(GObject.Object, FileManager.MenuProvider):
    snapshots_root = "/home"
    snapshots_dir = "/home/.snapshots"

    def get_version(self, version_path, current_path):
        s = current_path.replace(self.snapshots_root ,"")
        version = version_path.replace(self.snapshots_dir, "").replace(s, "").replace("/", "")
        return version

    def open_path(self, menu, version):
        print(version)
        system(f"xdg-open {version}")

    def get_file_items(self, window, files):
        current_path = unquote(urlparse(files[0].get_uri()).path)

        version_paths = []
        for snapshot in listdir(self.snapshots_dir):
            snapshot_path = current_path.replace("/home", f"{self.snapshots_dir}/{snapshot}")
            if path.exists(snapshot_path):
                version_paths += [snapshot_path]

        menu = FileManager.MenuItem(
            name='BtrfsExtension::Open',
            label="Open Versions"
        )

        # Context Submenu
        submenu = FileManager.Menu()
        menu.set_submenu(submenu)

        for version_path in version_paths:
            item = FileManager.MenuItem(
                name='BtrfsExtension::Version' + version_path,
                label= self.get_version(version_path, current_path)
            )
            item.connect('activate', self.open_path, version_path)
            submenu.append_item(item)

        return (menu,)
