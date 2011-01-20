
#import gui
#dreload(gui,exclude=['pygtk','gtk'])

list=[
	'config',
	'gui','gui.dialogs','gui.tags','gui.text',
	'data','data.db','data.nodes','data.parser',
]
	
for p in list:
	print '%s...'%p,
	exec('import ' + p)
	exec('reload(%s)'% p)
	print 'ok'
