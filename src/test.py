

testtext='''++ der titel am Anfang

ein erster Paragraph
auf meheren Linien der
korrekt geparst werden sollte

[:eqn://
5*3 = 15 \\\\
//]

$$

\\sum_{n} x^n = \\frac{x
	\\ \\ \\forall |x|<1 \\
	
$$

eine erste Formel $ E=mc^2 $

etwas *fetter Text* and a img://an_image.png
'''


import data,style,gui,db,wiki,config
import Tkinter as tk,tkFont


def test_db():
	wdb= db.SqliteDatabase('wiki.sli')
	w= tk.Tk()
	od= gui.openwordwin(w,wdb)
	w.mainloop()

def test_gui():
	w= gui.mainwin()
	w.tabbar.add('one')
	w.tabbar.add('two')
	w.tabbar.add('three')
	w.tabbar.active(1)
	w.mainloop()	

def test_parse():
	n= data.Root(testtext)
	n.parse()
	n.dump()
	
	w= tk.Tk()
	s=style.TracStyle(w)
	
	t=tk.Text(w)
	t.pack()
	t.insert( 'end',testtext )
	s.setuptext(t)
	n.addtags(t)
	t.mainloop()
	
	h= style.create_html(n,s)
	f= open('test.html','w')
	f.write(h)
	import os
	os.system('firefox test.html')


def test_tk():
	w= tk.Tk()
	t= tk.Text(w)
	t.pack()

	t.tag_config( 'monospace',font=tkFont.Font(family='Courier New') )
	t.tag_config( 'red',foreground='red')
	t.tag_config( 'green',background='green')
	t.tag_config( 'bg',background='lightgray')

	t.insert( 'end','some text that will [not] be formatted' )
	t.tag_add( 'bg','1.0','end' )
	t.tag_add( 'monospace', '1.0','1.10' )
	t.tag_add( 'red', '1.5','1.9' )
	t.tag_remove( 'bg', '1.5','1.9' ) # <-- needs to be done !
	t.tag_add( 'green', '1.5','1.9' )
	t.tag_remove( 'red', '1.6','1.7' )
	
	#t.tag_remove( 'green','1.0','end' )
	
	print t.tag_ranges('bg')
	
	tk.mainloop()

	
#test_tk()
#test_parse()
#test_gui()
test_db()


