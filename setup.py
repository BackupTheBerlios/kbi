#!/usr/bin/env python

from distutils.core import setup

setup(name='Distutils',
      version='0.1',
      description='Kbi',
      author='Luis Marques',
      author_email='Drune@gmx.net',
      url='',
      py_modules=['kbi_base', 'kbi_ui', 'kbi_conf'],
      data_files=[('/usr/share/kbi/', ['kbi.conf.template']), ('/usr/bin', ['kbi']), ('/usr/share/kbi/', ['kbi.glade'])]

)
	

	
