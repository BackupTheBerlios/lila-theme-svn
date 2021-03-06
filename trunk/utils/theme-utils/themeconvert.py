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
from sys import argv, exit

if len(argv) != 6:
	print "themeconvert - translate themes for other programs or environments"
	print "Copyright 2004 Daniel G. Taylor, released under the GNU GPL"
	print "Usage:"
	print "themeconvert database.xml from-theme-type to-theme-type /from/path /to/path"
	print "Example:"
	print "themeconvert theme-db.xml gnome kde /usr/share/icons/gnome/48x48 ./gnome-kde/48x48"
	exit()

xmldb_name = argv[1]
from_theme_type = argv[2]
to_theme_type = argv[3]
from_path = argv[4]
to_path = argv[5]

if from_path[-1] == '/':
	from_path = from_path[:-1]
if to_path[-1] == '/':
	to_path = to_path[:-1]

try:
	xmldb = XMLDB(xmldb_name)
except ValueError, e:
	print "Error with XML database:"
	print e
	exit()

print "Generating " + to_theme_type + " theme using " + xmldb_name
dict = convert_xmldb_to_dict(xmldb, from_theme_type, to_theme_type, from_path)
translate_theme(from_path, to_path, dict)
