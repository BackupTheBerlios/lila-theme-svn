#!/usr/bin/env python

"""
	translate
	Translate icon themes using an XML translation database

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

def convert_xmldb_to_dict(xmldb, from_theme_type, to_theme_type):
	"""
	This function returns a dictionary object of mappings from
	the icon names of the from_theme_type to the to_theme_type
	i.e. if "gnome" and "kde" are passed, it returns:
	{ ..., "devices/gnome-dev-floppy" : ["devices/3floppy_mount"],
		   "mimetypes/gnome-mime-text" : ["mimetypes/text"],
		   "devices/gnome-dev-printer" : ["devices/printer", 
		   "devices/printer1", "devices/print_printer"], ... }
	Note that the keys are strings while the values are lists
	this is to accomidate multiple paths to translate to
	When there are multiple paths to translate from, only the first
	is used in the key
	"""
	translation_dict = {}
	# for all directories and icons
	for objects in [xmldb.directories, xmldb.icons]:
		for object in objects:
			# reset the key and value
			key, value = None, []
			# if we are translating from/to the standard, set it
			if from_theme_type == "standard":
				key = object.name.split(",")[0]
			if to_theme_type == "standard":
				for name in object.name.split(","):
					value.append(name)
			# check each path for our theme names
			for path in object.paths:
				# if it's from, we set the dict key
				if path.env == from_theme_type:
					if path.action == "copy":
						key = object.name.split(",")[0]
					else:
						key = path.content.split(",")[0]
				# if it's to, we set the dict value
				if path.env == to_theme_type:
					if path.action == "copy":
						for name in object.name.split(","):
							value.append(name)
					else:
						for name in path.content.split(","):
							value.append(name)
			# if we found both a matching key and value above, save it into the dict
			if key and value:
				translation_dict[key] = value
	# return the dict
	return translation_dict

def translate_theme(from_base_path, to_base_path, translation_dict):
	"""
	Translate theme from from_base_path into to_base_path using
	the translation_dict.
	Icon name suffixes will be directly copied with the files, so
	directory.icon would copy over to gnome-dev-directory.icon. The
	same goes for PNG and SVG images.
	"""
	# here is the basic idea, although it needs to be done recursively:
	# for each dir in from_base_path
		# if the dir name is in translation_dict.keys()
			# translate all the icons using the dir names
		# else
			# for each file in the directory
				# cut off the from_base_path and suffix:
				# /base/devices/cdrom.svg -> devices/cdrom
				# if value from above is in translation_dict.keys()
					# translate icon name, add suffix and save
