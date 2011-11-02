import pygtk
pygtk.require('2.0')
import gtk
import gobject
from semanticxo.datawrapper import DataWrapper

class MetadataPanel(object):
    '''
    This panel shows a table of property / value
    '''
    def __init__(self):
        # Create the model
        self._model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        
        # Create the widget
        treeview = gtk.TreeView(self._model)
        column_p = gtk.TreeViewColumn('Property')
        cell_p = gtk.CellRendererText()
        column_p.pack_start(cell_p, True)
        column_p.set_attributes(cell_p, text=0)
        column_p.set_sort_column_id(0)
        treeview.append_column(column_p)
        column_o = gtk.TreeViewColumn('Value')
        cell_o = gtk.CellRendererText()
        column_o.pack_start(cell_o, True)
        column_o.set_attributes(cell_o, text=1)
        treeview.append_column(column_o)
        self._widget = treeview
        
    def get_model(self):
        return self._model
    
    def get_widget(self):
        return self._widget
     

class JournalPanel(object):
    '''
    This panel is used to select the content of a journal
    '''
    def __init__(self, metadata_panel):
        # The table to select an object
        model_resources = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        treeview = gtk.TreeView(model_resources)
        column = gtk.TreeViewColumn('Object')
        cell_object = gtk.CellRendererText()
        column.pack_start(cell_object, True)
        column.set_attributes(cell_object, text=0)
        column.set_sort_column_id(0)
        treeview.append_column(column)
        treeview.connect("cursor-changed", self._change_object_cb, metadata_panel)
        
        # The combo box to select a source
        model_sources = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        model_sources.append(['My XO','localhost'])
        combobox = gtk.ComboBox(model_sources)
        cell_source = gtk.CellRendererText()
        combobox.pack_start(cell_source, True)
        combobox.add_attribute(cell_source, 'text', 0)
        combobox.connect("changed", self._change_source_cb, treeview)
        
        # Create the widget
        data_source_xo = gtk.VBox()
        data_source_xo.pack_start(gtk.Label("Select a Journal"), False, False, 5)
        data_source_xo.pack_start(combobox, False, False, 5)
        data_source_xo.pack_start(treeview, True, True, 5)
        self._widget = data_source_xo
        
    def _change_source_cb(self, combobox, treeview):
        '''
        Called when a new data source is selected
        '''
        # Get the new host
        host = combobox.get_model()[combobox.get_active()][1]
        
        # Clear the content of the resources
        treeview.get_model().clear()
        
        # Get the new content from the data API
        self._wrapper = DataWrapper(store=host)
        instances = self._wrapper.get_datastore_instances()
        for instance in instances:
            treeview.get_model().append([instance['title'],instance['uid']])
            
    
    def _change_object_cb(self, treeview, metadata_panel):
        '''
        Called when a new object is selected
        '''
        # Get the selected id
        selected_row = treeview.get_selection().get_selected_rows()[1][0][0]
        selected_id = treeview.get_model()[selected_row][1]
        
        # Clear the previous metadata
        metadata_panel.get_model().clear()
        
        # Put the new data in place
        metadata = self._wrapper.get_datastore_instance(selected_id)
        for (key,value) in metadata.iteritems():
            metadata_panel.get_model().append([key,value])
            
    def get_widget(self):
        return self._widget
     
    