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

@Gtk.Template(resource_path='/com/github/wctaylor/Ruler/window.ui')
class RulerWindow(Gtk.ApplicationWindow):
    MARGIN_MM    = 2.5
    MM_PER_INCH  = 25.4
    PTS_PER_INCH = 72
    PTS_PER_MM   = PTS_PER_INCH/MM_PER_INCH

    # The shorter dimension is fixed to a maximum of 0.5"
    MAX_RULER_HEIGHT_MM = 0.5*MM_PER_INCH

    __gtype_name__ = 'RulerWindow'

    ruler_area = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # These will be set when created from a GtkApplication
        self.width_px_per_mm      = None
        self.height_px_per_mm     = None
        self.monitor_aspect_ratio = None

        self.ruler_area.connect("draw", self.on_draw)

        style_context    = self.get_style_context()
        self.font_family = style_context.get_property("font-family",
                                                      self.get_state())

    def on_draw(self, area, context):
        if (self.width_px_per_mm is None):
            return
        if (self.height_px_per_mm is None):
            return
        if (self.monitor_aspect_ratio is None):
            return

        width_px        = area.get_allocated_width()
        height_px       = area.get_allocated_height()
        ruler_height_px = self.calc_ruler_height(height_px,
                                                 self.height_px_per_mm)

        margin_px         = self.MARGIN_MM*self.width_px_per_mm
        area.props.margin = margin_px

        if (width_px/height_px >= 1.25*self.monitor_aspect_ratio):
            self.draw_ruler(context, width_px, ruler_height_px, 0, 0, 0)
        elif (height_px/width_px >= 1.25*self.monitor_aspect_ratio):
            self.draw_ruler(context, height_px, ruler_height_px, 0, 0, math.pi/2)
        else:
            # Draw horizontally along the top,
            # with space for others along the sides
            self.draw_ruler(context,
                            width_px - 2*(ruler_height_px + margin_px),
                            ruler_height_px,
                            ruler_height_px + margin_px, 0, 0)

            # Draw horizontally along the bottom,
            # with space for others along the sides
            self.draw_ruler(context,
                            width_px - 2*(ruler_height_px + margin_px),
                            ruler_height_px,
                            ruler_height_px + margin_px, height_px - ruler_height_px, 0)

            # Draw vertically along the left side
            # with space for others along the top and bottom
            self.draw_ruler(context,
                            height_px - 2*ruler_height_px, ruler_height_px,
                            margin_px, ruler_height_px, math.pi/2)

            # Draw vertically along the right side
            # with space for others along the top and bottom
            self.draw_ruler(context,
                            height_px - 2*ruler_height_px, ruler_height_px,
                            width_px - ruler_height_px - margin_px, ruler_height_px, math.pi/2)

    def calc_ruler_height(self, height_px, height_px_per_mm):
        ruler_height_px      = min(height_px,
                                   self.MAX_RULER_HEIGHT_MM*height_px_per_mm)
        return ruler_height_px

    def draw_ruler(self, context, width_px, height_px,
              width_offset_px, height_offset_px, angle_radians):
        width_mm  = width_px/self.width_px_per_mm
        height_mm = height_px/self.height_px_per_mm

        context.save()
        context.translate(width_offset_px, height_offset_px)
        context.rotate(angle_radians)
        context.translate(0, -height_px*math.sin(angle_radians))
        context.set_source_rgb(154/255, 153/255, 150/255)
        context.rectangle(0, 0, width_px, height_px)
        context.fill()

        font_size = (height_mm/4)*self.PTS_PER_MM
        font      = Pango.FontDescription(f"{self.font_family} {font_size}")
        pc_layout = PangoCairo.create_layout(context)
        pc_layout.set_font_description(font)

        context.set_source_rgb(0, 0, 0)

        mms = math.floor(width_mm-1)
        # Skip last unit so marks aren't on right/bottom edge
        # when drawn alone
        for mm in range(mms-1):
            if ((mm % 10) == 0):
                length_px = (height_px/4)
            elif ((mm % 5) == 0):
                length_px = (height_px/4)*(1/2)
            else:
                length_px = (height_px/4)*((1/2)**2)

            # Add 1 mm offset so marks aren't on the left/top edge
            # when drawn alone
            x_px = mm*self.width_px_per_mm + self.width_px_per_mm
            context.move_to(x_px, 0)
            context.line_to(x_px, length_px)
            if ((mm % 10) == 0):
                pc_layout.set_text(f"{mm//10}")
                PangoCairo.update_layout(context, pc_layout)
                PangoCairo.show_layout(context, pc_layout)
        context.stroke()

        px_per_inch = self.width_px_per_mm*self.MM_PER_INCH
        sixteenths = math.floor((width_mm/self.MM_PER_INCH)*16)
        # Skip last unit so marks aren't on right/bottom edge
        # when drawn alone
        for sixteenth in range(sixteenths-1):
            if ((sixteenth % 16) == 0):
                length_px = (height_px/4)
            elif ((sixteenth % 8) == 0):
                length_px = (height_px/4)*(3/4)
            elif ((sixteenth % 4) == 0):
                length_px = (height_px/4)*((3/4)**2)
            elif ((sixteenth % 2) == 0):
                length_px = (height_px/4)*((3/4)**3)
            else:
                length_px = (height_px/4)*((3/4)**4)

            # Add 1 mm offset so marks aren't on the left/top edge
            # when drawn alone
            x_px = (sixteenth/16)*px_per_inch + self.width_px_per_mm
            context.move_to(x_px, height_px - length_px)
            context.line_to(x_px, height_px)
            if ((sixteenth % 16) == 0):
                context.move_to(x_px,
                                height_px - length_px - 1.5*font_size)
                pc_layout.set_text(f"{sixteenth//16}")
                PangoCairo.update_layout(context, pc_layout)
                PangoCairo.show_layout(context, pc_layout)
        context.stroke()
        context.restore()
