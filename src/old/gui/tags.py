
import gtk,pango

class MyTags(gtk.TextTagTable):

	def __init__(self):
	
		gtk.TextTagTable.__init__(self)
		
		normalTag= gtk.TextTag('Text')
		self.add(normalTag)
		
		boldTag= gtk.TextTag('Bold')
		boldTag.set_property('weight',pango.WEIGHT_BOLD)
		self.add(boldTag)
		
		propertyTag= gtk.TextTag('Property')
		propertyTag.set_property('weight',pango.WEIGHT_BOLD)
		propertyTag.set_property('foreground','#555')
		self.add(propertyTag)
		
		italicTag= gtk.TextTag('Italic')
		italicTag.set_property('style',pango.STYLE_ITALIC)
		self.add(italicTag)
		
		insetTag= gtk.TextTag('Inset')
		insetTag.set_property('weight',pango.WEIGHT_BOLD)
		insetTag.set_property('background','#eee')
		self.add(insetTag)
		
		equationTag= gtk.TextTag('Equation')
		equationTag.set_property('weight',pango.WEIGHT_BOLD)
		equationTag.set_property('background','#eee')
		equationTag.set_property('foreground','#707')
		self.add(equationTag)
		
		linkTag= gtk.TextTag('Link')
		linkTag.set_property('foreground','#00f')
		linkTag.set_property('underline',pango.UNDERLINE_SINGLE)
		self.add(linkTag)
		
		wordTag= gtk.TextTag('WikiWord')
		wordTag.set_property('foreground','#00f')
		wordTag.set_property('underline',pango.UNDERLINE_SINGLE)
		self.add(wordTag)
		
		titleTag= gtk.TextTag('Title')
		titleTag.set_property('size-points',18)
		titleTag.set_property('weight',pango.WEIGHT_BOLD)
		self.add(titleTag)
		
		self.taglist= []
		self.foreach(self.fillin_taglist)
		

	def fillin_taglist(self,tag,dummy):
		self.taglist.append( tag.get_property('name') )
