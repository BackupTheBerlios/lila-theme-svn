#!/usr/bin/env python

"""
	svggrayscale
	Convert SVG images to grayscale

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

from svgfile import SVGFile

def color_to_grayscale(color):
	"""
	Return the grayscale version of color
	color must be in hex (i.e. #000000ff)
	Note that the alpha value is NOT changed!
	"""
	# grab the different colors
	red = color[1:3]
	green = color[3:5]
	blue = color[5:7]
	# find the average
	gray = hex((int(red, 16) + int(green, 16) + int(blue, 16)) / 3)[2:]
	# return the grayscale value
	return "#" + gray + gray + gray + color[-2:]

def convert_svg_to_grayscale(filename, file_to_save = None):
	"""
	Take a filename to an SVG image and convert it to grayscale
	if file_to_save is None, it will overwrite the file!
	"""
	# open and parse the file
	svg = SVGFile(filename)
	# get all the color information
	linear_gradients = svg.get_linear_gradients()
	radial_gradients = svg.get_radial_gradients()
	rects = svg.get_rects()
	circles = svg.get_circles()
	ellipses = svg.get_elipses()
	lines = svg.get_lines()
	polylines = svg.get_polylines()
	polygons = svg.get_polygons()
	paths = svg.get_paths()
	texts = svg.get_texts()
	tspans = svg.get_tspans()
	trefs = svg.get_trefs()
	text_paths = svg.get_text_paths()
	groups = svg.get_groups()

	# change the colors
	for gradient_type in [linear_gradients, radial_gradients]:
		for gradient in gradient_type:
			for stop in gradient.get_stops():
				old = stop.get_color()
				new = color_to_grayscale(old)
				stop.set_color(new)
	for objects in [rects, circles, ellipses, lines, polylines, polygons, \
					paths, texts, tspans, trefs, text_paths, groups]:
		for object in objects:
			fill = object.get_fill_color()
			if fill and fill[:3] != "url":
				newfill = color_to_grayscale(fill)
				object.set_fill_color(newfill)
			stroke = object.get_stroke_color()
			if stroke and stroke[:3] != "url":
				newstroke = color_to_grayscale(stroke)
				object.set_stroke_color(newstroke)

	# save the file
	svg.save(file_to_save)

if __name__ == "__main__":
	from sys import argv, exit
	import os

	# check if we are doing a single or multi file search
	if len(argv) not in [2, 3]:
		print "svggrayscale: Convert SVG images to grayscale"
		print "Copyright 2004 Daniel G. Taylor, released under the GNU GPL"
		print "Usage:"
		print "svggrayscale file.svg [newname.svg]"
		print "svggrayscale /path/to/search/for/svgs [/path/to/put/new/svgs]"
		print "Note that the SVG files must have an svg extension for them to be included!"
		exit()

	path = argv[1]
	base_path_length = len(path)
	if path[-1] != "/" or path[-1] != "\\":
		base_path_length += 1

	if len(argv) == 3:
		path_to_save = argv[2]
	else:
		path_to_save = None

	if not os.path.exists(path):
		print "That path does not exist!"
		exit()

	if os.path.isfile(path):
		# single file, so let's print out some info
		print "Grayscaling " + os.path.basename(path) + "..."
		convert_svg_to_grayscale(path, path_to_save)

	elif os.path.isdir(path):
		# multiple files, let's get all the colors
		def crawl_dir(path):
			"""
			recursively crawl a directory and convert all the SVG
			images that are found to grayscale
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
					convert_svg_to_grayscale(abspath, abspath_to_save)
				elif os.path.isdir(abspath):
					# oh, fun! recursion!
					crawl_dir(abspath)

		# =====================================================================
		print "Multi-file mode activated, converting all found SVG images:"
		crawl_dir(path)
