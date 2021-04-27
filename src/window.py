# window.py
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

import math
import cairo
from gi.repository import Gtk, Gdk

@Gtk.Template(resource_path='/org/gnome/ruler/window.ui')
class RulerWindow(Gtk.ApplicationWindow):
    # Set a default size of 5" x 1"
    MM_PER_INCH      = 25.4
    LONG_LENGTH_MM   = 5*MM_PER_INCH
    SHORT_LENGTH_MM  = 1*MM_PER_INCH

    __gtype_name__ = 'RulerWindow'

    ruler_area = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ruler_area.connect("draw", self.on_draw)

    def set_scale(self):
        window  = self.get_window()
        display = window.get_display()
        monitor = display.get_monitor_at_window(window)

        geometry      = monitor.get_geometry()
        max_width_px  = geometry.width
        max_height_px = geometry.height
        max_width_mm  = monitor.get_width_mm()
        max_height_mm = monitor.get_height_mm()

        self.w_px_per_mm   = max_width_px/max_width_mm
        self.h_px_per_mm   = max_height_px/max_height_mm

        if (max_width_px >= max_height_px):
            self.width_px  = self.LONG_LENGTH_MM*self.w_px_per_mm
            self.height_px = self.SHORT_LENGTH_MM*self.h_px_per_mm
        else:
            self.height_px = self.LONG_LENGTH_MM*self.w_px_per_mm
            self.width_px  = self.SHORT_LENGTH_MM*self.h_px_per_mm

        self.ruler_area.set_size_request(self.width_px, self.height_px)

    def draw_ruler(self):
        self.ruler_area.queue_draw()

    def on_draw(self, area, context):
        context.set_source_rgb(200/255, 200/255, 200/255)
        context.rectangle(0, 0, self.width_px, self.height_px)
        context.fill()

        context.set_source_rgb(0, 0, 0)

        mms = math.floor(self.LONG_LENGTH_MM)
        for mm in range(mms):
            if ((mm % 10) == 0):
                height_px = self.height_px/4
            elif ((mm % 5) == 0):
                height_px = self.height_px/8
            else:
                height_px = self.height_px/16

            context.move_to(mm*self.w_px_per_mm, 0)
            context.line_to(mm*self.w_px_per_mm, height_px)
        context.stroke()

        sixteenths = math.floor(self.LONG_LENGTH_MM/self.MM_PER_INCH*16)
        for sixteenth in range(sixteenths):
            if ((sixteenth % 16) == 0):
                height_px = (self.height_px/4)
            elif ((sixteenth % 8) == 0):
                height_px = (self.height_px/4)*(3/4)
            elif ((sixteenth % 4) == 0):
                height_px = (self.height_px/4)*((3/4)**2)
            elif ((sixteenth % 2) == 0):
                height_px = (self.height_px/4)*((3/4)**3)
            else:
                height_px = (self.height_px/4)*((3/4)**4)

            context.move_to((sixteenth/16)*self.w_px_per_mm*self.MM_PER_INCH,
                            self.height_px - height_px)
            context.line_to((sixteenth/16)*self.w_px_per_mm*self.MM_PER_INCH,
                            self.height_px)
        context.stroke()
