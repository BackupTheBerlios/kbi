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
	
		script_name = widgetTree.get_widget("text_name")
		cat = widgetTree.get_widget("text_cat")
		text = widgetTree.get_widget("text_code")
		t = text.get_buffer()		

		# Fill Database Fields..
		
		con = sqlite.connect(os.path.expanduser("~/.kbi/db.dat"))
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

#### SHOW ALL ITENS IN DATABASE #####
def listALL(model,database):
	try:

		con = sqlite.connect(os.path.expanduser("~/.kbi/"+database))
		cur = con.cursor()

		#clear the treeview
		model.clear()

		cur.execute("select name, category from code order by category, name")
		for (n,c) in cur:
				kbi_ui.insert_item(model, None, n, c)
		
		
		con.close()
	except IOError:
		pass

#### SEARCH FOR ITEM NAME ####
def search(model, database, word):
	try:
		
	
		con = sqlite.connect(os.path.expanduser("~/.kbi/"+database))
		cur = con.cursor()

		model.clear()
		pal = word
		
		cur.execute("select name, category from code where name like:pal", locals())
		
		for (n,c) in cur:
			kbi_ui.insert_item(model, None,n,c)

		con.close()

	except IOError:
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
	

		lis=[1,2]
		lis[0]=name
		lis[1]=category
	
		return lis

	except TypeError:
		print "E: Anything Selected?!"

#### EXPORT SELECT FILE ############

def processText(dp, treeview, database):
	

	try:
		epath = kbi_conf.returnExportConf()
		
		#Let's check if Export path exists..
		if not os.path.exists(os.path.expanduser(epath)):
			os.makedirs(os.path.expanduser(epath))


		#list with selected item..
		lst = get_selected(treeview)

		con = sqlite.connect(os.path.expanduser("~/.kbi/"+database))
		cur = con.cursor()

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
def removeItem(treeview, database):
	try:
		lst = get_selected(treeview)
		con = sqlite.connect(os.path.expanduser("~/.kbi/"+database))
		cur = con.cursor()

		p = lst[0]
		cur.execute("delete from code where name=:p", locals())
		con.commit()
		#pySQL API bug?!

		#con.close()

	except TypeError:
		print "E: Anything Selected?!"


### ADD NEW CATEGORY ########
def addCat(widgetTreeCat):
	cn = widgetTreeCat.get_widget("catname")
	ce = widgetTreeCat.get_widget("catext")
	print "Adding "+cn.get_text()
	kbi_conf.setnewCat(cn.get_text(),ce.get_text())


### EXPORT DATABASE #####
def exportDB():
	import shutil, time
	try:
		day=time.strftime('%a_%d_%Y')
		filename="kib_"+day+".dat"
		shutil.copyfile(os.path.expanduser("~/.kbi/db.dat"), os.path.expanduser(kbi_conf.returnExportConf()+"/"+filename))
		return 1

	except shutil.Error:
		print "E: exportDB()"
		return -1



### CREATE a EMPTY DATABASE on FIRST-RUN #####

def firstRun():
	value=-1
	try:
		#lets check if ~/.kbi dir exists..
		if not os.path.exists(os.path.expanduser("~/.kbi/")):
			os.mkdir(os.path.expanduser("~/.kbi/"))
			value=1
		if not os.path.exists(os.path.expanduser("~/.kbi/db.dat")):
			#create database..
			con = sqlite.connect(os.path.expanduser("~/.kbi/db.dat"))
			cur = con.cursor()
			cur.executescript("""
					create table code(
      					  name,
       					  category,
						  texto);  """)
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
		
