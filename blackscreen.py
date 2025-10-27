#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class BlackCover(Gtk.Window):
    def __init__(self, monitor):
        super().__init__()

        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_accept_focus(False)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.stick()
        self.fullscreen()

        geo = monitor.get_geometry()

        self.move(geo.x, geo.y)
        self.set_default_size(geo.width, geo.height)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))

        # Hide the cursor when the window is realized
        self.connect("realize", self.hide_cursor)

        # Event to uncover the screen
        self.connect("button-press-event", lambda *_: Gtk.main_quit())
        self.connect("key-press-event", lambda w, e: Gtk.main_quit() if e.keyval == Gdk.KEY_Escape else None)

        self.show_all()

    def hide_cursor(self, widget):
        gdk_window = self.get_window()
        if gdk_window:
            blank = Gdk.Cursor.new(Gdk.CursorType.BLANK_CURSOR)
            gdk_window.set_cursor(blank)

def main():
    Gtk.init([])
    display = Gdk.Display.get_default()
    for i in range(display.get_n_monitors()):
        monitor = display.get_monitor(i)
        # print(monitor)
        BlackCover(monitor)
    Gtk.main()

if __name__ == "__main__":
    main()
