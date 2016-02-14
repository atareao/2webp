#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# LoginDialog
#
# Copyright (C) 2015 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
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
#
#
from gi.repository import Gtk, Gdk
from gi.repository import GObject
import comun
import shlex
import subprocess
import mimetypes
import os
import urllib
import urllib.request
import threading

SUPPORTED_MIMES = ['image/png', 'image/jpeg', 'image/tiff']

GObject.threads_init()


def ejecuta(comando):
    args = shlex.split(comando)
    p = subprocess.Popen(args, bufsize=10000, stdout=subprocess.PIPE)
    valor = p.communicate()[0]
    return valor


class Convert2WebpDialog(Gtk.Dialog):
    def __init__(self):
        self.code = None
        Gtk.Dialog.__init__(self)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_title(comun.APPNAME)
        self.set_icon_from_file(comun.ICON)
        self.set_default_size(500, 500)
        #
        vbox = Gtk.VBox(spacing=5)
        self.get_content_area().add(vbox)
        self.background = Gtk.Image.new_from_file(comun.BACKGROUND)
        vbox.pack_start(self.background, True, True, 0)
        # set icon for drag operation
        self.background.connect('drag-begin', self.drag_begin)
        self.background.connect('drag-data-get', self.drag_data_get_data)
        self.background.connect('drag-data-received', self.drag_data_received)
        #
        dnd_list = [Gtk.TargetEntry.new(
            'text/uri-list', 0, 100), Gtk.TargetEntry.new('text/plain', 0, 80)]
        self.background.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK, dnd_list, Gdk.DragAction.COPY)
        self.background.drag_source_add_uri_targets()
        dnd_list = Gtk.TargetEntry.new("text/uri-list", 0, 0)
        self.background.drag_dest_set(
            Gtk.DestDefaults.MOTION |
            Gtk.DestDefaults.HIGHLIGHT |
            Gtk.DestDefaults.DROP,
            [dnd_list],
            Gdk.DragAction.MOVE)
        self.background.drag_dest_add_uri_targets()
        #
        self.show_all()

    def drag_begin(self, widget, context):
        pass

    def drag_data_get_data(self, treeview, context, selection, target_id,
                           etime):
        pass

    def drag_data_received(self, widget, drag_context, x, y, selection_data,
                           info, timestamp):
        for filename in selection_data.get_uris():
            if len(filename) > 8:
                filename = urllib.request.url2pathname(filename)
                filename = filename[7:]
                mime = mimetypes.guess_type(filename)
                if os.path.exists(filename):
                    mime = mimetypes.guess_type(filename)[0]
                    if mime in SUPPORTED_MIMES:
                        destinationfilename, originalextension = \
                            os.path.splitext(filename)
                        destinationfilename += '.webp'
                        quality = 80
                        t = threading.Thread(target=ejecuta, args=(
                            'cwebp -q %s %s -o %s' % (quality,
                                                      filename,
                                                      destinationfilename),))
                        t.daemon = True
                        t.start()
        return True

if __name__ == '__main__':
    ld = Convert2WebpDialog()
    ld.run()
