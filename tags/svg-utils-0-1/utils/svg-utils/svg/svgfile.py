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

"""
	This software implements part of the W3C SVG 1.1 Specification
	Access to objects and data have been changed for ease-of-use
	For more information on SVG, see:
	http://www.w3.org/TR/SVG11/
"""

# Imports
from svg.utils import XMLElement, get_color, set_color, ReadOnlyError
from xml.dom.minidom import parse, getDOMImplementation, Document
from xml.dom.ext import Print
from sys import exit

id_counter = 0

def get_special_attribute(element, attribute, recursive = False):
	"""
	Try to get a special attribute from an element
	"""
	if attribute == "color":
		color = get_color(element, "stop-color", "stop-opacity")
		if color: return color, False
		else: return color, True
	elif attribute == "stops":
		return element.get_children("stop", Stop), False
	elif attribute == "fill":
		color = get_color(element, "fill", "fill-opacity")
		if color: return color, False
		else: return color, True
	elif attribute == "stroke":
		color = get_color(element, "stroke", "stroke-opacity")
		if color: return color, False
		else: return color, True
	elif attribute == "text":
		text = ''
		for child in element.element.childNodes:
			if child.nodeType == child.TEXT_NODE:
				text += child.data.strip()
		if text:
			return text, False
	elif attribute == "points":
		try:
			points = []
			for point in element.points.split():
				x,y = point.split(",")
				points.append((x,y))
			return points, False
		except:
			return None, True
	else:
		# container objects
		search = []
		recursive = False

		if attribute[:4] == "all_":
			recursive = True
			attribute = attribute[4:]

		if attribute in ["linear_gradients", "gradients", "fills"]:
			search.append(("linearGradient", LinearGradient))
		if attribute in ["radial_gradients", "gradients", "fills"]:
			search.append(("radialGradient", RadialGradient))
		if attribute in ["patterns", "fills"]:
			search.append(("pattern", SVGElement))
		if attribute in ["rects", "basic_shapes", "shapes"]:
			search.append(("rect", Rect))
		if attribute in ["circles", "basic_shapes", "shapes"]:
			search.append(("circle", Circle))
		if attribute in ["ellipses", "basic_shapes", "shapes"]:
			search.append(("ellipse", Ellipse))
		if attribute in ["lines", "basic_shapes", "shapes"]:
			search.append(("line", Line))
		if attribute in ["polylines", "basic_shapes", "shapes"]:
			search.append(("polyline", Shape))
		if attribute in ["polygons", "basic_shapes", "shapes"]:
			search.append(("polygon", Shape))
		if attribute in ["paths", "basic_shapes", "shapes"]:
			search.append(("path", Path))
		if attribute in ["texts", "text_shapes", "shapes"]:
			search.append(("text", TextContainer))
		if attribute in ["tspans", "text_shapes", "shapes"]:
			search.append(("tspan", TextElement))
		if attribute in ["trefs", "text_shapes", "shapes"]:
			search.append(("tref", Tref))
		if attribute in ["text_paths", "text_shapes", "shapes"]:
			search.append(("textPath", TextPath))
		if attribute in ["groups", "containers"]:
			search.append(("g", Group))
		if attribute in ["defs", "containers"]:
			search.append(("defs", Defs))

		if search:
			objs = []
			for obj, stype in search:
				# shortcut for <svg> to go straight to defs
				if obj in ["linearGradient", "radialGradient", "pattern"] and element.tag == "svg":
					objs += element.defs.get_children(obj, stype, recursive)
				else:
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
	elif attribute == "text":
		for node in element.element.childNodes:
			element.element.removeChild(node)
		element.element.appendChild(Document().createTextNode(value))
		return True
	elif attribute == "points":
		points = ""
		for point in value:
			points += " " + str(point[0]) + "," + str(point[1])
		element.element.setAttribute("points", points.strip())
		return True
	elif attribute in ["stops"]:
		raise ReadOnlyError, str(attribute) + " is read only! Use the add_* functions instead!"
	return False

