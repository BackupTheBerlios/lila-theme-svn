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

def get_path_content(path, parent_name):
	"""
	Returns the content of a path node
	"""
	# if path action is copy
	if path.action == "copy":
		# if there is no path content
		if not path.content:
			# set content to parent name
			content = parent_name
		else:
			# set content to path content
			content = path.content
	# else if path action is prepend
	elif path.action == "prepend":
		# set content to path content + parent name
		content = path.content + parent_name
	# else if path action is append
	elif path.action == "append":
		# set content to parent name + path content
		content = parent_name + path.content
	else:
		# set content to path content
		content = path.content
	# return content
	if content:
		return content
	else:
		raise ValueError, parent_name + " is missing path content for " + path.env + "!"

def convert_xmldb_to_dict(xmldb, from_theme_type, to_theme_type, base_path = "."):
	"""
	This function returns a dictionary object of mappings from
	the icon names of the from_theme_type to the to_theme_type
	i.e. if "gnome" and "kde" are passed, it returns:
	{ ..., "devices/gnome-dev-floppy" : ["devices/3floppy_mount"],
		   "mimetypes/gnome-mime-text" : ["mimetypes/txt"],
		   "devices/gnome-dev-printer" : ["devices/printer", 
		   "devices/printer1", "devices/print_printer"], ... }
	Note that the keys are strings while the values are lists
	this is to accomidate multiple paths to translate to
	When there are multiple paths to translate from, only the first
	is used in the key
	base_path should be the location of the theme to translate
	"""
	assert from_theme_type != to_theme_type

	translation_dict = {}

	# for each icon
	for icon in xmldb.icons:
		key, value = None, []
		# if to/from == standard
		if from_theme_type == "standard":
			key = icon.name.split(",")[0]
		elif to_theme_type == "standard":
			for val in icon.name.split(","):
				value.append(val)
		# for each path in the icon
		from_path, to_path = None, None
		for path in icon.paths:
			# if path env == from theme type
			if path.env == from_theme_type:
				from_path = path
			# if path env == to theme type
			elif path.env == to_theme_type:
				to_path = path
		# if from and to path
		if (from_path or key) and (to_path or value):
			# get from path content
			if from_path:
				from_path_content = get_path_content(from_path, icon.name).split(",")[0]
			else:
				from_path_content = key
			if to_path:
				# if to path action == copy
				if to_path.action == "copy":
					# if to path has no content, set it to the icon name
					if not to_path.content:
						to_path_content = icon.name.split(",")
					else:
						to_path_content = to_path.content.split(",")
						# set dict[from path content] to path content
					translation_dict[from_path_content] = to_path_content
				# else if to path action == prepend
				elif to_path.action == "prepend":
					# set dict[from path content] to path content + icon name
					new_list = []
					for p in icon.name.split(","):
						d, f = os.path.split(p)
						new_list.append(os.path.join(d, to_path.content + f))
					translation_dict[from_path_content] = new_list
				# else if to path action == append
				elif to_path.action == "append":
					# set dict[from path content] to icon name + path content
					new_list = []
					for p in icon.name.split(","):
						new_list.append(p + to_path.content)
					translation_dict[from_path_content] = new_list
				else:
					# set dict[from path content] to path content
					translation_dict[from_path_content] = to_path.content.split(",")
			else:
				translation_dict[from_path_content] = value

	# for each directory
	for directory in xmldb.directories:
		key, value = None, []
		# if to/from == standard
			# set directory name as key/value
		if from_theme_type == "standard":
			key = directory.name
		elif to_theme_type == "standard":
			value.append(directory.name)
		# for each path in dir
		from_path, to_path = None, None
		for path in directory.paths:
			# if path env == from theme type
			if path.env == from_theme_type:
				from_path = path
			# else if path env == to theme type
			elif path.env == to_theme_type:
				to_path = path
		# if from and to path
		if (from_path or key) and (to_path or value):
			# get from path content
			if from_path:
				from_path_content = get_path_content(from_path, directory.name).split(",")[0]
			else:
				from_path_content = key
			if to_path:
				# if to path action == copy
				if to_path.action == "copy":
					# if to path doesn't have content, set it to the directory name
					if not to_path.content:
						to_path_content = directory.name.split(",")
					else:
						to_path_content = to_path.content.split(",")
					# for each file in base path + directory name
					for file in os.listdir(os.path.join(base_path, from_path_content)):
						# remove the file extension if there is one
						name, ext = os.path.splitext(file)
						# if dict doesn't have key of filename
						if not translation_dict.has_key(os.path.join(from_path_content, name)):
							# set dict[directory name + file] to content + file
							new_list = []
							for p in to_path_content:
								new_list.append(os.path.join(p, file))
							translation_dict[os.path.join(from_path_content, name)] = new_list
				# else if to path action == prepend
				elif to_path.action == "prepend":
					# for each file in base path + directory name
					for file in os.listdir(os.path.join(base_path, from_path_content)):
						# remove the file extension if there is one
						name, ext = os.path.splitext(file)
						# if dict doesn't have key of filename
						if not translation_dict.has_key(os.path.join(from_path_content, name)):
							# set dict[directory name + file] to path content + file
							new_list = []
							for p in directory.name.split(","):
								new_list.append(os.path.join(p, to_path.content + name))
							translation_dict[os.path.join(from_path_content, name)] = new_list
				# else if to path action == append
				elif to_path.action == "append":
					# for each file in base path + directory name
					for file in os.listdir(os.path.join(base_path, from_path_content)):
						# remove the file extension if there is one
						name, ext = os.path.splitext(file)
						# if dict doesn't have key of filename
						if not translation_dict.has_key(os.path.join(from_path_content, name)):
							# set dict[directory name + file] to file + to path content
							new_list = []
							for p in directory.name.split(","):
								new_list.append(os.path.join(p, name + to_path.content))
							translation_dict[os.path.join(from_path_content, name)] = new_list
				else:
					# for each file in base path + directory name
					for file in os.listdir(os.path.join(base_path, from_path_content)):
						# remove the file extension
						name, ext = os.path.splitext(file)
						# if dict doesn't have key of filename
						if not translation_dict.has_key(os.path.join(from_path_content, name)):
							# set dict[directory name + file] to path content
							translation_dict[os.path.join(from_path_content, name)] = to_path.content.split(",")
			else:
				# we have (from_path or key) and value
				if from_path:
					if from_path.action == "copy" or not from_path.action:
						dir_to_list = from_path.content or directory.name
					else:
						# make sure we don't pre-/append to the directory name!
						dir_to_list = directory.name
				else:
					# we just have the key value
					dir_to_list = key
				# make sure it's a directory
				if os.path.isdir(os.path.join(base_path, dir_to_list)):
					# for each file in the directory
					for filename in os.listdir(os.path.join(base_path, dir_to_list)):
						# remove the file extension
						file, ext = os.path.splitext(filename)
						# default to the normal filename, this is used below
						file_to_save = file
						if from_path:
							if from_path.action == "prepend":
								# remove what was prepended before
								file_to_save = file[len(from_path.content):]
							elif from_path.action == "append":
								# remove what was appended before
								file_to_save = from_path.content[:-len(from_path.content)]
						# save it!
						translation_dict[os.path.join(dir_to_list, file)] = [os.path.join(value[0], file_to_save)]
	# return this baby!
	return translation_dict

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

	# walk the directories!
	for root, dirs, files in os.walk(from_base_path):
		# save a relative root that removes the from_base_path
		relative_root = root[len(from_base_path) + 1:]
		# for each file in the root (aka directory)
		for file in files:
			# split the file extension
			name, ext = os.path.splitext(file)
			# create the 'full name', i.e. 'devices/cdrom'
			full_name = os.path.join(relative_root, name)
			# if the full name is in the dictionary
			if translation_dict.has_key(full_name):
				# for each path in the value
				for path in translation_dict[full_name]:
					# setup the name to save
					save_name = os.path.join(to_base_path, path + ext)
					if not os.path.exists(os.path.dirname(save_name)):
						os.makedirs(os.path.dirname(save_name))
					#print os.path.join(root, file), save_name
					# copy the file!
					shutil.copy2(os.path.join(root, file), save_name)
