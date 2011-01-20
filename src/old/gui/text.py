
do_redirect= False

import gtk,pango,sys

from tags import MyTags
from data import nodes

class WikiText:

	def __init__(self,win,page):
	
		self.win= win
		self.page= page
		self.tagtable= MyTags()
		self.buffer= gtk.TextBuffer(self.tagtable)
		self.tags= []

		self.text= gtk.TextView(self.buffer)
		self.text.set_wrap_mode(gtk.WRAP_WORD)
		self.monospace= pango.FontDescription('Courier New')
		self.text.modify_font(self.monospace)
		
		self.buffer.set_text(page.content)
		self.create_tags(page.root)
		
		self.buffer.connect( 'insert-text', self.text_inserted )
		self.buffer.connect( 'delete_range',self.range_deleted )
		self.text.connect('button_press_event',self.button_press_event)
		self.text.set_events(gtk.gdk.BUTTON_PRESS_MASK)

	def button_press_event(self,widget,event):
		if event.type==gtk.gdk._2BUTTON_PRESS:
			offset= self.buffer.get_iter_at_mark( self.buffer.get_insert() ).get_offset()
			node= self.page.root.find(offset)
			
			if node.__class__ == nodes.WikiWord:
				word= node.content_absolute(self.string())
				print 'dblclicked at WikiWord %s'% word
				self.load_word(word)
			
	def load_word(self,word):
	
		insert_iter= self.buffer.get_iter_at_mark( self.buffer.get_insert() )
		self.page.selection= [insert_iter.get_offset(),0]
	
		try:
			self.page= self.win.db.page(word)
		except Exception,e:
			print 'COULD NOT LOAD WORD : %s'% word
			return
			
		self.buffer.set_text(self.page.content)
		self.create_tags(self.page.root)
		insert_iter= self.buffer.get_iter_at_offset( self.page.selection[0] )
		
		#TODO move selection properly... scroll there, too
		self.buffer.place_cursor( insert_iter )
		self.buffer.place_cursor( self.buffer.get_iter_at_offset(0) )
		self.buffer.move_mark(self.buffer.get_insert(), self.buffer.get_iter_at_offset(0) )

	def string(self):
		return unicode( self.buffer.get_property('text') )

	def apply_tag(self,tag_name,start_offset,end_offset):
		#print 'applying tag %s from %d to %d'% (tag_name,start_offset,end_offset)
		start_iter= self.buffer.get_iter_at_offset(start_offset)
		end_iter= self.buffer.get_iter_at_offset(end_offset)
		#print '-> that is "%s"'% self.buffer.get_text(start_iter,end_iter)
		self.buffer.apply_tag_by_name(tag_name,start_iter,end_iter)
		self.tags.append( [tag_name,start_offset,end_offset] )
		
	def test_tags(self):
		for tag in self.tagtable.taglist:
			string= 'this is tag "%s"\n'% tag
			self.buffer.insert_with_tags_by_name(self.buffer.get_end_iter(),string,tag)
	
	def create_tags(self,node):
		#import pdb; pdb.set_trace()
		try:
			for child in node.children:
				self.create_tags(child)
		except AttributeError,e:
			range= list(node.pos)
			range= [node.absolute(),node.pos[1]]
			name= node.__class__.__name__
			self.apply_tag(name,range[0],sum(range))

	def delete_tags(self,node):
		range= node.absolute()
		for tag in self.tags:
			if not( tag[2]<range[0] or tag[1]>sum(range) ):
				start_iter= self.buffer.get_iter_at_offset(tag[1])
				end_iter= self.buffer.get_iter_at_offset(tag[2])
				self.buffer.remove_tag_by_name( tag[0],start_iter,end_iter )
				
	def text_inserted(self,buffer,iter,text,length):
		#print 'added "%s" at %d'% (text,iter.get_offset())
		pass
		
	def range_deleted(self,textbuffer, start, end):
		print 'deleted range from %d to %d'% (start.get_offset(),end.get_offset())

	def node_changed(self,node):
		pass
	def node_created(self,node):
		pass
	def node_deleted(self,node):
		pass

		
class wrapper:

	def __init__(self,object,cbs):
		self.object	= object
		self.cbs	= cbs
		
	def __getattr__(self,name):
		if self.cbs.has_key(name):
			return self.cbs[name]
		return self.object.__getattr__(name)
		
		
class LogText:

	def __init__(self):
		self.tagtable= MyTags()
		self.buffer= gtk.TextBuffer(self.tagtable)

		self.text= gtk.TextView(self.buffer)
		self.text.set_wrap_mode(gtk.WRAP_WORD)
		self.monospace= pango.FontDescription('Courier New')
		self.text.modify_font(self.monospace)
		
		self.stdout= sys.stdout
		if do_redirect:
			sys.stdout= wrapper(sys.stdout,{'write':self.stdout_cb})
		print 'log initialized'

	def stdout_cb(self,string):
		self.buffer.insert(self.buffer.get_end_iter(),string)
		self.stdout.write(string)
		
	def restore(self):
		sys.stdout= self.stdout

