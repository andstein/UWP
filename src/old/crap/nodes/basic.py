# this file provides the "basic" node classes

#import data.nodes as nodes
from paragraphs import Paragraph,Title,Verbatim,Inset,Equation
from text import Text,Bold,Italic,InlineEquation


class Node:

	def __init__(self,parent=None):
		self.parent= parent
		
		self.pos=[0,0]		# relative to parent
		self.content=[0,0]	# relative to pos


	def parse(self,string,parser):
		'''
		parses the string using 'parser' and sets properties accordingly
		raises exception if string does not conform entirely 
		'''
		self.pos= parser.findNext( self.__class__,string )
		
		if self.pos[0] != 0:
			raise ParseException("cannot parse %s : garbage characters at beginning of '%s'" %(str(self),string))
		if self.pos[1] != len(string):
			raise ParseException("cannot parse %s : garbage characters at end of '%s'" %(str(self),string))

		self.pos    = [0,len(string)]
		self.content= list(self.pos)
		
	def absolute(self):
		ret= self.pos[0]
		if self.parent != None:
			ret+= self.parent.absolute()
		return ret

	def dump(self,string=None,prefix=''):
		if string==None:
			text=''
		else:
			pos= self.absolute()
			text= ': ' + string[pos:pos+self.pos[1]]
		print '%s%s %s'% (prefix,str(self),text)
		
	def process(self):
		''' gets called after parsing '''
		pass

	def __str__(self):
		return '<|%s|%d-%d>'% (self.__class__.__name__,self.pos[0],self.pos[1])
		
	#### dynamic
	
	def replace(self,string,offset,length):
		pass
		
		
class Container(Node):

	def __init__(self,parent=None):
		Node.__init__(self,parent)
		
		self.children=[]
		self.candidates=[]		# possible child-nodes
		self.default=None		# default  child-node
		

	def parse(self,string,parser):
		'''
		parses the string recursively
		'''
		
		ranges=dict(zip( self.candidates,[None for i in range(len(self.candidates))] ))
		pos= 0
		
		while pos<len(string):
			
			# update list of next matches
			for node in self.candidates:
				if ranges[node]==None or ranges[node][0] < pos:
					r= ranges[node]= parser.findNext(node,string[pos:])
					if r!=None: r[0]+=pos
					
					if do_debug and r!=None:
						print "<< found %s at %d-%d ('%s') >>"% (node.__name__,r[0],r[1],string[r[0]:sum(r)])
			
			# choose best next match
			best= None
			for node in self.candidates:
				if ranges[node] == None:
					continue
				if best==None or ranges[node][0] < ranges[best][0]:
					# chose _first_ lowest occurence
					# -> latter candidates act like fall-back defaults
					best= node

			#import pdb; pdb.set_trace()
			if best==None:
				break
					
			# evtl create default element(s) before
			while pos < ranges[best][0]:
				r= parser.findNext( self.default,string[pos:ranges[best][0]] )
				r[0]+= pos
				
				if r==None or r[0]!=pos:
					raise ParseException('could not fill (%d-%d) with %s (default-element); r=%s'% \
										(pos,ranges[best][0],str(self.default),str(r)))

				node= self.default(self)
				node.parse( string[r[0]:sum(r)],parser  )
				node.pos[0] += r[0]
				self.children.append(node)
				pos+= r[1]
				
			# create found element
			node= best(self)
			node.parse( string[ranges[best][0]:sum(ranges[best])],parser )
			node.pos[0] += ranges[best][0]
			self.children.append(node)
			
			# update index
			pos= sum( ranges[best] )

		# create default element with the rest
		if pos<len(string):
			node= self.default(self)
			node.parse( string[pos:],parser )
			node.pos[0] += pos
			self.children.append(node)
			
			
	def dump(self,string=None,prefix=''):
		Node.dump(self,string,prefix)
		
		for child in self.children:
			child.dump(string,prefix + ' ')

			
class Root(Container):

	def __init__(self):
		#import pdb; pdb.set_trace()
		Container.__init__(self,None)
		self.candidates= (Title,Inset,Verbatim,Equation)#,Paragraph)
		self.default= Paragraph
		

		
