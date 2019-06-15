import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
import os
import sys


class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        self.open_file_dialog()


    def open_file_dialog(self):
        dialog = Gtk.FileChooserDialog("Please choose a folder", None,Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,"Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
            os.system("python test_script.py "+dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # app action quit, connected to the callback function
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.quit_callback)
        self.add_action(quit_action)

        # get the menu from the ui file with a builder
        builder = Gtk.Builder()
        # try:
        #     builder.add_from_file("filechooserdialog.ui")
        # except:
        #     print("file not found")
        #     sys.exit()
        # menu = builder.get_object("appmenu")
        # self.set_app_menu(menu)

    # callback function for quit
    def quit_callback(self, action, parameter):
        self.quit()

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)