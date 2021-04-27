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
        super().__init__(application_id='org.gnome.ruler',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = RulerWindow(application=self)
        win.present()

        win.set_scale()
        win.draw_ruler()
        # win.draw_ruler(width_mm, height_mm, width_px, height_px)
        # screen = self.get_screen()
        # display = screen.get_display()
        # monitor = display.get_n_monitors()
        # monitor = display.get_monitor(monitor)

        # print(window.get_width(),
        #       window.get_height(),
        #       window.get_scale_factor())


def main(version):
    app = Application()
    return app.run(sys.argv)
