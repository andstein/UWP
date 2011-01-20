
import nodes
import re

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
		name= node.__name__
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
			
		m= r.search(string[pos:])
		if m==None: return None
		
		string= string[m.start():m.end()]
		pos = string.index(m.group(1))
		cont= string.index(m.group(2))
		
		return [m.start() + pos ,len(m.group(1))]

		
class WikidpadParser(Parser):

	def __init__(self):
		Parser.__init__(self)
		
		flags= re.U | re.S | re.X
		
		# paragraphs
#		self.ParagraphRE 	= re.compile( '^((.*?\\n\\s*\\n[\\n\\s]*))' ,flags)
		self.ParagraphRE 	= re.compile( '((.+?(?:$|\\n\\s*\\n)))' ,flags)
		self.TitleRE		= re.compile( '(?:^|\\n)(\\++\\s+(.*?)\\n)' ,flags)
		self.PropertyRE  	= re.compile( '(?:^|\\n)(\\s*\\[\\s*(?P<name>\w+)\\s*:\\s*(?P<value>\w+)\\s*\\])' ,flags)
		self.InsetRE		= re.compile( '(?:^|[^\\\\])(\\[:(?P<id>\\w+)://(.*?)//\\])' ,flags)
		self.EquationRE		= re.compile( '(?:^|[^\\\\])(\\$\\$(.*?)\\$\\$)' ,flags)
		self.VerbatimRE		= re.compile( '(?:^|[^\\\\])(\\<\\<pre(.*?)\\>\\>)' ,flags)
		
		# in-paragraphs
		self.TextRE			= re.compile( '((.*))' ,flags)
		self.BoldRE			= re.compile( '(?:^|\\s)(\*(\\S.*?[^\\s\\\\])\*)' ,flags)
		self.ItalicRE		= re.compile( '(?:^|\\s)(_(\\S.*?[^\\s\\\\])_)' ,flags)
		self.InlineEquationRE=re.compile( '(?:^|[^\\\\$])(\\$(.*?)\\$)' ,flags)
		self.WikiWordRE		= re.compile( '(([A-Z]+[a-z]+[A-Z]+[a-z]*))' ,flags)
		self.LinkRE			= re.compile( '((\w+://\S+))' ,flags)
		
		# lists
		self.BulletListRE	= re.compile( '(?:^|\\n)((\\s+\*.*?))(?:$|\\n\\s*[^\\\\*])' ,flags)
		self.BulletItemRE	= re.compile( '^((?P<spaces>\\s+)\\*(.*?)\\n)' ,flags)

	
	
	def test(self):
		textf= file('test/wikidpad.txt')
		text=  ''.join( textf.readlines() )

		parser= parsers.WikidpadParser()

		#import pdb; pdb.set_trace()

		root= nodes.Root()
		root.parse( text,parser )
		root.dump(text)
		