
from parsers import *

import nodes

class Parser:

	def __init__(self):
		# how to define patterns:
		# self.NodeRE = re.compile( ... )
		# use following groups
		#   - group1= actual match (often equals whole regexp; you might want to exclude delimiters and such)
		#   - group2= content of match
		#   - named groups are node-type-specific
		pass
		

	def findRE(self,node):
		'''
		return self.NodeRE -- raises ParseException if not defined
		'''
		name= node.__class__.__name__
		try:
			return eval( 'self.' + name + 'RE' )
		except AttributeError,e:
			raise ParseException(str(self) + " does not support node-type " + name)

			
	def findNext(self,node,string,pos=0):
		'''
		to get next range for a given node
		
		returns [begin,length] relative to string
		returns None if there was no match
		'''
		r= self.findRE(node)
			
		m= r.searcH(string[pos:])
		if m==None: return None,None
		
		string= string[m.start(),m.end()]
		pos = string.index(m.group(1))
		cont= string.index(m.group(2))
		
		return [m.start() + pos ,len(m.group(1))]
