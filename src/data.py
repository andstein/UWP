
'''
minimalistic parser implementation

takes a linear string as input and creates an node-hierarchy that constantly
updates a tk.Text widget when new text is inserted or deleted
'''

import re,time,logging,sys
FLAGS= re.U | re.S | re.X
def brk():
	import pdb; pdb.set_trace()
import tkFont

l= logging.getLogger('data')
l.setLevel(logging.INFO)
l.addHandler(logging.StreamHandler(sys.stderr))
l.info('logger started')


#####################################################
#########    GENERAL      ###########################
#####################################################


class Node:

	'''
	outside:
		- takes ownership of the text it represents
		- need to call .parse() after creation
		- widgets can be "registered" so they get automatically updated when 
		  text is inserted
		- buffer is modified via .insert and .delete methods
	inside:
		- subclassing defines document structure
		- easy-to-use methods to create the 
	'''
	
	
	# list of compiled re-delimiters [start,end]
	# the 1st group is NOT INCLUDED (-> to exclude test for escape character)
	delimiters=[]

	def __init__(self,buffer,position,parent=None,children=None,widgets=None):
		# text contained in this node -- will be reduced to '' in non-leaves
		self.buffer= buffer
		# None for root element
		self.parent= parent
		if children==None: children= list()
		self.children= children
		# position within parent
		self.position= position
		# registered widgets to be updated
		if widgets==None: widgets= list()
		self.widgets= widgets
		
	def transform(self,nodeclass):
		newme= nodeclass( buffer=self.buffer,position=self.position,
					parent=self.parent,children=self.children,widgets=self.widgets )
		if self.parent != None:
			self.parent.replace(self,newme)
		
		return newme
		
	def replace(self,old,new):
		self.children[self.children.index(old)]= new
			
	#### infos
	
	def dump(self):
		''' dumps (recursively) to stdout '''
		text= self.root().collect(self.pos()+self.len())[self.pos():].replace('\n','\\n')
		if len(text)>30: text=text[:20]+'...'+text[-7:]
		print '%s%s (%d,%d) "%s"'% (' '*self.level(),self.__class__,self.pos(),self.len(),text)
		for child in self.children:
			child.dump()
		
	def level(self):
		if self.parent==None: return 0
		return self.parent.level() +1
	
	def collect(self,length):
		''' 
		returns 'length' characters of text contained in this node (recursively)
		''' 
		if self.buffer!=None:
			return self.buffer
		
		ret=''
		for child in self.children:
			ret+= child.collect(length-len(ret))
			if length<=len(ret): break
			
		return ret[:length]
	
	def pos(self):
		''' returns (absolute) starting position of this node '''
		if self.parent==None: return 0
		else: return self.position + self.parent.pos()

	def tkpos(self,where):
		''' returns '''
		buffer= self.root().collect(where)
		try:
			return '%d.%d'% (1+buffer.count('\n'),where-buffer.rindex('\n')-1)
		except ValueError:
			return '1.%d'% where
			
	def len(self):
		''' returns length of this node (recursively) '''
		if self.buffer != None: 
			return len(self.buffer)
			
		ret= 0
		for child in self.children:
			ret+= child.len()
		return ret
		
	def range(self):
		return [self.pos(),self.len()]
		
	def find(self,nodeclass):
		ret=[]
		for child in self.children:
			if child.__class__ == nodeclass:
				ret.append( child )
			ret+= child.find(nodeclass=nodeclass)
		return ret
		
	def root(self):
		if self.parent==None: return self
		return self.parent.root()
		
		
	#### parsing
	
	def parse(self):
		pass
	
	def extract(self,candidates):
		'''
		parses buffer and generates children according to their respective delimiters
		(first come first served; the shorter the better)
		'''
		
		parsedpos= 0
		while True:
			
			ranges=[]
			classes=[]
			for node in candidates:
				for dels in node.delimiters:
				
					mstart= dels[0].search(self.buffer[parsedpos:])
					if mstart != None:
						mend= dels[1].search(self.buffer[parsedpos+mstart.end():])
						if mend != None:
							rstart= parsedpos + mstart.start() + len(mstart.group(1))
							rstop = parsedpos + mstart.end() + mend.end()
							ranges.append([ rstart,rstop ])
							classes.append( node )
						
			if len(ranges)==0:
				break
			
			# find first (and shortest)
			best= 0
			for range in ranges:
				if ranges[best][0] > range[0]:
					best= ranges.index(range)
				elif ranges[best][0] == range[0]:
					if ranges[best][1] > range[1]: 
						best= ranges.index(range)
				
			before= self.buffer[parsedpos:ranges[best][0]]
			match = self.buffer[ranges[best][0]:ranges[best][1]]
			if len(before):
				self.children.append( Node(buffer=before,position=parsedpos,parent=self) )
			self.children.append( classes[best](buffer=match,position=ranges[best][0],parent=self) )
			
			parsedpos= ranges[best][1]
		
		if parsedpos>0:
			after= self.buffer[parsedpos:]
			if len(after):
				n= Node(buffer=after,position=parsedpos,parent=self)
				self.children.append( n )
				
			self.buffer=None
		
	#### HTML generating
	
	def html(self,opening=None,closing=None):
		''' creates html code (recursively) '''
		if opening==None: opening= '<div class="%s">'% str(self.__class__)
		if closing==None: closing= '</div>'
		ret= opening
		for child in self.children:
			ret+= child.html()
		ret+= closing
		return ret
		
	#### highlighting
		
	def register(self,widget):
		try:
			self.widgets.index(widget)
		except ValueError:
			self.widgets.append(widget)
		
	def unregister(self,widget):
		self.widgets.remove(widget)
		
	def addtag(self,widget):
		''' adds the tag for this node to the registered widgets '''
		tkstart= self.tkpos(self.pos())
		tkend  = self.tkpos(self.pos()+self.len())
		widget.tag_add( self.__class__, tkstart, tkend )
		l.debug( 'added tag %s %s-%s'% (self.__class__,tkstart,tkend) )

	def addtags(self,widget):
		''' recursively adds tags to registered widgets '''
		self.addtag(widget)
		for child in self.children:
			child.addtags(widget)
		
	# modify text
	
	def insert(self,pos,text):
		pass
		
	def delete(self,pos,length):
		pass
	

	


