#!/usr/bin/env python

"""
	translate
	Translate icon themes using an XML translation database

	Copyright (C) 2004 Daniel G. Taylor and Chromakode

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

import os, os.path
import shutil

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

def copy_dir(src, dst, symlinks=False):
	"""
	Recursively copy a directory tree using copy2().

	Based on shutil.copytree()

	If the optional symlinks flag is true, symbolic links in the
	source tree result in symbolic links in the destination tree; if
	it is false, the contents of the files pointed to by symbolic
	links are copied.
	"""
	names = os.listdir(src)
	if not os.path.isdir(dst):
		os.mkdir(dst)
	for name in names:
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		if symlinks and os.path.islink(srcname):
			linkto = os.readlink(srcname)
			os.symlink(linkto, dstname)
		elif os.path.isdir(srcname):
			copytree(srcname, dstname, symlinks)
		else:
			shutil.copy2(srcname, dstname)

def translate_theme(from_base_path, to_base_path, translation_dict):
	"""
	Translate theme from from_base_path into to_base_path using
	the translation_dict.
	Icon name suffixes will be directly copied with the files, so
	directory.icon would copy over to gnome-dev-directory.icon. The
	same goes for PNG and SVG images.
	"""

	# note: this code is python 2.3 dependent. porting should not be difficult,
	# but python 2.3 makes copying and walking directories much easier.  

	# for each dir in from_base_path
	for root, dirs, files in os.walk(from_base_path):
		# make root relative to from_base_path
		# this is a hack, look for a better solution
		# remove base from root
		root = root.replace(from_base_path, "")
		# remove any leading/trailing slashes, to make sure it's relative
		root = root.strip("/")

		# get the final component of root (the current directory name)
		dirname = os.path.basename(root)
		# if the dir name is in translation_dict
		if translation_dict.has_key(dirname):
			# translate all the icons using the dir name
			# get destination path in to_base_path
			for dest in translation_dict[dirname]:
				to_dest_path = os.path.join(to_base_path, dest)
				# recreate directories between the root of to_base_path and the destination
				try:
					os.makedirs(to_dest_path)
				except: pass
				# copy
				copy_dir(root, to_dest_path)

		for file_ in files:
			# separate filename and ext
			file_, ext = os.path.splitext(file_)
			# add the current directory, in the system translation_dict uses
			translation_name = os.path.join(dirname,file_)
			# if value from above is in translation_dict
			if translation_dict.has_key(translation_name):
				# translate icon name, add suffix and save
				for dest in translation_dict[translation_name]:
					print os.path.join(root, file_+ext), os.path.join(to_base_path, dest+ext)
					to_dest_path = os.path.join(to_base_path, dest+ext)
					# recreate directories between the root of to_base_path and the destination
					try:
						os.makedirs(os.path.dirname(to_dest_path))
					except OSError, e:
						# why is this happening when the path exists???
						print e
					# copy
					shutil.copy2(os.path.join(root, file_+ext), to_dest_path)
