#!/usr/bin/env python

"""
	xmldb
	Read an XML database of icon name translations

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

"""
	The structure of the XMLDB is shown below:

	XMLDB
	|-directories[]
	| |-directory
	| | |-name
	| | |-paths[]
	| |   |-path
	| |     |-env
	| |     |-action
	| |     |-content
	| |-directory
	|   |-name
	|   |-paths[]
	|     |-path
	|       |-env
	|       |-action
	|       |-content
	|-icons[]
	| |-icon
	| | |-name
	| | |-paths[]
	| |   |-path
	| |     |-env
	| |     |-action
	| |     |-content
	| |-icon
	|   |-name
	|   |-paths[]
	|     |-path
	|       |-env
	|       |-action
	|       |-content
	...
"""

from xml.dom.minidom import parse

class Path:
	"""
	Holds icon path translation data
	"""
	def __init__(self, element):
		self.env = element.getAttribute("env")
		# env has no default, so make sure it's set
		if not self.env:
			raise ValueError, "Environment missing from path element!"
		# action defaults to translate
		self.action = element.hasAttribute("action") \
						and element.getAttribute("action") \
						or "translate"
		# content must be present if action is translate
		self.content = ''
		for child in element.childNodes:
			if child.nodeType == child.TEXT_NODE:
				self.content += child.data.strip()
		if self.action == "translate" and not self.content:
			raise ValueError, "Action for " + self.env + \
				" is set to translate, but no path is present!"

class XMLDBObject:
	"""
	Common class that has functions that apply to all objects
	"""
	def __init__(self, element):
		self.name = element.getAttribute("name")
		self.paths = []
		for path in element.getElementsByTagName("path"):
			# catch exceptions so we can tag on the element's name
			# to help with debugging the XML database
			try:
				self.paths.append(Path(path))
			except ValueError, e:
				raise ValueError, "Error in path for " + self.name + ". " + str(e)

class Directory(XMLDBObject):
	"""
	Directory object
	Allows an action to be performed on an entire directory
	"""
	def __init__(self, element):
		XMLDBObject.__init__(self, element)

class Icon(XMLDBObject):
	"""
	Icon object
	Allows an action to be performed on a single icon
	"""
	def __init__(self, element):
		XMLDBObject.__init__(self, element)

class XMLDB:
	"""
	Class to hold all XML database data (i.e. icon name translations)
	"""
	def __init__(self, filename = None):
		if filename:
			self.load_from_file(filename)
		else:
			# create the lists
			self.directories = []
			self.icons = []

	def _load(self, dom):
		"""
		Load our data from an XML dom object
		"""
		# reset the lists
		self.directories = []
		self.icons = []
		# load all directory objects
		for directory in dom.documentElement.getElementsByTagName("directory"):
			self.directories.append(Directory(directory))
		# load all icon objects
		for icon in dom.documentElement.getElementsByTagName("icon"):
			self.icons.append(Icon(icon))

	def load_from_file(self, filename):
		"""
		Load an XML icon name translation
		database from a file
		"""
		# parse creates a dom object tree which we
		# send to self._load to crawl for our elements
		dom = parse(filename)
		self._load(dom)
