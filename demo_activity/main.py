'''
@author: cgueret
'''
import os
import sys
sys.path.append(os.path.join(os.path.expanduser('~'), 'Code/SemanticXO/common/demo_activity'))

import pygtk
pygtk.require('2.0')
import gtk
from sugar.graphics import style
from panels import MetadataPanel, JournalPanel

class MainWindow(object):
    def __init__(self):
        '''
        Constructor
        '''
        # Create the right panel
        metadata_panel = MetadataPanel()
        
        # Create the browser of XO journal
        xo_panel = JournalPanel(metadata_panel)
        
        # Pack everything
        container = gtk.HBox()
        data_sources = gtk.Notebook()
        data_sources.show_border = False
        data_sources.show_tabs = True
        data_sources.append_page(xo_panel.get_widget(), gtk.Label(" XO Journal "))
        container.pack_start(data_sources, False, False, 5)
        container.pack_start(metadata_panel.get_widget(), True, True, 5)
        
        # Create the Window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy_cb)
        self.window.connect("key-press-event", self.keypress_cb)
        self.window.connect("delete_event", self.destroy_cb)
        self.window.set_border_width(style.DEFAULT_PADDING)
        self.window.set_size_request(600, 450)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.add(container)
        self.window.show_all()

    def keypress_cb(self, widget, event):
        if event.keyval == gtk.keysyms.Escape or event.keyval == gtk.keysyms.Return :
            gtk.main_quit()
        
    def destroy_cb(self, widget, event=None):
        gtk.main_quit()

if __name__ == '__main__':
    # Create the application
    main = MainWindow()
    
    # Start gtk main loop
    gtk.main()

