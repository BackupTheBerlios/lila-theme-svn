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

from svgfile import SVGFile
from xml.dom.minidom import parse

class Replace:
	"""Class to hold color replacement data"""
	def __init__(self, filename = None):
		"""Initialize the class"""
		# setup some default empty dicts
		self.colors = {}
		self.gradients = {}
		self.objects = {}
		self.linear_gradients = {}
		self.radial_gradients = {}
		self.rects = {}
		self.circles = {}
		self.ellipses = {}
		self.lines = {}
		self.polylines = {}
		self.polygons = {}
		self.paths = {}
		self.texts = {}
		self.tspans = {}
		self.trefs = {}
		self.text_paths = {}
		self.groups = {}
		if filename:
			self.load_xml_file(filename)

	def load_xml_file(self, filename):
		"""
		Loads the xml file into the class
		For the syntax please see svgcolor-template.xml!
		"""
		self._dom = parse(filename)
		# colors
		for color_tag in self._dom.documentElement.getElementsByTagName("color"):
			old = color_tag.getAttribute("old")
			new = color_tag.getAttribute("new")
			self.colors[old] = new
		# gradients
		self.load_gradient(self._dom.documentElement.getElementsByTagName("gradient"), self.gradients)
		self.load_gradient(self._dom.documentElement.getElementsByTagName("linearGradient"), self.linear_gradients)
		self.load_gradient(self._dom.documentElement.getElementsByTagName("radialGradient"), self.radial_gradients)
		# objects
		self.load_object(self._dom.documentElement.getElementsByTagName("object"), self.objects)
		self.load_object(self._dom.documentElement.getElementsByTagName("rect"), self.rects)
		self.load_object(self._dom.documentElement.getElementsByTagName("circle"), self.circles)
		self.load_object(self._dom.documentElement.getElementsByTagName("ellipse"), self.ellipses)
		self.load_object(self._dom.documentElement.getElementsByTagName("line"), self.lines)
		self.load_object(self._dom.documentElement.getElementsByTagName("polyline"), self.polylines)
		self.load_object(self._dom.documentElement.getElementsByTagName("polygon"), self.polygons)
		self.load_object(self._dom.documentElement.getElementsByTagName("path"), self.paths)
		self.load_object(self._dom.documentElement.getElementsByTagName("text"), self.texts)
		self.load_object(self._dom.documentElement.getElementsByTagName("tspan"), self.tspans)
		self.load_object(self._dom.documentElement.getElementsByTagName("tref"), self.trefs)
		self.load_object(self._dom.documentElement.getElementsByTagName("textPath"), self.text_paths)
		self.load_object(self._dom.documentElement.getElementsByTagName("group"), self.groups)

	def load_gradient(self, elements, store):
		"""
		load the gradient color replacement data from
		a given set of XML element objects into store dict
		"""
		for gradient_tag in elements:
			old = ()
			new = ()
			old_grad = gradient_tag.getElementsByTagName("old")[0]
			for stop in old_grad.getElementsByTagName("stop"):
				old += (stop.getAttribute("color"),)
			new_grad = gradient_tag.getElementsByTagName("new")[0]
			for stop in new_grad.getElementsByTagName("stop"):
				new += (stop.getAttribute("color"),)
			store[old] = new

	def load_object(self, elements, store):
		"""
		load object color replacement data from a given
		set of XML Element objects into the store dict
		"""
		for object_tag in elements:
			fill = object_tag.getElementsByTagName("fill")[0]
			fill_old = fill.getAttribute("old")
			fill_new = fill.getAttribute("new")
			stroke = object_tag.getElementsByTagName("stroke")[0]
			stroke_old = stroke.getAttribute("old")
			stroke_new = stroke.getAttribute("new")
			store[(fill_old, stroke_old)] = (fill_new, stroke_new)


def condense_gradient(gradient):
	"""
	Returns a condensed version of the gradient:
	(stop1, stop2, stop3, ...)
	"""
	tmp = ()
	for stop in gradient.get_stops():
		tmp += (stop.get_color(),)
	return tmp

