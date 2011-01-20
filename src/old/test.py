

def test_unicode():
	text= ''.join(file('test/umlaute.txt').readlines()).replace('\xfe\xff','')
	text= unicode(text[2:],errors='ignore')
	print 'len("%s")=%d'% (text,len(text))
	import sys; sys.exit(0)


	from data.nodes import Root
	from data.parser import WikidpadParser
	root= Root()
	root.parse(text,WikidpadParser())
	root.dump(text)


import gui,data

def open_word(word):
	global win
	db= data.db.SqliteDatabase('wiki.sli')
	page= db.page(word)
	#page.root.dump(page.content)
	win= gui.MainWindow(db,[page])
	win.main()

	
def test_update():
	root= data.nodes.Root()
	
execfile('reload.py')
open_word('BJTx')