class SVGElement(XMLElement):
	"""
	Hold and manage an SVG element
	"""
	def __init__(self, element=None):
		XMLElement.__init__(self, element)
		if not self.__dict__.has_key("special_attributes"):
			self.__dict__["special_attributes"] = []

	def register_special_attribute(self, attribute):
		"""
		Register a special attribute that will be passed
		on to the special attribute handler function
		"""
		self.__dict__["special_attributes"].append(attribute)

	def unregister_special_attribute(self, attribute):
		"""
		Remove a special attribute from this item
		"""
		for pos in range(len(self.__dict__["special_attributes"]) - 1):
			if self.__dict__["special_attributes"][pos] == attribute:
				self.__dict__["special_attributes"][pos:pos + 1] = []
				return True
		raise ValueError, str(attribute) + " not registered!"

	def _get_attribute(self, attribute):
		"""
		Get custom attributes
		"""
		if attribute in self.__dict__["special_attributes"]:
			return get_special_attribute(self, attribute)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Set custom attributes
		"""
		print attribute, value
		if attribute in self.__dict__["special_attributes"]:
			print "setting special..."
			return set_special_attribute(self, attribute, value)
		return False

	def add_element(self, element):
		"""
		Add an existing element as a child into this element
		"""
		self.__dict__["element"].appendChild(element.element)

class Stop(SVGElement):
	"""
	Hold and manage a gradient stop
	"""
	def __init__(self, element = None):
		SVGElement.__init__(self, element)
		self.register_special_attribute("color")

class Gradient(SVGElement):
	"""
	Hold and manage a gradient
	"""
	def __init__(self, element = None):
		SVGElement.__init__(self, element)
		self.register_attribute_alias("xlink", "xlink:href")
		self.register_special_attribute("stops")

	def add_stop(self, id = None, color = "#000000ff", offset = "1"):
		"""
		Append a stop to this gradient
		"""
		if id == None:
			global id_counter
			id = id_counter
			id_counter += 1
		stop = self.add_child_tag("stop", Stop, { "id" : str(id), "color" : color, "offset" : offset })
		id_counter += 1
		return stop

class LinearGradient(Gradient):
	"""
	Hold and manage a linear gradient
	"""
	def __init__(self, element = None):
		Gradient.__init__(self, element)
		self.register_attribute_alias("startx", "x1")
		self.register_attribute_alias("starty", "y1")
		self.register_attribute_alias("stopx", "x2")
		self.register_attribute_alias("stopy", "y2")

class RadialGradient(Gradient):
	"""
	Hold and manage a radial gradient
	"""
	def __init__(self, element = None):
		Gradient.__init__(self, element)
		self.register_attribute_alias("centerx", "cx")
		self.register_attribute_alias("centery", "cy")
		self.register_attribute_alias("radius", "r")
		self.register_attribute_alias("focalx", "fx")
		self.register_attribute_alias("focaly", "fy")

class FilledElement:
	"""
	Hold and manage a filled element
	This is NOT a stand-alone element! Use SVGElement with it!
	"""
	def __init__(self):
		self.register_special_attribute("fill")

class StrokedElement:
	"""
	Hold and manage a stroked element
	This is NOT a stand-alone element! Use SVGElement with it!
	"""
	def __init__(self):
		self.register_special_attribute("stroke")

class TransformableElement:
	"""
	Handle and manage transformable objects
	This is NOT a stand-alone element! Use SVGElement with it!
	"""
	def __init__(self):
		pass

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

class Shape(SVGElement, FilledElement, StrokedElement, TransformableElement):
	"""
	Holds normal colorable, transformable shapes (excluding lines)
	"""
	def __init__(self, element = None):
		SVGElement.__init__(self, element)
		FilledElement.__init__(self)
		StrokedElement.__init__(self)
		TransformableElement.__init__(self)

class Rect(Shape):
	"""
	Holds a rect shape
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		self.register_attribute_alias("roundedx", "rx")
		self.register_attribute_alias("roundedy", "ry")

