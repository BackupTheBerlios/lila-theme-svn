#!/usr/bin/env python

"""
	themestandard
	Print out the standard theme spec from an xml database

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
from themeconvert.utils import print_standard
from sys import argv, exit

if len(argv) != 2:
	print "themestandard - print out the standard theme spec"
	print "Copyright 2004 Daniel G. Taylor, released under the GNU GPL"
	print "Usage:"
	print "themestandard database.xml"
	print "Example:"
	print "themestandard theme-db.xml"
	exit()

xmldb_name = argv[1]

try:
	xmldb = XMLDB(xmldb_name)
except ValueError, e:
	print "Error with XML database:"
	print e
	exit()

print_standard(xmldb)
