

from data import *
import tkFont

def create_html(root,style):
    ret= '<html><head><style type="text/css">'
    ret+= style.stylesheet()
    ret+= '</style></head>'
    ret+= root.html()
    ret+= '</html>'
    return ret

class GenericStyle(object):
    
    def __init__(self):
        self.ff= None
        self.css= []
        self.tags= []
        
    def setuptext(self,text):
        text.config(font=tkFont.Font(text,family=self.ff))
        for tag in self.tags:
            text.tag_config(**tag)
        
    def stylesheet(self):
        ret=''
        for style in self.css:
            ret+= '%s { %s } \n'% (style[0],style[1])
        return ret
    

class TracStyle(GenericStyle):
    
    def __init__(self,win):
        self.ff='Courier New'
        self.css=[['body','font-family:Courier New;'],
                  ]
        self.tags=[{'tagName':Inset,'background':'lightgray'},
                   {'tagName':Equation,'background':'lightgray','foreground':'red'},
                   {'tagName':Link,'foreground':'blue','underline':True},
                   {'tagName':Title,'underline':True,\
                    'font':tkFont.Font(win,family=self.ff,size=14,weight=tkFont.BOLD)},
                   ]