class Circle(Shape):
	"""
	Holds a circle shape
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		self.register_attribute_alias("centerx", "cx")
		self.register_attribute_alias("centery", "cy")
		self.register_attribute_alias("radius", "r")

class Ellipse(Shape):
	"""
	Holds an ellipse shape
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		self.register_attribute_alias("centerx", "cx")
		self.register_attribute_alias("centery", "cy")
		self.register_attribute_alias("radiusx", "rx")
		self.register_attribute_alias("radiusy", "ry")

class Line(SVGElement, StrokedElement, TransformableElement):
	"""
	Holds a line element
	"""
	def __init__(self, element = None):
		SVGElement.__init__(self, element)
		StrokedElement.__init__(self)
		TransformableElement.__init__(self)
		self.register_attribute_alias("startx", "x1")
		self.register_attribute_alias("starty", "y1")
		self.register_attribute_alias("stopx", "x2")
		self.register_attribute_alias("stopy", "y2")

class PolyShape(Shape):
	"""
	Holds a polyline/polygon
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		self.register_special_attribute("points")

	def add_point(self, x, y):
		"""
		Add a point to the polyshape
		"""
		try:
			points = self.get_attribute("points")
			points.append((x,y))
			self.points = points
		except:
			self.points = [(x, y),]

	def remove_point(self, x, y):
		"""
		Remove a point from the polyshape
		"""
		pass

	def clear(self):
		"""
		Clear this polyshape's point data
		"""
		self.points = []

class Path(Shape):
	"""
	Hold and manage a path element
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		self.register_attribute_alias("data", "d")

	def moveto(self, x, y, relative = False):
		"""
		Move the path's 'pen'
		"""
		if relative:
			char = "m"
		else: char = "M"
		self.d += " " + char + " " + str(x) + "," + str(y)

	def lineto(self, x = None, y = None, relative = False):
		"""
		Draw a line to the new point from the 'pen's current position
		"""
		if relative:
			char = " l"
		else: char = " L"
		if x:
			char += " " + str(x)
		if y:
			if x:
				char += ", "
			char += str(y)
		self.d += char

	def close(self):
		"""
		Close the current subpath
		"""
		self.d += " Z"

	def curveto(self, curve_node_x1, curve_node_y1, curve_node_x2, curve_node_y2, x, y, relative = False):
		"""
		Add a bezier curve to this path
		"""
		pass

	def curveto_smooth(self, curve_node_x, curve_node_y, x, y, relative = False):
		"""
		Add a smooth bezier curve to this path
		"""
		pass

	def clear(self):
		"""
		Clear the path
		"""
		self.d = ''

class TextElement(Shape):
	"""
	Holds an element containing text
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		self.register_special_attribute("text")

class Tref(Shape):
	"""
	Holds a tref element
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		self.register_attribute_alias("xlink", "xlink:href")

