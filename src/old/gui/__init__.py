
try:
	import pygtk
	pygtk.require('2.0')
	import gtk,pango
	
except ImportError,e:
	try:
		import Tkintexr as tk
		w=tk.Tk()
		w.title('could not load package')
		l=tk.Label(w,text='You need to install <b>pygtk</b> to run this program.\nConsult Google !')
		l.pack()
		import sys
		b=tk.Button(w,text='Quit',command=w.destroy)
		b.pack()
		tk.mainloop()
	except ImportError,e:
		raise ImportError('\n\nYou need to install pygtk to run this program.\nConsult Google !')


from tags import MyTags
from dialogs import WordDialog
from text import WikiText,LogText

		
class MainWindow:

	def __init__(self,db,pages):
		self.window= gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect('destroy',self.destroy)

		self.db= db
		self.log= LogText()

		self.frames= []
		self.tab_labels= []
		self.notebook= gtk.Notebook()
		for page in pages:
			self.frames.append( WikiText(self,page) )
			self.frames[-1].text.show()
			self.tab_labels.append( gtk.Label(page.word) )
			self.tab_labels[-1].show()
			scrolled= gtk.ScrolledWindow()
			scrolled.add( self.frames[-1].text )
			self.notebook.append_page(scrolled,self.tab_labels[-1])
			scrolled.show()
#			self.frames[-1].test_tags()
		
		scrolled= gtk.ScrolledWindow()
		scrolled.add( self.log.text )
		self.log.text.show()
		label= gtk.Label('Log')
		label.show()
		self.notebook.append_page(scrolled,label)
		scrolled.show()
		
		self.button= gtk.Button('acme')
		self.button.connect("clicked",self.clicked,'dummy data')
		
		self.window.add(self.notebook)
		self.notebook.show()
		self.window.show()
		self.window.resize(800,600)
		#self.window.set_border_width(5)
		
		
	def clicked(self,widget,data=None):
		print 'button clicked'
		
	def destroy(self,widget,data=None):
		self.log.restore()
		gtk.main_quit()
		
	def main(self):
		gtk.main()
		
		
class TmpDB:
	def __init__(self):
		self.words= ['ene','neif','lsienf']

def dummy_cb(widget,data):
	print 'cb called; data=%s'% str(data)

#import data.db	
#db= data.db.SqliteDatabase('wiki.sli')
#win= WordDialog(db,dummy_cb)
#gtk.main()
