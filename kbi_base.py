#!/usr/bin/env python 

##############################################################
# KBI_BASE.PY
# Released under GPLv2 - http://www.gnu.org/copyleft/gpl.html
# Luis "Drune" Marques - Drune@gmx.net
###############################################################
import os, sys, gtk, kbi_ui, kbi_conf
from pysqlite2 import dbapi2 as sqlite

### SAVE DATABASE CHANGES ###
def saveDataBase(widgetTree):
	try:
		#get widgets..
		db_name=widgetTree.get_widget("data_combo")
		script_name = widgetTree.get_widget("text_name")
		cat = widgetTree.get_widget("text_cat")
		text = widgetTree.get_widget("text_code")
		t = text.get_buffer()		

		# Fill Database Fields..
		
		database=db_name.get_active_text()
		con = sqlite.connect(os.path.expanduser("~/.kbi/databases/"+database))
		cur = con.cursor()

		all_code = t.get_text(t.get_start_iter(), t.get_end_iter())
		selected_text_cb = kbi_ui.get_active_text(cat)
	
		ins = (script_name.get_text(),selected_text_cb,all_code)
		cur.execute("insert into code (name, category, texto) values ( ?, ?, ?)" ,ins)
		con.commit()
		return 1

		#bug?!
		con.close()
		
	except IOError : 
		
		print "E: saveDataBase()"
		return -1

### RETURN ALL DATABASES AVAILABLE ###
def returnDBs(widgetTree):
	try:
		import glob
		a=glob.glob(os.path.expanduser("~/.kbi/databases/*.dat"))
		dat = widgetTree.get_widget("data_combo")
		model = dat.get_model()
		model.clear()
		for x in a:
			dat.append_text(os.path.basename(x))
		
		#set active item for default 
		dat.set_active(0)
	except:
		print "E: returnDBs()"

#### SHOW ALL ITENS IN DATABASE #####
def listALL(model):
	try:
		model.clear()
		for i in os.listdir(os.path.expanduser("~/.kbi/databases/")):
			if i.endswith(".dat"):	
				com = sqlite.connect(os.path.expanduser("~/.kbi/databases/"+i))
				cur = com.cursor()
				cur.execute("select name, category from code order by category, name")
				for (n,c) in cur:
					kbi_ui.insert_item(model, None, n,c,i)
				com.close()
	
	except IOError:
		print "E: listALL()"




		        
		        
	

#### SEARCH FOR ITEM NAME ####
def search(model, word):
	try:
			model.clear()
			for i in os.listdir(os.path.expanduser("~/.kbi/databases/")):
				if i.endswith(".dat"):
					print "Searching: "+i
					con = sqlite.connect(os.path.expanduser("~/.kbi/databases/"+i))
					cur = con.cursor()
		
					cur.execute("select name, category from code where name like:word", locals())
		
					for (n,c) in cur:
						
						kbi_ui.insert_item(model, None,n,c, i)

					
					con.close()

	except IOError:
		print "E: search()"
		sys.exit(-1)


# get selected item
def get_selected(treeview):
	try:
		#there's a simple way to get the selected ITEM?
		selected=treeview.get_selection()
		#set selected to single SELECTION:
		selected.set_mode(gtk.SELECTION_SINGLE)
	
		(model, itera) = selected.get_selected()
	

		name=model.get_value(itera, 0)
		category=model.get_value(itera, 1)
		dataname=model.get_value(itera,2)
	

		lis=[1,2,3]
		lis[0]=name
		lis[1]=category
		lis[2]=dataname
	
		return lis

	except TypeError:
		print "E: Anything Selected?!"

#### EXPORT SELECT FILE ############

def processText(dp, treeview):
	

	try:

		#lst [0] - filename
		#lst [1] - extension
		#lst [2] - database name


		epath = kbi_conf.returnExportConf()
		
		#Let's check if Export path exists..
		if not os.path.exists(os.path.expanduser(epath)):
			os.makedirs(os.path.expanduser(epath))


		#list with selected item..
		lst = get_selected(treeview)

		for i in os.listdir(os.path.expanduser("~/.kbi/databases/")):
				if i.endswith(".dat"):
					
					#lst[2] - database name
					con = sqlite.connect(os.path.expanduser("~/.kbi/databases/"+lst[2]))
					cur = con.cursor()

					# p - filename

					p = lst[0]
					cur.execute("select name, category, texto from code where name=:p", locals())
	
							
					path = os.path.expanduser(epath+"/"+lst[0]+"."+dp[lst[1]])
					f3 = open (path, "w")

					for (n,c,t) in cur:
						f3.write(t)
	
					f3.close()
		
					con.close()
					
					
					
		return 1
		
	except IOError:
		print "I/O error.."
		return -1
	except TypeError:
		print "E: Anything Selected?!"

