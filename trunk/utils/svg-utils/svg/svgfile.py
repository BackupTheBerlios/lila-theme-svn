#!/usr/bin/env python

"""
	SVGFile and supporting classes
	Class to hold an SVG file and retrieve/set its data

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

# Imports
from svg.utils import XMLElement, get_color, set_color, ReadOnlyError
from xml.dom.minidom import parse, getDOMImplementation
from xml.dom.ext import PrettyPrint
from sys import exit

id_counter = 0

def get_special_attribute(element, attribute):
	"""
	Try to get a special attribute from an element
	"""
	if attribute == "color":
		return get_color(element, "stop-color", "stop-opacity"), False
	elif attribute == "stops":
		return element.get_children("stop", Stop), False
	elif attribute == "xlink":
		return element.get_attribute("xlink:href", False), False
	elif attribute == "fill":
		return get_color(element, "fill", "fill-opacity"), False
	elif attribute == "stroke":
		return get_color(element, "stroke", "stroke-opacity"), False
	elif element.tag in ["svg", "defs", "g"]:
		# container objects
		search = []

		if attribute[:4] == "all_":
			recursive = True
			attribute = attribute[4:]
		else:
			recursive = False

		if attribute in ["linear_gradients", "gradients", "fills"]:
			search.append(("linearGradient", Gradient))
		if attribute in ["radial_gradients", "gradients", "fills"]:
			search.append(("radialGradient", Gradient))
		if attribute in ["patterns", "fills"]:
			search.append(("pattern", TransformableContainer))
		if attribute in ["rects", "basic_shapes", "shapes"]:
			search.append(("rect", Shape))
		if attribute in ["circles", "basic_shapes", "shapes"]:
			search.append(("rect", Shape))
		if attribute in ["ellipses", "basic_shapes", "shapes"]:
			search.append(("ellipse", Shape))
		if attribute in ["lines", "basic_shapes", "shapes"]:
			search.append(("line", Line))
		if attribute in ["polylines", "basic_shapes", "shapes"]:
			search.append(("polyline", Shape))
		if attribute in ["paths", "basic_shapes", "shapes"]:
			search.append(("path", Shape))
		if attribute in ["texts", "text_shapes", "shapes"]:
			search.append(("text", Shape))
		if attribute in ["tspans", "text_shapes", "shapes"]:
			search.append(("tspan", Shape))
		if attribute in ["trefs", "text_shapes", "shapes"]:
			search.append(("tref", Shape))
		if attribute in ["groups", "containers"]:
			search.append(("g", TransformableColorableContainer))
		if attribute in ["defs", "containers"]:
			search.append(("defs", Container))

		if search:
			objs = []
			for obj, stype in search:
				objs += element.get_children(obj, stype, recursive)
			return objs, False
	return None, True

def set_special_attribute(element, attribute, value):
	"""
	Handle calls to set color values
	"""
	if attribute == "color":
		set_color(element, "stop-color", "stop-opacity", value)
		return True
	elif attribute == "fill":
		set_color(element, "fill", "fill-opacity", value)
		return True
	elif attribute == "stroke":
		set_color(element, "stroke", "stroke-opacity", value)
		return True
	elif attribute == "xlink":
		element.set_attribute("xlink:href", value)
		return True
	return False

class Stop(XMLElement):
	"""
	Hold and manage a gradient stop
	"""
	def __init__(self, element = None):
		XMLElement.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Get custom attributes like color
		"""
		if attribute in ["color"]:
			return get_special_attribute(self, attribute)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Set custom attributes like color
		"""
		if attribute in ["color"]:
			return set_special_attribute(self, attribute, value)
		return False

class Gradient(XMLElement):
	"""
	Hold and manage a gradient
	"""
	def __init__(self, element = None):
		XMLElement.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Catch calls to the gradient's stops and such
		"""
		if attribute in ["stops", "xlink"]:
			return get_special_attribute(self, attribute)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Catch calls to set the gradient's stops
		"""
		if attribute == "stops":
			raise ReadOnlyError, "Cannot set stops this way!\n" \
					"Try using add_stop to add stops or calling " \
					"unlink() on a stop element to remove it"
		elif attribute == "xlink":
			return set_special_attribute(self, attribute, value)
		return False

	def add_stop(self, color = "#00000000", offset = "1"):
		"""
		Append a stop to this gradient
		"""
		global id_counter
		stop = self.add_child_tag("stop", Stop, { "id" : str(id_counter), "color" : color, "offset" : offset })
		id_counter += 1
		return stop

class ColoredElement(XMLElement):
	"""
	Hold and manage a colored element
	"""
	def __init__(self, element = None):
		XMLElement.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Handle calls to get color values
		"""
		if attribute in ["fill", "stroke"]:
			return get_special_attribute(self, attribute)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Handle calls to set color values
		"""
		if attribute in ["fill", "stroke"]:
			return set_special_attribute(self, attribute, value)
		return False

class TransformableElement(XMLElement):
	"""
	Handle and manage transformable objects
	"""
	def __init__(self, element = None):
		XMLElement.__init__(self, element)

	def __transform(self, name, attributes):
		"""
		Do a transformation
		"""
		transform = ''
		if self.has_attribute("transform"):
			# see if an old translation is there
			# if it is, remove it and replace
			transform = self.transform
			start = transform.find(name)
			if start != -1:
				end = transform.find(")", start)
				transform = transform[:start] + transform[end + 1:]
				transform = transform.strip()
			transform += ' '
		transform += name + "("
		for attr in attributes:
			transform += str(attr) + ' '
		transform += ') '
		self.transform = transform

	def translate(self, x = None, y = None):
		"""
		Move a shape
		"""
		attributes = []
		if x:
			attributes.append(x)
		if y:
			attributes.append(y)
		self.__transform("translate", attributes)

	def scale(self, x = None, y = None):
		"""
		Scale a shape
		"""
		attributes = []
		if x:
			attributes.append(x)
		if y:
			attributes.append(y)
		self.__transform("scale", attributes)

	def rotate(self, degrees, centerx = None, centery = None):
		"""
		Rotate a shape
		"""
		attributes = []
		if degrees:
			attributes.append(degrees)
		if centerx:
			attributes.append(centerx)
		if centery:
			attributes.append(centery)
		self.__transform("rotate", attributes)

class Shape(ColoredElement, TransformableElement):
	"""
	Holds normal colorable, transformable shapes
	"""
	def __init__(self, element = None):
		ColoredElement.__init__(self, element)
		TransformableElement.__init__(self, element)

class Line(TransformableElement):
	"""
	Holds a line element
	"""
	def __init__(self, element = None):
		TransformableElement.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Handle calls to get stroke value
		"""
		if attribute in ["stroke"]:
			return get_special_attribute(self, attribute)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Handle calls to set stroke value
		"""
		if attribute in ["stroke"]:
			return set_special_attribute(self, attribute, value)
		return False

class Container(XMLElement):
	"""
	Holds SVG elements
	"""
	def __init__(self, element = None):
		XMLElement.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Handle attribute access to objects
		"""
		if attribute in ["linear_gradients", "radial_gradients", "gradients", \
						"patterns", "rects", "circles", "ellipses", "lines", \
						"polylines", "polygons", "paths", "fills", "basic_shapes", \
						"text_shapes", "shapes", "defs", "groups", "containers"]:
			return get_special_attribute(self, attribute)

	def _set_attribute(self, attribute, value):
		"""
		Handle attribute setting
		"""
		if attribute in ["linear_gradients", "radial_gradients", "gradients", \
						"patterns", "rects", "circles", "ellipses", "lines", \
						"polylines", "polygons", "paths", "fills", "basic_shapes", \
						"text_shapes", "shapes", "defs", "groups", "containers"]:
			raise ReadOnlyError, "Cannot directly set " + attribute + "!\n" \
								"To add an object, use the add_* functions, and " \
								"to remove an object call its unlink() method!"
		return False

	def add_gradient(self, grad_type, attributes, grad_id = None):
		"""
		Add a gradient to this container
		"""
		if not grad_id:
			global id_counter
			grad_id = id_counter
			id_counter += 1
		attributes["id"] = grad_id
		return self.add_child_tag(grad_type + "Gradient", Gradient, attributes)

	def add_linear_gradient(self, gradient_id = None, x1 = None, y1 = None, x2 = None, y2 = None, xlink = None):
		"""
		Add a linear gradient to this container
		"""
		attributes = {}
		if x1:
			attributes["x1"] = x1
		if y1:
			attributes["y1"] = y1
		if x2:
			attributes["x2"] = x2
		if y2:
			attributes["y2"] = y2
		if xlink:
			attributes["xlink"] = xlink
		return self.add_gradient("linear", attributes, gradient_id)

	def add_radial_gradient(self, gradient_id = None, centerx = None, centery = None, radius = None, focusx = None, focusy = None, xlink = None):
		"""
		Add a radial gradient to this container
		"""
		attributes = {}
		if centerx:
			attributes["cx"] = centerx
		if centery:
			attributes["cy"] = centery
		if radius:
			attributes["r"] = radius
		if focusx:
			attributes["fx"] = focusx
		if focusy:
			attributes["fy"] = focusy
		if xlink:
			attributes["xlink"] = xlink
		return self.add_gradient("radial", attributes, gradient_id)

	def add_shape(self, tag, shape_id, attributes, fill = None, stroke = None):
		"""
		Add an object to this container
		"""
		# if no shape id is specified get a numerical one
		if not shape_id:
			global id_counter
			shape_id = id_counter
			id_counter += 1
		attributes["id"] = str(shape_id)
		shape = self.add_child_tag(tag, SVGShape, attributes)
		if fill:
			shape.fill = fill
		if stroke:
			shape.stroke = stroke
		return shape

	def add_rect(self, rect_id = None, x = None, y = None, width = None, height = None, fill = None, stroke = None, stroke_width = None, rx = None, ry = None):
		"""
		Add a rect to this container
		x,y specify the top left corner
		fill specifies the fill color
		stroke specifies the stroke color
		rx,ry specify rounded corners
		"""
		attributes = {}
		if x:
			attributes["x"] = x
		if y:
			attributes["y"] = y
		if width:
			attributes["width"] = width
		if height:
			attributes["height"] = height
		if stroke_width:
			attributes["stroke-width"] = stroke_width
		if rx:
			attributes["rx"] = rx
		if ry:
			attributes["ry"] = ry
		return self.add_shape("rect", rect_id, attributes, fill, stroke)

	def add_circle(self, circle_id = None, centerx = None, centery = None, radius = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a circle to this container
		Center is (centerx, centery)
		"""
		attributes = {}
		if centerx:
			attributes["cx"] = centerx
		if centery:
			attributes["cy"] = centery
		if radius:
			attributes["r"] = radius
		if stroke_width:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("circle", circle_id, attributes, fill, stroke)

	def add_ellipse(self, ellipse_id = None, centerx = None, centery = None, radiusx = None, radiusy = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add an ellipse into this container
		Center is (centerx, centery)
		radiusx specifies width
		radiusy specifies height
		"""
		attributes = {}
		if centerx:
			attributes["cx"] = centerx
		if centery:
			attributes["cy"] = centery
		if radiusx:
			attributes["rx"] = radiusx
		if radiusy:
			attributes["ry"] = radiusy
		if stroke_width:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("ellipse", ellipse_id, attributes, fill, stroke)

	def add_line(self, line_id = None, x1 = None, y1 = None, x2 = None, y2 = None, stroke = None, stroke_width = None):
		"""
		Add a line into this container
		"""
		attributes = {}
		if x1:
			attributes["x1"] = x1
		if y1:
			attributes["y1"] = y1
		if x2:
			attributes["x2"] = x2
		if y2:
			attributes["y2"] = y2
		if stroke_width:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("line", line_id, attributes, stroke)

class TransformableContainer(Container, TransformableElement):
	"""
	Hold and manage a container that can be transformed
	"""
	def __init__(self, element = None):
		Container.__init__(self, element)
		TransformableElement.__init__(self, element)

class TransformableColorableContainer(TransformableContainer):
	"""
	Hold and manage a container that can be transformed/colored
	"""
	def __init__(self, element = None):
		TransformableContainer.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Handle attribute access to objects
		"""
		if attribute in ["linear_gradients", "radial_gradients", "gradients", \
						"patterns", "rects", "circles", "ellipses", "lines", \
						"polylines", "polygons", "paths", "fills", "basic_shapes", \
						"text_shapes", "shapes", "defs", "groups", "containers", \
						"fill", "stroke"]:
			return get_special_attribute(self, attribute)

	def _set_attribute(self, attribute, value):
		"""
		Handle attribute setting
		"""
		if attribute in ["linear_gradients", "radial_gradients", "gradients", \
						"patterns", "rects", "circles", "ellipses", "lines", \
						"polylines", "polygons", "paths", "fills", "basic_shapes", \
						"text_shapes", "shapes", "defs", "groups", "containers"]:
			raise ReadOnlyError, "Cannot directly set " + attribute + "!\n" \
								"To add an object, use the add_* functions, and " \
								"to remove an object call its unlink() method!"
		elif attribute in ["fill", "stroke"]:
			return set_special_attribute(self, attribute, value)
		return False

class SVGFile(Container):
	def __init__(self, filename = None):
		if filename:
			dom = parse(filename)
			Container.__init__(self, dom.documentElement)
			self.__filename = filename
			self.__dict__["defs"] = self.get_children("defs", Container)[0]
		else:
			# create a default SVG document
			XMLElement.__init__(self, getDOMImplementation().createDocument(None, "svg", None).documentElement)
			self.id = "New Document"
			self.width = "48pt"
			self.height = "48pt"
			self.xmlns = "http://www.w3.org/2000/svg"
			self.set_attribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
			self.__dict__["defs"] = self.add_child_tag("defs", SVGContainer, { "id" : "defs" })

	def save(self, filename = None):
		"""
		Save the SVG
		If no filename is given the same file that was loaded is used
		"""
		if filename:
			outfile = file(filename, "w")
		else:
			outfile = file(self.__filename, "w")
		print >>outfile, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
		print >>outfile, '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"'
		print >>outfile, '"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">'
		PrettyPrint(self.element, outfile)

	def add_gradient(self, grad_type, attributes, grad_id = None):
		"""
		Add a gradient to the SVG
		"""
		if not grad_id:
			global id_counter
			grad_id = id_counter
			id_counter += 1
		attributes["id"] = grad_id
		return self.__dict__["defs"].add_child_tag(grad_type + "Gradient", Gradient, attributes)
