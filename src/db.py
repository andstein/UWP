import sqlite3,time,logging,sys

l= logging.getLogger('data')
l.setLevel(logging.INFO)
l.addHandler(logging.StreamHandler(sys.stderr))
l.info('logger started')


class SqliteDatabase:

	def __init__(self,fname):
	
		then= time.time()
	
		self.fname= fname
		self.db= sqlite3.connect(self.fname)
		self.cursor= self.db.cursor()

		self.words= []
		self.allwords= []
		self.props= {}
		self.cursor.execute("SELECT `word` FROM `wikiwordcontent`")
		for x in self.cursor:
			word= unicode(x[0])
			self.words.append( word )
			self.allwords.append( word )
			self.props[word]= {}
			
		self.aliases= {}
		self.cursor.execute("SELECT `word`,`key`,`value` FROM `wikiwordprops`")
		for x in self.cursor:
			word = unicode(x[0])
			key  = unicode(x[1])
			value= unicode(x[2])
			self.props[word][key]= value
			if key == 'alias':
				self.aliases[value]= word
				self.allwords.append( value )
			
		self.allwords.sort()
		
		now= time.time()
		ms= int(1e3*(now-then))
		l.info('%s : %d words loaded in %sms'% (self.__class__.__name__,len(self.words),ms))
		
		
	def dealiasify(self,word):
		if self.aliases.has_key(word):
			word= self.aliases[word]
		return word
		
	def content(self,word):
		word= self.dealiasify(word)
					
		t= (word,)
		self.cursor.execute("SELECT `content` FROM `wikiwordcontent` WHERE `word`=?",t)
		return unicode(self.cursor.next()[0])
		
	def store(self,word,content):
		pass



def SqliteDatabaseCreate(fname):
	import db_structure
	
	db= sqlite3.connect(fname)
	cursor= db.cursor()
	
	for tablename in ['wikiwordcontent','wikiwordprops','wikirelations']:
		cmd= 'CREATE TABLE `%s` ( '% tablename
		for prop in db_structure.TABLE_DEFINITIONS[tablename]:
			cmd+= '%s %s, '% (prop[0],prop[1])
		cmd= cmd[:-2]
		cmd+= ')'
		print '### ' + cmd
		cursor.execute(cmd)

	db.close()
