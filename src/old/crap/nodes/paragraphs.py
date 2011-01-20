
# this file contains the nodes that will represent a paragraphs (apart from 'Container')

import data.nodes

class Paragraph(data.nodes.Container):

	def __init__(self,parent=None):
		data.nodes.Container.__init__(self,parent)
		
		# nodes.Text not in candidates because it's greedy
		self.candidates	=[nodes.Bold,nodes.Italic,nodes.InlineEquation]
		self.default	=nodes.Text

class Title(data.nodes.Node):
	pass
	
class Verbatim(data.nodes.Node):
	pass
	
class Inset(data.nodes.Node):
	pass
	
class Equation(data.nodes.Node):
	pass
	