#!/usr/bin/env python 

##############################################################
# KBI_UI.PY
# Released under GPLv2 - http://www.gnu.org/copyleft/gpl.html
# Luis "Drune" Marques - Drune@gmx.net
###############################################################
import gtk, os, kbi_conf

## SHOW TREEVIEWS FIELDS #####
def show_col(tree, wTree, tree_mod):	
	
 tree.set_model(tree_mod)
# 1 - Name of the program..
 renderer=gtk.CellRendererText()
 column=gtk.TreeViewColumn("Piece Name",renderer, text=0)
 tree.append_column(column)
#2 - Category of Code

 renderer=gtk.CellRendererText()
 column=gtk.TreeViewColumn("Category",renderer, text=1)
 tree.append_column(column)

#3 - Source Database
 renderer=gtk.CellRendererText()
 column=gtk.TreeViewColumn("Database",renderer, text=2)
 tree.append_column(column)
	

### INSET ITEM in TREEVIEW #####
def insert_item(model,parent,firstcolumn,secondcolumn,third):
    myiter=model.insert_after(parent,None)
    model.set_value(myiter,0,firstcolumn)
    model.set_value(myiter,1,secondcolumn)
    model.set_value(myiter,2,third)
    return myiter


### GET ACTIVE COMBO-BOX TEXT ####

def get_active_text(combobox):
      model = combobox.get_model()
      active = combobox.get_active()
      if active < 0:
          return None
      return model[active][0]

### INFO MESSAGE ###
def message(message, window):
	msg=gtk.MessageDialog(parent=window, flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE, message_format=message)
	msg.run()
	msg.destroy()

### ERROR MESSAGE ###

def error(message, window):
	msg=gtk.MessageDialog(parent=window, flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format=message)
	msg.run()
	msg.destroy()

#######################
### EXPORT DATABASE ###
#######################

def saveDialog(widgetTree, windows_title):
	try:
		import shutil
		chooser = gtk.FileChooserDialog(title=windows_title,action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))

		r = chooser.run()
		#name of file to export
		name = chooser.get_filename()
		db = widgetTree.get_widget("data_combo")
		db_name=db.get_active_text()
	
		if r == gtk.RESPONSE_OK:
			shutil.copy(os.path.expanduser("~/.kbi/databases/"+db_name), chooser.get_filename())
			message("Kbi: Database Exported to: "+chooser.get_filename())
	
		chooser.destroy()
	except:
		print "E: saveDialog()"

#########################
### IMPORT DATABASE #####
#########################


def ImportDialog(widgetTree, windows_title):
	try:
		import shutil
		chooser = gtk.FileChooserDialog(title=windows_title,action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))

		r = chooser.run()
	#name of file to export
	
	
		if r == gtk.RESPONSE_OK:
			name = chooser.get_filename()
	
			db_name = os.path.basename(chooser.get_filename())
			if db_name.endswith(".dat"):
				shutil.copy(chooser.get_filename(), os.path.expanduser("~/.kbi/databases/"+db_name))
			else:
				shutil.copy(chooser.get_filename(), os.path.expanduser("~/.kbi/databases/"+db_name+".dat"))
		
		chooser.destroy()
	except:
		print "E: ImportDialog()"

#################################
### CHANGE EXPORT FILE PATH ####
################################

def changeExportPath():
	try:

		epath = kbi_conf.returnExportConf()

		chooser = gtk.FileChooserDialog(title="Change Export Path",action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		e = chooser.run()
		if e == gtk.RESPONSE_OK:
			chooser.hide()
			return chooser.get_filename()
		else:
			chooser.hide()
			return epath

		chooser.destroy()
	except:
		print "E: changeExportPath()"

### ABOUT WINDOW ###
def about(obj):
	widgetTreeAbout = gtk.glade.XML("/usr/share/kbi/kbi.glade", "about")
	abou = widgetTreeAbout.get_widget("about")
	abou.run()
	abou.destroy()





