
from data.parsers import Parser
import re

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
		