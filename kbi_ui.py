#!/usr/bin/env python 

##############################################################
# KBI_UI.PY
# Released under GPLv2 - http://www.gnu.org/copyleft/gpl.html
# Luis "Drune" Marques - Drune@gmx.net
###############################################################
import gtk

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


### INSET ITEM in TREEVIEW #####
def insert_item(model,parent,firstcolumn,secondcolumn):
    myiter=model.insert_after(parent,None)
    model.set_value(myiter,0,firstcolumn)
    model.set_value(myiter,1,secondcolumn)
    
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
