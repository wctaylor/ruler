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

import gi
import math
import cairo
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk, Gdk, Pango, PangoCairo

@Gtk.Template(resource_path='/com/github/wctaylor/ruler/window.ui')
class RulerWindow(Gtk.ApplicationWindow):
    # Set a default size of 5" x 1"
    MM_PER_INCH      = 25.4
    DEFAULT_LONG_DIM_MM   = 5*MM_PER_INCH
    DEFAULT_SHORT_DIM_MM  = 1*MM_PER_INCH

    __gtype_name__ = 'RulerWindow'

    ruler_area = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ruler_area.connect("draw", self.on_draw)

    def set_size(self, long_dim_mm, short_dim_mm,
                 long_dim_px, short_dim_px, orientation):
        self.long_dim_mm  = long_dim_mm
        self.short_dim_mm = short_dim_mm
        self.long_dim_px  = long_dim_px
        self.short_dim_px = short_dim_px

        self.long_px_per_mm  = long_dim_px/long_dim_mm
        self.short_px_per_mm = short_dim_px/short_dim_mm

        self.orientation = orientation

        if (orientation == "landscape"):
            self.ruler_area.set_size_request(long_dim_px, short_dim_px)
        else:
            self.ruler_area.set_size_request(short_dim_px, long_dim_px)

    def draw_ruler(self):
        self.ruler_area.queue_draw()

    def on_draw(self, area, context):
        FONT = Pango.FontDescription("Sans 10")
        pc_layout  = PangoCairo.create_layout(context)
        pc_layout.set_font_description(FONT)

        context.set_source_rgb(200/255, 200/255, 200/255)
        if (self.orientation == "landscape"):
            context.rectangle(0, 0, self.long_dim_px, self.short_dim_px)
        else:
            context.rectangle(0, 0, self.short_dim_px, self.long_dim_px)
        context.fill()

        context.set_source_rgb(0, 0, 0)

        mms = math.floor(self.long_dim_mm)
        for mm in range(mms):
            if ((mm % 10) == 0):
                length_px = (self.short_dim_px/4)
            elif ((mm % 5) == 0):
                length_px = (self.short_dim_px/4)*(1/2)
            else:
                length_px = (self.short_dim_px/4)*((1/2)**2)

            if (self.orientation == "landscape"):
                context.move_to(mm*self.long_px_per_mm, 0)
                context.line_to(mm*self.long_px_per_mm, length_px)
                if ((mm % 10) == 0):
                    pc_layout.set_text(f"{mm//10}")
                    PangoCairo.update_layout(context, pc_layout)
                    PangoCairo.show_layout(context, pc_layout)
            else:
                context.move_to(0, mm*self.long_px_per_mm)
                context.line_to(length_px, mm*self.long_px_per_mm)
        context.stroke()

        px_per_inch = self.long_px_per_mm*self.MM_PER_INCH
        sixteenths = math.floor((self.long_dim_mm/self.MM_PER_INCH)*16)
        for sixteenth in range(sixteenths):
            if ((sixteenth % 16) == 0):
                length_px = (self.short_dim_px/4)
            elif ((sixteenth % 8) == 0):
                length_px = (self.short_dim_px/4)*(3/4)
            elif ((sixteenth % 4) == 0):
                length_px = (self.short_dim_px/4)*((3/4)**2)
            elif ((sixteenth % 2) == 0):
                length_px = (self.short_dim_px/4)*((3/4)**3)
            else:
                length_px = (self.short_dim_px/4)*((3/4)**4)

            if (self.orientation == "landscape"):
                context.move_to((sixteenth/16)*px_per_inch,
                                self.short_dim_px - length_px)
                context.line_to((sixteenth/16)*px_per_inch,
                                self.short_dim_px)
                if ((sixteenth % 16) == 0):
                    context.move_to((sixteenth/16)*px_per_inch,
                                self.short_dim_px - length_px - 15)
                    pc_layout.set_text(f"{sixteenth//16}")
                    PangoCairo.update_layout(context, pc_layout)
                    PangoCairo.show_layout(context, pc_layout)
            else:
                context.move_to(self.short_dim_px - length_px,
                                (sixteenth/16)*px_per_inch)
                context.line_to(self.short_dim_px,
                                (sixteenth/16)*px_per_inch)
        context.stroke()