class TextContainer(Shape):
	"""
	Holds a text container
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		self.register_special_attribute("text")
		self.register_special_attribute("tspans")
		self.register_special_attribute("trefs")
		self.register_special_attribute("all_tspans")
		self.register_special_attribute("all_trefs")

	def add_child_text(self, element_name, element_type, tspan_id = None, text = None, x = None, y = None, deviation_x = None, deviation_y = None, rotation = None, length = None, font_weight = None, fill = None, stroke = None, xlink = None):
		"""
		Add a text child
		"""
		attributes = {}
		if text:
			attributes["text"] = text
		if x:
			attributes["x"] = x
		if y:
			attributes["y"] = y
		if deviation_x:
			attributes["dx"] = deviation_x
		if deviation_y:
			attributes["dy"] = deviation_y
		if rotation:
			attributes["rotation"] = rotation
		if length:
			attributes["textLength"] = length
		if font_weight:
			attributes["font-weight"] = font_weight
		if xlink:
			attributes["xlink"] = xlink
		if not tspan_id:
			global id_counter
			tspan_id = str(id_counter)
			id_counter += 1
		attributes["id"] = tspan_id
		text = self.add_child_tag(element_name, element_type, attributes)
		if fill:
			text.set_attribute("fill", fill)
		if stroke:
			text.set_attribute("stroke", stroke)
		return text

	def add_tspan(self, tspan_id = None, text = None, x = None, y = None, deviation_x = None, deviation_y = None, rotation = None, length = None, font_weight = None, fill = None, stroke = None, element = None):
		"""
		Add a tref into this container
		"""
		if element:
			self.element.appendChild(element.element)
			return element
		else:
			return self.add_child_text("tspan", TextElement, tspan_id, text, x, y, deviation_x, deviation_y, rotation, length, font_weight, fill, stroke)

	def add_tref(self, tref_id = None, xlink = None, text = None, x = None, y = None, dx = None, dy = None, rotation = None, length = None, font_weight = None, fill = None, stroke = None, element = None):
		"""
		Add a tref into this container
		"""
		if element:
			self.element.appendChild(element.element)
			return element
		else:
			return self.add_child_text("tref", Tref, tref_id, text, x, y, deviation_x, deviation_y, rotation, length, font_weight, fill, stroke, xlink)

class TextPath(SVGElement, TransformableElement):
	"""
	Holds a textPath element
	"""
	def __init__(self, element = None):
		SVGElement.__init__(self, element)
		TransformableElement.__init__(self)
		self.register_attribute_alias("xlink", "xlink:href")
		self.register_special_attribute("text")

class Defs(SVGElement):
	"""
	Holds a defs element
	"""
	def __init__(self, element = None):
		SVGElement.__init__(self, element)
		for special_element in ["gradients", "fills", "linear_gradients", \
											"radial_gradients", "patterns"]:
			self.register_special_attribute(special_element)
			self.register_special_attribute("all_" + special_element)

	def add_gradient(self, grad_type = None, attributes = None, grad_id = None):
		"""
		Add a gradient to this container
		gradient type, id, attributes etc... will produce a new gradient
		"""
		if not grad_id:
			global id_counter
			grad_id = id_counter
			id_counter += 1
		attributes["id"] = grad_id
		if grad_type == "linear":
			grad_class = LinearGradient
		else:
			grad_class = RadialGradient
		return self.add_child_tag(grad_type + "Gradient", grad_class, attributes)

	def add_linear_gradient(self, id = None, startx = None, starty = None, stopx = None, stopy = None, xlink = None):
		"""
		Add a linear gradient to this container
		"""
		attributes = {}
		if startx != None:
			attributes["x1"] = startx
		if starty != None:
			attributes["y1"] = starty
		if stopx != None:
			attributes["x2"] = stopx
		if stopy != None:
			attributes["y2"] = stopy
		if xlink:
			attributes["xlink"] = xlink
		return self.add_gradient("linear", attributes, id)

	def add_radial_gradient(self, id = None, centerx = None, centery = None, radius = None, focusx = None, focusy = None, xlink = None):
		"""
		Add a radial gradient to this container
		center and focus are (x, y) tuples
		"""
		attributes = {}
		if centerx != None:
			attributes["cx"] = centerx
		if centery != None:
			attributes["cy"] = centery
		if radius != None:
			attributes["r"] = radius
		if focusx != None:
			attributes["fx"] = focusx
		if focusy != None:
			attributes["fy"] = focusy
		if xlink:
			attributes["xlink"] = xlink
		return self.add_gradient("radial", attributes, id)

	def add_pattern(self, id = None):
		"""
		Add a pattern to this container
		"""
		pass

class Container(SVGElement):
	"""
	Holds SVG elements
	"""
	def __init__(self, element = None):
		SVGElement.__init__(self, element)
		for special_element in ["shapes", "basic_shapes", "text_shapes", \
								"containers", "rects", "circles", "ellipses", \
								"lines", "polylines", "polygons", "paths", \
								"texts", "text_paths", "groups"]:
			self.register_special_attribute(special_element)
			self.register_special_attribute("all_" + special_element)

	def add_shape(self, tag = None, shape_id = None, attributes = {}, fill = None, stroke = None, shape_type = Shape):
		"""
		Add a new shape to this container
		"""
		# if no shape id is specified get a numerical one
		if shape_id == None:
			global id_counter
			shape_id = id_counter
			id_counter += 1
		attributes["id"] = str(shape_id)
		shape = self.add_child_tag(tag, shape_type, attributes)
		if fill:
			shape.fill = fill
		if stroke:
			shape.stroke = stroke
		return shape

	def add_rect(self, id = None, x = None, y = None, width = None, height = None, fill = None, stroke = None, stroke_width = None, roundedx = None, roundedy = None):
		"""
		Add a rect to this container
		x,y specify the top left corner
		fill specifies the fill color
		stroke specifies the stroke color
		rx,ry specify rounded corners
		"""
		attributes = {}
		if x != None:
			attributes["x"] = x
		if y != None:
			attributes["y"] = y
		if width != None:
			attributes["width"] = width
		if height != None:
			attributes["height"] = height
		if stroke_width != None:
			attributes["stroke-width"] = stroke_width
		if roundedx != None:
			attributes["rx"] = roundedx
		if roundedy != None:
			attributes["ry"] = roundedy
		return self.add_shape("rect", id, attributes, fill, stroke, Rect)

	def add_circle(self, id = None, centerx = None, centery = None, radius = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a circle to this container
		Center is (centerx, centery)
		"""
		attributes = {}
		if centerx != None:
			attributes["cx"] = centerx
		if centery != None:
			attributes["cy"] = centery
		if radius != None:
			attributes["r"] = radius
		if stroke_width != None:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("circle", id, attributes, fill, stroke, Circle)

	def add_ellipse(self, id = None, centerx = None, centery = None, radiusx = None, radiusy = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add an ellipse into this container
		Center is (centerx, centery)
		radiusx specifies width
		radiusy specifies height
		"""
		attributes = {}
		if centerx != None:
			attributes["cx"] = centerx
		if centery != None:
			attributes["cy"] = centery
		if radiusx != None:
			attributes["rx"] = radiusx
		if radiusy != None:
			attributes["ry"] = radiusy
		if stroke_width != None:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("ellipse", id, attributes, fill, stroke, Ellipse)

	def add_line(self, id = None, startx = None, starty = None, stopx = None, stopy = None, stroke = None, stroke_width = None):
		"""
		Add a line into this container
		"""
		attributes = {}
		if startx != None:
			attributes["x1"] = startx
		if starty != None:
			attributes["y1"] = starty
		if stopx != None:
			attributes["x2"] = stopx
		if stopy != None:
			attributes["y2"] = stopy
		if stroke_width != None:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("line", id, attributes, stroke, shape_type=Line)

	def add_polyline(self, id = None, x = None, y = None, points = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a polyline into this container
		"""
		attributes = {}
		if x and y:
			attributes["points"] = [(x, y),]
		if points != None:
			attributes["points"] = points
		if stroke_width != None:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("polyline", id, attributes, fill, stroke, PolyShape)

	def add_polygon(self, id = None, x = None, y = None, points = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a polygon into this container
		"""
		attributes = {}
		if x and y:
			attributes["points"] = [(x, y),]
		if points != None:
			attributes["points"] = points
		if stroke_width != None:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("polygon", id, attributes, fill, stroke, PolyShape)

	def add_path(self, id = None, data = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a path element into this container
		"""
		attributes = {}
		if data != None:
			attributes["d"] = data
		if stroke_width != None:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("path", id, attributes, fill, stroke, Path)

	def add_text(self, id = None, x = None, y = None, deviationx = None, deviationy = None, length = None, text = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a text element into this container
		"""
		attributes = {}
		if x != None:
			attributes["x"] = x
		if y != None:
			attributes["y"] = y
		if deviationx != None:
			attributes["dx"] = deviationx
		if deviationy != None:
			attributes["dy"] = deviationy
		if length != None:
			attributes["textLength"] = length
		if stroke_width != None:
			attributes["stroke-width"] = stroke_width
		obj = self.add_shape("text", id, attributes, fill, stroke, TextContainer)
		if text:
			obj.text = text
		return obj

	def add_group(self, id = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a group element into this container
		"""
		attributes = {}
		if stroke_width != None:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("g", id, attributes, fill, stroke, Group)

class Group(Container, FilledElement, StrokedElement, TransformableElement):
	"""
	Hold and manage a container that can be transformed
	"""
	def __init__(self, element = None):
		Container.__init__(self, element)
		FilledElement.__init__(self)
		StrokedElement.__init__(self)
		TransformableElement.__init__(self)

class SVGFile(Container, Defs):
	def __init__(self, filename = None):
		if filename:
			dom = parse(filename)
			Container.__init__(self, dom.documentElement)
			self.__filename = filename
			try:
				self.__dict__["defs"] = self.get_children("defs", Defs)[0]
			except:
				self.__dict__["defs"] = self.add_child_tag("defs", Defs, { "id" : "defs" })
		else:
			# create a default SVG document
			Container.__init__(self, getDOMImplementation().createDocument(None, "svg", None).documentElement)
			self.id = "New Document"
			self.width = "48pt"
			self.height = "48pt"
			self.xmlns = "http://www.w3.org/2000/svg"
			self.set_attribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
			self.__dict__["defs"] = self.add_child_tag("defs", Defs, { "id" : "defs" })
		# register some special attributes that aren't provided for
		# a normal container class
		self.register_special_attribute("all_fills")
		self.register_special_attribute("all_gradients")
		self.register_special_attribute("all_patterns")
		self.register_special_attribute("all_linear_gradients")
		self.register_special_attribute("all_radial_gradients")
		self.register_special_attribute("all_trefs")
		self.register_special_attribute("all_tspans")

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
		Print(self.element, outfile)

	def __str__(self):
		"""
		Return the SVG's XML in a string
		"""
		class SVGString:
			def __init__(self):
				self.string = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">'

			def write(self, data):
				self.string += str(data)

		svg = SVGString()

		Print(self.element, svg)

		return svg.string

	def add_gradient(self, grad_type = None, attributes = None, grad_id = None):
		"""
		Add a gradient to this container
		gradient type, id, attributes etc... will produce a new gradient
		"""
		attributes = {}
		if not grad_id:
			global id_counter
			grad_id = id_counter
			id_counter += 1
		attributes["id"] = grad_id
		if grad_type == "linear":
			grad_class = LinearGradient
		else:
			grad_class = RadialGradient
		return self.defs.add_child_tag(grad_type + "Gradient", grad_class, attributes)

	def add_linear_gradient(self, id = None, startx = None, starty = None, stopx = None, stopy = None, xlink = None):
		"""
		Add a linear gradient to this container
		"""
		attributes = {}
		if startx != None:
			attributes["x1"] = startx
		if starty != None:
			attributes["y1"] = starty
		if stopx != None:
			attributes["x2"] = stopx
		if stopy != None:
			attributes["y2"] = stopy
		if xlink:
			attributes["xlink"] = xlink
		return self.add_gradient("linear", attributes, id)

	def add_radial_gradient(self, id = None, centerx = None, centery = None, radius = None, focusx = None, focusy = None, xlink = None):
		"""
		Add a radial gradient to this container
		center and focus are (x, y) tuples
		"""
		attributes = {}
		if centerx != None:
			attributes["cx"] = centerx
		if centery != None:
			attributes["cy"] = centery
		if radius != None:
			attributes["r"] = radius
		if focusx != None:
			attributes["fx"] = focusx
		if focusy != None:
			attributes["fy"] = focusy
		if xlink:
			attributes["xlink"] = xlink
		return self.add_gradient("radial", attributes, id)

	def add_pattern(self, id = None):
		"""
		Add a pattern to this container
		"""
		pass
