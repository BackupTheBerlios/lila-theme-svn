#!/usr/bin/env python

"""
	utils
	Utility functions

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

def print_xmldb(xmldb, verbose = False):
	"""
	Print out an XML database's data nicely:
	Element Name
		Environment
			Action
			[Content]
	"""
	if verbose:
		for directory in xmldb.directories:
			print "Directory " + directory.name
			for path in directory.paths:
				print "  " + path.env
				if path.content:
					print "    " + path.action + ": " + path.content
				else:
					print "    " + path.action
		for icon in xmldb.icons:
			print icon.name
			for path in icon.paths:
				print "  " + path.env
				if path.content:
					print "    " + path.action + ": " + path.content
				else:
					print "    " + path.action
	else:
		print "The database contains " + str(len(xmldb.directories)) + \
		" directories and " + str(len(xmldb.icons)) + " icons."
		envs = []
		for element_list in [xmldb.directories, xmldb.icons]:
			for element in element_list:
				for path in element.paths:
					if path.env not in envs:
						envs.append(path.env)
		print "Possible environment conversion strings:"
		for env in envs: print "  " + env