#####################################################
#########    WIKIDPAD     ###########################
#####################################################

class Root(Node):

	def __init__(self,buffer,position=0,parent=None,children=None,widgets=None):
		Node.__init__(self,buffer=buffer,position=position,
			parent=parent,children=children,widgets=widgets)
			
	def parse(self):
	
		ms= -time.time()*1e3
				
		# first exclude everything that may contain \n\n
		self.extract([Equation,Inset,Title])
		
		# rest must be paragraphs, then
		for child in self.children:
			if child.__class__ == Node:
				child= child.transform(Paragraph)
				for p in child.split():
					p.parse()
					
		ms+= time.time()*1e3
		l.info( 'Root parsed in %f ms' %ms )
		
		
	def html(self):
		return Node.html(self, opening='<body>', closing='</body>')
	

class Paragraph(Node):

	def __init__(self,buffer,position,parent=None,children=None,widgets=None):
		Node.__init__(self,buffer=buffer,position=position,
			parent=parent,children=children,widgets=widgets)
		
	def split(self):
		nn= re.compile('\\n\\n+',FLAGS)
		parts=[]
		
		last= 0
		match= nn.search(self.buffer[last:])
		if match==None or match.end()+last==len(self.buffer):
			return [self]

		while match != None:
		
			buffer= self.buffer[last : match.end()+last]
			position= self.position + last
			newpart= Paragraph(buffer=buffer,position=position,
						parent=self.parent,children=None,widgets=self.widgets)
			parts.append( newpart )
			
			last+= match.end()
			match= nn.search(self.buffer[last:])
		
		self.position+= last
		self.buffer= self.buffer[last:]
		idx= self.parent.children.index(self)
		
		ret= parts + [self]
		if len(self.buffer)==0:
			del self.parent.children[idx]
			ret.pop()			
		while len(parts):
			self.parent.children.insert(idx,parts.pop())
			
		return ret
		
	def parse(self):
#		import pdb; pdb.set_trace()
		self.extract([Bold,Italic,InlineEquation,Link])
		
	def html(self):
		return Node.html(self, opening='<p>', closing='</p>')



		
class Inset(Node):
	delimiters=[[re.compile('(^|[^\\\\])\\[:(?P<id>\\w+)://',FLAGS),
				 re.compile('([^\\\\])//\\]',FLAGS)]]

class Equation(Node):
	delimiters=[[re.compile('(^|[^\\\\])\\[:eqn://',FLAGS),
				 re.compile('([^\\\\])//\\]',FLAGS)],
				[re.compile('(^|[^\\\\])\\$\\$',FLAGS),
				 re.compile('([^\\\\])\\$\\$',FLAGS)]]
	def html(self):
		return Node.html(self, opening='<div class="eq">', closing='</div>')

class Title(Node):
	delimiters=[[re.compile('(^|\\n)\\+\\++',FLAGS),
				 re.compile('$|\\n',FLAGS)]]
	def html(self):
		for i in range(5):
			if self.buffer[i] != '+': break
		return Node.html(self, opening='<h%d>'%(i-1), closing='</h%d>'%(i-1))

class Bold(Node):
	delimiters=[[re.compile('(^|[^\\\\])\\*\\w',FLAGS),
				 re.compile('(\\w)\\*\\s',FLAGS)]]
	def html(self):
		return Node.html(self, opening='<b>', closing='</b>')

class Italic(Node):
	delimiters=[[re.compile('(^|[^\\\\])_\\w',FLAGS),
				 re.compile('(\\w)_\\s',FLAGS)]]
	def html(self):
		return Node.html(self, opening='<i>', closing='</i>')

class InlineEquation(Node):
	delimiters=[[re.compile('(^|[^\\\\])\\$',FLAGS),
				 re.compile('[^\\\\]\\$',FLAGS)]]
	def html(self):
		return Node.html(self, opening='<span class="eq">', closing='</span>')
	
class Link(Node):
	delimiters=[[re.compile('(^|[^\\\\])\\w+:',FLAGS),
				 re.compile('(\\s|$)',FLAGS)]]

	def html(self):
		return '<a href="%s">%s</a>'%(self.buffer,self.buffer)
	
	
