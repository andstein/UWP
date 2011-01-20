
import data


class wiki(object):
    
    def __init__(self,db):
        self.db= db
        self.openpages= {}
        
    def open(self,word):
        realname= self.db.dealiasify(word)
        if not self.openpages.has_key(realname):
            text= self.db.content()
            page= page(self, text)
            self.openpages[realname]= page
            #? page needs more information from database
            
        return self.openpages[realname]
    
    def mainword(self):
        #TODO
        return self.db.allwords[0]


class page(object):
    
    def __init__(self,wiki,word,text,aliases=None):
        self.wiki= wiki
        self.text= text
        self.word= word
        if aliases==None: aliases= list()
        self.aliases= aliases
        
        self.root= data.Root(self.text)
        self.root.parse()
        

 