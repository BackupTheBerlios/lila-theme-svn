#!/usr/bin/env python

"""
	themeconvert
	Convert between desktop theme formats

	Copyright (C) 2004 Daniel G. Taylor

	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from themeconvert.xmldb import XMLDB
from themeconvert.translate import convert_xmldb_to_dict, translate_theme
from themeconvert.utils import print_xmldb, print_standard
from sys import exit

try:
	xmldb = XMLDB("theme-db.xml")
except ValueError, e:
	print "Error with XML database:"
	print e
	exit()

#print_xmldb(xmldb, True)
#print_standard(xmldb)

# gnome -> standard
print "Generating standard theme"
dict = convert_xmldb_to_dict(xmldb, "gnome", "standard", "/usr/share/icons/Lila/scalable")
translate_theme("/usr/share/icons/Lila/scalable", "./test", dict)

print "Generating GNOME theme from the standard theme"
# standard -> gnome
dict = convert_xmldb_to_dict(xmldb, "standard", "gnome", "./test")
translate_theme("./test", "./test-gnome", dict)
