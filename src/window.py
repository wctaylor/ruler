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
    MARGIN_MM   = 5
    MM_PER_INCH = 25.4

    __gtype_name__ = 'RulerWindow'

    ruler_area = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ruler_area.connect("draw", self.on_draw)

        style_context = self.get_style_context()
        self.font_family = style_context.get_property("font-family",
                                                      self.get_state())
        self.font_size   = style_context.get_property("font-size",
                                                      self.get_state())

    def on_draw(self, area, context):
        font = Pango.FontDescription(f"{self.font_family} {self.font_size}")
        pc_layout  = PangoCairo.create_layout(context)
        pc_layout.set_font_description(font)

        width_px  = area.get_allocated_width()
        height_px = area.get_allocated_height()

        if (width_px >= height_px):
            long_dim_px     = width_px
            short_dim_px    = height_px
            orientation     = "landscape"
            long_px_per_mm  = self.width_px_per_mm
            short_px_per_mm = self.height_px_per_mm
        else:
            long_dim_px     = height_px
            short_dim_px    = width_px
            orientation     = "portrait"
            long_px_per_mm  = self.width_px_per_mm
            short_px_per_mm = self.height_px_per_mm

        margin_px         = self.MARGIN_MM*long_px_per_mm
        area.props.margin = margin_px

        long_dim_mm  = long_dim_px/long_px_per_mm

        # The shorter dimension is fixed to a maximum of 1"
        short_px_per_inch = self.MM_PER_INCH*short_px_per_mm
        short_dim_px      = min(short_dim_px, short_px_per_inch)
        short_dim_mm      = short_dim_px/short_px_per_mm

        context.set_source_rgb(200/255, 200/255, 200/255)
        if (orientation == "landscape"):
            context.rectangle(0, 0, long_dim_px, short_dim_px)
        else:
            context.rectangle(0, 0, short_dim_px, long_dim_px)
        context.fill()

        context.set_source_rgb(0, 0, 0)

        mms = math.floor(long_dim_mm)
        for mm in range(mms):
            if ((mm % 10) == 0):
                length_px = (short_dim_px/4)
            elif ((mm % 5) == 0):
                length_px = (short_dim_px/4)*(1/2)
            else:
                length_px = (short_dim_px/4)*((1/2)**2)

            # Add 1 mm offset so marks aren't right on the edge
            if (orientation == "landscape"):
                context.move_to(mm*long_px_per_mm + long_px_per_mm, 0)
                context.line_to(mm*long_px_per_mm + long_px_per_mm, length_px)
                if ((mm % 10) == 0):
                    pc_layout.set_text(f"{mm//10}")
                    PangoCairo.update_layout(context, pc_layout)
                    PangoCairo.show_layout(context, pc_layout)
            else:
                context.move_to(0, mm*long_px_per_mm + long_px_per_mm)
                context.line_to(length_px, mm*long_px_per_mm + long_px_per_mm)
                if ((mm % 10) == 0):
                    pc_layout.set_text(f"{mm//10}")
                    PangoCairo.update_layout(context, pc_layout)
                    PangoCairo.show_layout(context, pc_layout)
        context.stroke()

        px_per_inch = long_px_per_mm*self.MM_PER_INCH
        sixteenths = math.floor((long_dim_mm/self.MM_PER_INCH)*16)
        for sixteenth in range(sixteenths):
            if ((sixteenth % 16) == 0):
                length_px = (short_dim_px/4)
            elif ((sixteenth % 8) == 0):
                length_px = (short_dim_px/4)*(3/4)
            elif ((sixteenth % 4) == 0):
                length_px = (short_dim_px/4)*((3/4)**2)
            elif ((sixteenth % 2) == 0):
                length_px = (short_dim_px/4)*((3/4)**3)
            else:
                length_px = (short_dim_px/4)*((3/4)**4)

            # Add 1 mm offset so marks aren't right on the edge
            if (orientation == "landscape"):
                context.move_to((sixteenth/16)*px_per_inch + long_px_per_mm,
                                short_dim_px - length_px)
                context.line_to((sixteenth/16)*px_per_inch + long_px_per_mm,
                                short_dim_px)
                if ((sixteenth % 16) == 0):
                    context.move_to((sixteenth/16)*px_per_inch + long_px_per_mm,
                                short_dim_px - length_px
                                - 1.5*self.font_size)
                    pc_layout.set_text(f"{sixteenth//16}")
                    PangoCairo.update_layout(context, pc_layout)
                    PangoCairo.show_layout(context, pc_layout)
            else:
                context.move_to(short_dim_px - length_px,
                                (sixteenth/16)*px_per_inch + long_px_per_mm)
                context.line_to(short_dim_px,
                                (sixteenth/16)*px_per_inch + long_px_per_mm)
                if ((sixteenth % 16) == 0):
                    context.move_to(short_dim_px - length_px
                                    - self.font_size,
                                    (sixteenth/16)*px_per_inch + long_px_per_mm)
                    pc_layout.set_text(f"{sixteenth//16}")
                    PangoCairo.update_layout(context, pc_layout)
                    PangoCairo.show_layout(context, pc_layout)
        context.stroke()
