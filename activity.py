#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""LiveDemo Activity: speech recognition demo"""
import pygtk
pygtk.require('2.0')
import gtk

import gobject

from sugarlistens import helper

from gettext import gettext as _

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityButton
from sugar.activity.widgets import ActivityToolbox
from sugar.activity.widgets import TitleEntry
from sugar.activity.widgets import StopButton
from sugar.activity.widgets import ShareButton

import os


class LiveDemoActivity(activity.Activity):
    """LiveDemoActivity class as specified in activity.info"""

    def __init__(self, handle):
        """Set up the LiveDemo activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        # box principal
        main_box = gtk.VBox()
        self.init_gui(main_box)
        self.set_canvas(main_box)
        self.set_toolbar_box(toolbar_box)
        self.set_canvas(main_box)
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
        main_box.show_all()
        
        self.__path = os.path.dirname(os.path.abspath(__file__))
        self.__recognizer = helper.RecognitionHelper(self.__path)
        self.__recognizer.listen(self.final_result)
        self.__recognizer.start_listening()

    def init_gui(self, vbox):
        """Initialize the GUI components"""
        self.__textbuf = gtk.TextBuffer()
        self.__text = gtk.TextView(self.__textbuf)
        self.__text.set_wrap_mode(gtk.WRAP_WORD)
        vbox.pack_start(self.__text)

    def final_result(self, text):
        """Insert the final result."""
        self.__textbuf.begin_user_action()
        #self.textbuf.delete_selection(True, self.text.get_editable())
        self.__textbuf.set_text(text)
        self.__textbuf.end_user_action()
