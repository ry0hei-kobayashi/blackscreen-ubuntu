#!/usr/bin/env python3
import gi
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class BlackCover(Gtk.Window):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_accept_focus(False)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.NORMAL)
        self.move(x, y)
        self.set_default_size(w, h)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))
        self.connect("button-press-event", self.on_click)
        self.show_all()
        self.fullscreen()
        try:
            self.get_window().set_cursor(Gdk.Cursor.new(Gdk.CursorType.BLANK_CURSOR))
        except:
            pass

    def on_click(self, widget, event):
        Gtk.main_quit()

def get_monitors():
    result = subprocess.run(['xrandr', '--listactivemonitors'], stdout=subprocess.PIPE, encoding='utf-8')
    lines = result.stdout.strip().split('\n')[1:]  # skip header
    monitors = []
    for line in lines:
        parts = line.split()
        res_pos = parts[2]  # e.g., "3440/797x1440/333+0+0"
        size_str, pos_str = res_pos.split('+', 1)
        width_raw, height_raw = size_str.split('x')
        width = int(width_raw.split('/')[0])
        height = int(height_raw.split('/')[0])
        x, y = map(int, pos_str.split('+'))
        monitors.append((x, y, width, height))
    return monitors

def main():
    Gtk.init([])
    covers = []
    for x, y, w, h in get_monitors():
        cover = BlackCover(x, y, w, h)
        covers.append(cover)
    Gtk.main()

if __name__ == "__main__":
    main()

