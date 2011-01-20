
import Tkinter as tk
import tkFont


font= None

class editor(tk.Text):

    def __init__(self,win,**kwargs):
        self.page= None
        
        global font
        kwargs['font']= font
        kwargs['background']= 'white'
        kwargs['height']= 50
        kwargs['width']= 100
        tk.Text.__init__(self, win, **kwargs)

    def settext(self,text):
        self.delete('1.0', tk.END)
        self.insert('1.0', text)
        
    def setpage(self,page):
        self.page= page
        self.settext(page.text)


class tabbar(tk.Text):
    
    def __init__(self,win,**kwargs):
        self.tabs= []
        self.idx= -1
        
        global font
        kwargs['font']= font
        kwargs['background']= 'light gray'
        kwargs['height']= 1
        kwargs['state']= tk.DISABLED
        tk.Text.__init__(self, win, **kwargs)
        
        self.spacer= '  '
        self.tag_configure('active', background='dark gray' )
    
    
    def add(self,tabname):
        self.tabs += [tabname]
        line= self.get('1.0', tk.END).replace('\n','')
        line+= self.spacer + tabname
        
        self.config(state=tk.NORMAL)
        self.delete('1.0', tk.END)
        self.insert('1.0', line)
        self.config(state=tk.DISABLED)
        
        
    def active(self,idx=None):
        ret= self.idx
        
        if idx!=None:
            start= idx*len(self.spacer)
            if idx>0:
                start+= sum([x for x in self.tabs[:idx-1]]) 
            stop= start + len(self.tabs[idx])
                
            self.config(state=tk.NORMAL)
            self.tag_remove('active', '1.0', tk.END)
            self.tag_add('active', '1.%d'% (start-1), '1.%d'% (stop+1))
            self.config(state=tk.DISABLED)
        
        return ret


class statusline(tk.Text):
    
    def __init__(self,win,**kwargs):
        self.dix= {}
        
        global font
        kwargs['font']= font
        kwargs['background']= 'light gray'
        kwargs['height']= 1
        kwargs['state']= tk.DISABLED
        tk.Text.__init__(self, win, **kwargs)
        
    
    def update(self):
        self.config(state=tk.NORMAL)
        self.delete('1.0', tk.END)
        self.insert('1.0', 'statusbar')
        self.config(state=tk.DISABLED)


class mainwin(object):
    
    def __init__(self):
        self.wiki= None
        self.win= tk.Tk()
#TODO
#        self.win.wm_iconbitmap('uwp.ico')
        self.win.wm_title('uwp')
        global font
        font= tkFont.Font(self.win, family='Courier New', size=10)
         
        self.tabbar= tabbar(self.win)
        self.tabbar.pack(fill=tk.X,expand=False)
        self.text= editor(self.win)
        self.text.pack(fill=tk.BOTH,expand=True)
        self.status= statusline(self.win)
        self.status.pack(fill=tk.X,expand=False)
        
        
    def mainloop(self):
        self.win.mainloop()
        
    def load(self,wiki):
        self.wiki= wiki
        if len(welf.wiki.openpages.keys()) == 0:
            self.wiki.open(self.wiki.mainword())
        
        for page in self.wiki.openpages.keys():
            self.tabbar.add(page.word)
        
        self.tabbar.active(0)
        self.editor.setpage(self.tabbar.tabs[0])


class openwordwin(tk.Toplevel):
    
    def __init__(self,master,db):
        global font
        self.db= db
        
        tk.Toplevel.__init__(self,master)
        self.text= tk.Entry(self,width=40,font=font)
        self.text.pack()
        
        self.middle= tk.Frame(self)
        self.middle.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)
        self.list= tk.Listbox(self.middle,font=font,selectmode=tk.SINGLE)
        self.list.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        self.scroll= tk.Scrollbar(self.middle,command=self.list.yview)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        
        for widget in [self.text,self.list]:
            widget.bind('<Down>',self.next)
            widget.bind('<Up>',self.prev)
            widget.bind('<Return>',self.enter)
        self.text.bind('<Key>',self.updatelist)

        self.list.config(yscrollcommand=self.scroll)
        self.list.pack()
        self.updatelist(None)

    def next(self,event):
        self.list.event_generate('<Down>',event)
        return
        self.list.send(interp, cmd)
        sel= self.list.curselection()
        if len(sel): self.list.select_clear(sel[0])
        if len(sel): 
            if int(sel[0])+1<self.list.size(): sel= int(sel[0])+1
            else: sel= int(sel[0])
        else:
            sel= 0
        if self.list.size(): self.list.select_set(sel)
        
    def prev(self,**kargs):
        self.list.event_generate('<Up>',**kargs)
        return
        sel= self.list.curselection()
        if len(sel): self.list.select_clear(sel[0])
        if len(sel):
            if int(sel[0])>0: sel=int(sel[0])-1
            else: sel= 0
        else:
            sel= self.list.size()-1
        if self.list.size(): self.list.select_set(sel)
         
    def enter(self,event):
        sel= self.list.curselection()
        if len(sel) and sel[0]<self.list.size():
            self.choice= self.list.get(sel[0])
            self.destroy()
            
    def updatelist(self,event):
        filter= self.text.get().lower()
#        sel= self.list.curselection()
#        if len(sel): self.list.select_clear(sel[0])
        wi=li=0
        while wi<len(self.db.allwords):
            while li>0 and self.list.get(li).lower().find(filter)==-1:
                self.list.delete(li)
#                if len(sel)>0 and i<=sel[0] and sel[0]>0: sel[0]-=1
            if self.db.allwords[wi].lower().find(filter) != -1:
                while (li<self.list.size() and 
                       self.list.get(li)<self.db.allwords[wi]): li+=1
                self.list.insert(li,self.db.allwords[wi])
#                if len(sel)>0 and i<=sel[0]: sel[0]+=1
            wi+=1
#        if len(sel): self.list.select_set(sel[0])
