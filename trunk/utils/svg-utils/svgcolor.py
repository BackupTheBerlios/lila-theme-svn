#!/usr/bin/env python

"""
	svgcolor
	Recolor SVG images using a simple XML file

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

from svg import SVGFile
from svg.color import ColorTranslate

def color_translate_svg(filename, replace, file_to_save = None):
	"""
	Take a filename to an SVG image and convert it to grayscale
	if file_to_save is None, it will overwrite the file!
	replace should be an instance of the Replace class
	"""
	# open and parse the file
	svg = SVGFile(filename)

	replace.translate(svg)

	# save the file
	svg.save(file_to_save)

if __name__ == "__main__":
	from sys import argv, exit
	import os

	# check if we are doing a single or multi file search
	if len(argv) not in [3, 4]:
		print "svgcolor: Recolor SVG images using a simple XML file"
		print "Copyright 2004 Daniel G. Taylor, released under the GNU GPL"
		print "Usage:"
		print "svgcolor colors.xml file.svg [newname.svg]"
		print "svgcolor colors.xml /path/to/search/for/svgs [/path/to/put/new/svgs]"
		print "Note that the SVG files must have an svg extension for them to be included!"
		exit()

	xml_file = ColorTranslate(argv[1])

	path = argv[2]
	base_path_length = len(path)
	if path[-1] != os.sep:
		base_path_length += 1

	if len(argv) == 4:
		path_to_save = argv[3]
	else:
		path_to_save = None

	if not os.path.exists(path):
		print "That path does not exist!"
		exit()

	if os.path.isfile(path):
		# single file, so let's print out some info
		print "Coloring " + os.path.basename(path) + "..."
		color_translate_svg(path, xml_file, path_to_save)

	elif os.path.isdir(path):
		# multiple files, let's get all the colors
		def crawl_dir(path):
			"""
			recursively crawl a directory and color all the SVG
			images that are found
			"""
			print "Scanning " + path
			# for each file or dir (let's just call it a node)
			for node in os.listdir(path):
				# construct our paths
				abspath = os.path.join(path, node)
				abspath_to_save = os.path.join(path_to_save, path[base_path_length:])
				if not os.path.exists(abspath_to_save):
					# make the path
					os.makedirs(abspath_to_save)
				abspath_to_save = os.path.join(abspath_to_save, node)
				if os.path.isfile(abspath) and node[-3:].lower() == "svg":
					# parse the file
					color_translate_svg(abspath, xml_file, abspath_to_save)
				elif os.path.isdir(abspath):
					# oh, fun! recursion!
					crawl_dir(abspath)

		# =====================================================================
		print "Multi-file mode activated, coloring all found SVG images:"
		crawl_dir(path)
