#!/usr/bin/env python

"""
	Color
	SVG color modification functions

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
from xml.dom.minidom import parse

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

def grayscale(svg):
	"""
	Convert an svg to grayscale
	svg should be an SVGFile (but can also be any container element)
	"""
	# change the gradient stop colors
	for gradient in svg.all_gradients:
		for stop in gradient.stops:
			try:
				stop.color = color_to_grayscale(stop.color)
			except: pass

	# change the shape and group fill/stroke colors
	for shapes in [(item for item in svg.all_shapes), (item for item in svg.all_groups)]:
		for shape in shapes:
			try:
				fill = shape.fill
				if fill[0] == "#":
					shape.fill = color_to_grayscale(fill)
			except: pass
			try:
				stroke = shape.stroke
				if stroke[0] == "#":
					shape.stroke = color_to_grayscale(stroke)
			except: pass

class ColorTranslate:
	"""Class to hold color translation data"""
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

	def translate(self, svg):
		"""
		Translate the colors of an SVG
		"""
		translate(svg, self)

def condense_gradient(gradient):
	"""
	Returns a condensed version of the gradient:
	(stop1, stop2, stop3, ...)
	"""
	tmp = ()
	for stop in gradient.stops:
		tmp += (stop.color,)
	return tmp

def translate_gradient(gradient, new_gradient):
	"""
	Replace a Gradient object with the values
	from new_gradient
	"""
	stops = gradient.stops
	for pos in range(len(stops)):
		stops[pos].color = new_gradient[pos]

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
			for stop in gradient.stops:
				if stop.color in replace.colors.keys():
					stop.color = replace.colors[stop.color]

def translate_object(object, replacements):
	"""
	Translates the color of an object if it's
	fill or stroke are found
	Returns True if we got a hit
	"""
	replaced = False
	# get the object's fill & stroke
	try:
		fill = object.fill
		if fill and fill[:3] == "url": fill = None
	except: fill = None
	try:
		stroke = object.stroke
		if stroke and stroke[:3] == "url": stroke = None
	except: stroke = None

	if not (fill or stroke):
		return replaced

	for replacement in replacements.keys():
		# get the replacement's fill and stroke
		match_fill = replacement[0]
		match_stroke = replacement[1]
		if match_fill:
			if fill == match_fill:
				object.fill = replacements[replacement][0]
				replaced = True
		if match_stroke:
			if stroke == match_stroke:
				object.stroke = replacements[replacement][1]
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
			try:
				fill = object.fill
			except: fill = None
			try:
				stroke = object.stroke
			except: stroke = None
			if fill in replace.colors.keys():
				object.fill = replace.colors[fill]
			if stroke in replace.colors.keys():
				object.stroke = replace.colors[stroke]

def translate(svg, replace):
	"""
	Take a an SVGFile and convert it using a ColorTranslate XML spec
	"""

	# translate any gradients
	check_gradients(svg.all_gradients, replace, replace.linear_gradients)

	# translate any objects
	check_objects(svg.all_rects, replace, replace.rects)
	check_objects(svg.all_circles, replace, replace.circles)
	check_objects(svg.all_ellipses, replace, replace.ellipses)
	check_objects(svg.all_lines, replace, replace.lines)
	check_objects(svg.all_polylines, replace, replace.polylines)
	check_objects(svg.all_polygons, replace, replace.polygons)
	check_objects(svg.all_paths, replace, replace.paths)
	check_objects(svg.all_texts, replace, replace.texts)
	check_objects(svg.all_tspans, replace, replace.tspans)
	check_objects(svg.all_trefs, replace, replace.trefs)
	check_objects(svg.all_text_paths, replace, replace.text_paths)

	# translate groups
	check_objects(svg.all_groups, replace, replace.groups)
