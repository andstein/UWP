
import gtk

class WordDialog:

	def __init__(self,db,cb,title='Open WikiWord'):
		'''
		shows a window to choose a WikiWord from a database
		
		cb should accept (widget,word) as parameters in case 'Ok' was chosen
		'''
	
		self.db= db
		self.cb= cb
		self.window= gtk.Window( gtk.WINDOW_TOPLEVEL )
		
		self.vbox= gtk.VBox(False,0)
		
		self.entry= gtk.Entry()
		self.vbox.pack_start(self.entry,False,False,0)
		self.entry.show()
		
		self.store= gtk.ListStore(str)		
		self.scrolled= gtk.ScrolledWindow()
		self.list= gtk.TreeView(model=self.store)
		self.scrolled.add(self.list)
		self.list.set_size_request(200,300)
		self.list.show()
		self.column= gtk.TreeViewColumn('WikiWord')
		self.list.append_column(self.column)
		self.cell= gtk.CellRendererText()
		self.column.pack_start(self.cell,True)
		self.column.add_attribute(self.cell,'text',0)
		self.vbox.pack_start(self.scrolled,True,True,0)
		self.scrolled.show()
		
		self.hbox= gtk.HBox(False,10)
		self.ok= gtk.Button('Ok')
		self.hbox.pack_start(self.ok,True,False,0)
		self.ok.show()
		self.cancel= gtk.Button('Cancel')
		self.hbox.pack_start(self.cancel,True,False,0)
		self.cancel.show()
		self.vbox.pack_start(self.hbox,False,False,10)
		
		self.hbox.show()
		self.window.add(self.vbox)
		self.vbox.show()
		self.window.show()
		
		self.window.connect('destroy',self.destroy)
		self.entry.connect('changed',self.entry_changed)
		self.entry.connect('key_release_event',self.key_released)
		self.list.connect('key_release_event',self.key_released)
		
	def destroy(self,widget,data=None):
		gtk.main_quit()
		
	def update(self):
		self.store.clear()
		filters= self.entry.get_text().split(' ')
		
		for word in self.db.allwords:
			try:
				for filter in filters:
					word.lower().index(filter.lower())
				self.store.append([word])
			except ValueError,e:
				pass
				
			if len(self.store)>100:
				break
				
	def entry_changed(self,widget,data=None):
		self.update()
		
	def key_released(self,widget,event,data=None):
		key= gtk.gdk.keyval_name(event.keyval)
		
		(model,iter)= self.list.get_selection().get_selected()
		if iter!=None:
			word= model[iter][0]
		
		if key == 'Return' and widget==self.list:
			self.window.destroy()
			self.cb(self.list,word)
		if key == 'Escape':
			self.window.destroy()