### REMOVE A ITEM #########
def removeItem(treeview):
	try:
		lst = get_selected(treeview)
		con = sqlite.connect(os.path.expanduser("~/.kbi/databases/"+lst[2]))
		cur = con.cursor()

		p = lst[0]
		cur.execute("delete from code where name=:p", locals())
		con.commit()
		#pySQL API bug?!

		#con.close()

	except TypeError:
		print "E: Anything Selected?!"




### EXPORT DATABASE #####
def exportDB(widgetTree):
	import shutil
	try:
		db = widgetTree.get_widget("data_combo")
		db_name=db.get_active_text()
		
		shutil.copyfile(os.path.expanduser("~/.kbi/databases/"+db_name), os.path.expanduser(kbi_conf.returnExportConf()+"/"+db_name))
		return 1

	except shutil.Error:
		print "E: exportDB()"
		return -1

#############################################
### CREATE A EMPTY DATABASE (MENU OPTION) ###
#############################################

def newDatabase(widgetTree):
	wnd = gtk.glade.XML("/usr/share/kbi/kbi.glade", "newDatabase")
	f = wnd.get_widget("newDatabase")
	text = wnd.get_widget("text_newdb")
	
	new = f.run()

	if new == gtk.RESPONSE_OK:
		if text.get_text() != "":

			if text.get_text().endswith(".dat"):
				createDatabase(text.get_text())
			else:
				createDatabase(text.get_text()+".dat")


			kbi_ui.message("Kbi: Empty database created in ~/.kbi/databases",f)	
			#update available databases in combo box
			returnDBs(widgetTree)
			f.destroy()		
			
		else:
			kbi_ui.error("Input a valid name in box", f)

	else:
		f.destroy()
	
	
	
##############################################
### CREATE a EMPTY DATABASE 			 #####
#############################################


def createDatabase(database):
	con = sqlite.connect(os.path.expanduser("~/.kbi/databases/"+database))
	cur = con.cursor()
	cur.executescript("""
					create table code(
      					  name,
       					  category,
						  texto);  """)



#####################################3
## ADD NEW CATEGORY 				###
#####################################
def getAllCats(widgetTree):
	cat = widgetTree.get_widget("text_cat")
	mo=cat.get_model()
	mo.clear()
	all = kbi_conf.returnAllCat()
	
	
	for i in all.split(" "):
		x=i.split(",")
	for j in x:
		r=j.split("-")
		cat.append_text(r[0])
		
	cat.set_active(0)


def addCatUI(widgetTree):

	widgetTreeCat = gtk.glade.XML("/usr/share/kbi/kbi.glade", "wnewCat")
	# window - categorie
	wcat = widgetTreeCat.get_widget("wnewCat")
	# name / extension
	cn = widgetTreeCat.get_widget("catname")
	ce = widgetTreeCat.get_widget("catext")
	
	
	


	r= wcat.run()
	if r == gtk.RESPONSE_OK:
		# save in kbi.conf
		kbi_conf.setnewCat(cn.get_text(),ce.get_text())
		print "Category Saved.."
		getAllCats(widgetTree)
		#addNewCat(obj)
		kbi_ui.message("Kbi: Category Saved!", wcat)
	wcat.hide()



###########################################
### FIRST RUN 						######
###########################################

def firstRun():
	value=-1
	try:
		#lets check if ~/.kbi dir exists..
		if not os.path.exists(os.path.expanduser("~/.kbi/")):
			os.makedirs(os.path.expanduser("~/.kbi/databases"))
			value=1
		if not os.path.exists(os.path.expanduser("~/.kbi/databases/db.dat")):
			createDatabase("db.dat")
			value=1
		#Copy configuration file to homedir
		if not os.path.exists(os.path.expanduser("~/.kbi/kbi.conf")):
			import shutil
			shutil.copyfile("/usr/share/kbi/kbi.conf.template",os.path.expanduser("~/.kbi/kbi.conf"))
			value=1
		
		else:
			pass

		return value
	except IOError:
		print "E: I/O firstRun() error.."
		value=-1
		return value
		