def translate_gradient(gradient, new_gradient):
	"""
	Replace a Gradient object with the values
	from new_gradient
	"""
	stops = gradient.get_stops()
	for pos in range(len(stops)):
		stops[pos].set_color(new_gradient[pos])

def check_gradients(gradients, replace, replace_type):
	"""
	Check and translate any needed gradients
	"""
	for gradient in gradients:
		condensed = condense_gradient(gradient)
		if condensed in replace_type.keys():
			translate_gradient(gradient, replace_type[condensed])
		elif condensed in replace.gradients.keys():
			translate_gradient(gradient, replace.gradients[condensed])
		else:
			for stop in gradient.get_stops():
				old = stop.get_color()
				if old in replace.colors.keys():
					stop.set_color(replace.colors[old])

def translate_object(object, replacements):
	"""
	Translates the color of an object if it's
	fill or stroke are found
	Returns True if we got a hit
	"""
	replaced = False
	# get the object's fill & stroke
	fill = object.get_fill_color()
	stroke = object.get_stroke_color()
	if fill and fill[:3] == "url": fill = None
	if stroke and stroke[:3] == "url": stroke = None

	for replacement in replacements.keys():
		# get the replacement's fill and stroke
		match_fill = replacement[0]
		match_stroke = replacement[1]
		if match_fill and match_stroke:
			if fill == match_fill and stroke == match_stroke:
				object.set_fill_color(replacements[replacement][0])
				object.set_stroke_color(replacements[replacement][1])
				replaced = True
		elif match_fill:
			if fill == match_fill:
				object.set_fill_color(replacements[replacement][0])
				replaced = True
		elif match_stroke:
			if stroke == match_stroke:
				object.set_stroke_color(replacements[replacement][1])
				replaced = True
	return replaced

def check_objects(objects, replace, replace_type):
	"""
	Check and translate any needed objects
	"""
	for object in objects:
		if translate_object(object, replace_type):
			pass
		elif translate_object(object, replace.objects):
			pass
		else:
			fill = object.get_fill_color()
			stroke = object.get_stroke_color()
			if fill in replace.colors.keys():
				object.set_fill_color(replace.colors[fill])
			if stroke in replace.colors.keys():
				object.set_stroke_color(replace.colors[stroke])

def color_translate_svg(filename, replace, file_to_save = None):
	"""
	Take a filename to an SVG image and convert it to grayscale
	if file_to_save is None, it will overwrite the file!
	replace should be an instance of the Replace class
	"""
	# open and parse the file
	svg = SVGFile(filename)
	# get all the color information
	linear_gradients = svg.get_linear_gradients()
	radial_gradients = svg.get_radial_gradients()
	rects = svg.get_rects()
	circles = svg.get_circles()
	ellipses = svg.get_ellipses()
	lines = svg.get_lines()
	polylines = svg.get_polylines()
	polygons = svg.get_polygons()
	paths = svg.get_paths()
	texts = svg.get_texts()
	tspans = svg.get_tspans()
	trefs = svg.get_trefs()
	text_paths = svg.get_text_paths()
	groups = svg.get_groups()

	# translate any gradients
	check_gradients(linear_gradients, replace, replace.linear_gradients)
	check_gradients(radial_gradients, replace, replace.radial_gradients)

	# translate any objects
	check_objects(rects, replace, replace.rects)
	check_objects(circles, replace, replace.circles)
	check_objects(ellipses, replace, replace.ellipses)
	check_objects(lines, replace, replace.lines)
	check_objects(polylines, replace, replace.polylines)
	check_objects(polygons, replace, replace.polygons)
	check_objects(paths, replace, replace.paths)
	check_objects(texts, replace, replace.texts)
	check_objects(tspans, replace, replace.tspans)
	check_objects(trefs, replace, replace.trefs)
	check_objects(text_paths, replace, replace.text_paths)
	check_objects(groups, replace, replace.groups)

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
		print "svggrayscale colors.xml /path/to/search/for/svgs [/path/to/put/new/svgs]"
		print "Note that the SVG files must have an svg extension for them to be included!"
		exit()

	xml_file = Replace(argv[1])

	path = argv[2]
	base_path_length = len(path)
	if path[-1] != "/" or path[-1] != "\\":
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
