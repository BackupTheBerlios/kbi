#!/usr/bin/env python 

##############################################################
# KBI_CONF.PY
# Released under GPLv2 - http://www.gnu.org/copyleft/gpl.html
# Luis "Drune" Marques - Drune@gmx.net
###############################################################

import  ConfigParser, os, sys

#CONFIGURATION FILE - Kbi.conf


def ConfigKBI():
	
	
	config = ConfigParser.ConfigParser()
	config.read(os.path.expanduser('~/.kbi/kbi.conf'))

	return config


def returnExportConf():
	c = ConfigKBI()
	return c.get("basic","export")
	
def returnAllCat():
	c = ConfigKBI()
	return c.get("categories","all")

def setnewCat(name, extension):
	try:
		
		c=ConfigKBI()
		all_cats	=returnAllCat()
		new_all_cats=all_cats+","+name+"-"+extension
		
		
		c.set("categories","all",new_all_cats)	
		f = open(os.path.expanduser('~/.kbi/kbi.conf'), "w")
		c.write(f)
		
		f.close()
		return 1
	except:
		return -1
		print "E: setnewCat()"

def getExport(widgetTree):
	fe = widgetTree.get_widget("texport")
	text_fe = fe.get_text()
	return text_fe

def SaveConfiguration(widgetTree):
	
	try:
		
		ed = getExport(widgetTree)
	
		
		ci = ConfigKBI()
		ci.set("basic","export",ed)

		fc = open(os.path.expanduser('~/.kbi/kbi.conf'), "w")
		ci.write(fc)
		fc.close()
		return 1
	except:
		return -1
		print "E: SaveConfiguration()"
