#!/usr/bin/env python

"""
	Scripts
	Helper classes/functions for SVG scripts

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

from os import walk, makedirs, sep
from os.path import join, exists, isfile, isdir
from sys import exit

def dummy(path, save_path):
	"""
	Example function for SVGScript
	"""
	print path + " -> " + save_path

class SVGScript:
	"""
	A class to handle calling a function on every SVG file found
	given a path to search and function to call
	"""
	def __init__(self, path = None, function = dummy, save_path = None):
		self.path = path
		self.function = function
		self.save_path = save_path
		self.filters = ["svg"]

	def run(self):
		"""
		Run this script!
		"""
		if self.path[-1] != sep:
			self.path += sep

		if self.save_path and self.save_path[-1] != sep:
			self.save_path += sep
		else:
			self.save_path = self.path

		if isfile(self.path):
			pass
		elif isdir(self.path):
			for root, dirs, files in walk(self.path):
				relative_root = root[len(self.path):]
				print "Scanning " + root
				for file in files:
					for filter in self.filters:
						if file[-len(filter):] == filter:
							try:
								save_path = join(self.save_path, relative_root)
								if not exists(save_path):
									makedirs(save_path)
								try:
									self.function(join(root, file), join(save_path, file))
								except:
									print "Error with " + join(root, file) + ", continuing..."
							except IOError, err:
								print "Skipping " + join(root, file) + ", check permissions!"
		else:
			raise AttributeError, self.path + " is neither a file or directory!"
