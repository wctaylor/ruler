# main.py
#
# Copyright 2021 Will Taylor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, Gio

from .window import RulerWindow


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.github.wctaylor.Ruler',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        window = self.props.active_window
        if not window:
            window = RulerWindow(application=self)
        window.present()

        # Initial set up
        gdk_window  = window.get_window()
        display     = gdk_window.get_display()
        monitor     = display.get_monitor_at_window(gdk_window)

        geometry      = monitor.get_geometry()
        max_width_px  = geometry.width
        max_height_px = geometry.height
        max_width_mm  = monitor.get_width_mm()
        max_height_mm = monitor.get_height_mm()

        window.width_px_per_mm  = max_width_px/max_width_mm
        window.height_px_per_mm = max_height_px/max_height_mm

def main(version):
    app = Application()
    return app.run(sys.argv)
