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
from xml.dom.ext import PrettyPrint
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
	elif element.tag in ["svg", "defs", "g", "text"]:
		# container objects
		search = []

		if attribute in ["linear_gradients", "gradients", "fills"]:
			search.append(("linearGradient", LinearGradient))
		if attribute in ["radial_gradients", "gradients", "fills"]:
			search.append(("radialGradient", RadialGradient))
		if attribute in ["patterns", "fills"]:
			search.append(("pattern", TransformableContainer))
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
		self.register_attribute_alias("xlink", "xlink:href")

	def _get_attribute(self, attribute):
		"""
		Catch calls to the gradient's stops and such
		"""
		if attribute in ["stops"]:
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
		return False

	def add_stop(self, id = None, color = "#00000000", offset = "1"):
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

class Line(TransformableElement):
	"""
	Holds a line element
	"""
	def __init__(self, element = None):
		TransformableElement.__init__(self, element)
		self.register_attribute_alias("startx", "x1")
		self.register_attribute_alias("starty", "y1")
		self.register_attribute_alias("stopx", "x2")
		self.register_attribute_alias("stopy", "y2")

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

class PolyShape(Shape):
	"""
	Holds a polyline/polygon
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Handle calls to get stroke value
		"""
		if attribute in ["fill", "stroke", "points"]:
			return get_special_attribute(self, attribute)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Handle calls to set stroke value
		"""
		if attribute in ["fill", "stroke", "points"]:
			return set_special_attribute(self, attribute, value)
		return False

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
			char = "l"
		else: char = "L"
		self.d += " " + char + " " + str(x) + "," + str(y)

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

class TextElement(TransformableElement):
	"""
	Holds an element containing text
	"""
	def __init__(self, element = None):
		TransformableElement.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Handle calls to get special variables
		"""
		if attribute in ["fill", "stroke", "text"]:
			return get_special_attribute(self, attribute)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Handle calls to set special variables
		"""
		if attribute in ["fill", "stroke", "text"]:
			return set_special_attribute(self, attribute, value)
		return False

class Tref(TransformableElement):
	"""
	Holds a tref element
	"""
	def __init__(self, element = None):
		TransformableElement.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Handle calls to get special variables
		"""
		if attribute in ["fill", "stroke", "text"]:
			return get_special_attribute(self, attribute)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Handle calls to set special variables
		"""
		if attribute in ["fill", "stroke", "text"]:
			return set_special_attribute(self, attribute, value)
		return False

class TextContainer(TransformableElement):
	"""
	Holds a text container
	"""
	def __init__(self, element = None):
		TransformableElement.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Handle calls to get special variables
		"""
		if attribute in ["fill", "stroke", "text", "tspans", "trefs"]:
			return get_special_attribute(self, attribute)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Handle calls to set special variables
		"""
		if attribute in ["fill", "stroke", "text"]:
			return set_special_attribute(self, attribute, value)
		return False

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

class TextPath(TransformableElement):
	"""
	Holds a textPath element
	"""
	def __init__(self, element = None):
		TransformableElement.__init__(self, element)

	def _get_attribute(self, attribute):
		"""
		Handle calls to get special variables
		"""
		if attribute in ["xlink", "text"]:
			return get_special_attribute(self, attribute)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Handle calls to set special variables
		"""
		if attribute in ["xlink", "text"]:
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
		if attribute[:4] == "all_":
			recursive = True
			attribute = attribute[4:]
		else:
			recursive = False
		if attribute in ["linear_gradients", "radial_gradients", "gradients", \
						"patterns", "rects", "circles", "ellipses", "lines", \
						"polylines", "polygons", "paths", "texts", "tspans", \
						"trefs", "text_paths", "fills", "basic_shapes", \
						"text_shapes", "shapes", "defs", "groups", "containers"]:
			return get_special_attribute(self, attribute, recursive)
		return None, True

	def _set_attribute(self, attribute, value):
		"""
		Handle attribute setting
		"""
		if attribute[:4] == "all_":
			attribute = attribute[4:]
		if attribute in ["linear_gradients", "radial_gradients", "gradients", \
						"patterns", "rects", "circles", "ellipses", "lines", \
						"polylines", "polygons", "paths", "texts", "tspans", \
						"trefs", "text_paths", "fills", "basic_shapes", \
						"text_shapes", "shapes", "defs", "groups", "containers"]:
			raise ReadOnlyError, "Cannot directly set " + attribute + "!\n" \
								"To add an object, use the add_* functions, and " \
								"to remove an object call its unlink() method!"
		return False

	def add_gradient(self, grad_type = None, attributes = None, grad_id = None, element = None):
		"""
		Add a gradient to this container
		Either element can be specified (and should be a Gradient object)
		OR
		gradient type, id, attributes etc... will produce a new gradient
		"""
		if element:
			self.element.appendChild(element.element)
			return element
		else:
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

	def add_shape(self, tag = None, shape_id = None, attributes = {}, fill = None, stroke = None, shape_type = Shape, element = None):
		"""
		Add an object to this container
		Either element can be specified (and it should be one of these shape/text classes
		OR
		A tag, shape_id, attributes, etc... can be specified and a new shape will be added
		"""
		if element:
			self.element.appendChild(element.element)
			return element
		else:
			# if no shape id is specified get a numerical one
			if not shape_id:
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
		if roundedx:
			attributes["rx"] = roundedx
		if roundedy:
			attributes["ry"] = roundedy
		return self.add_shape("rect", id, attributes, fill, stroke, Rect)

	def add_circle(self, id = None, centerx = None, centery = None, radius = None, fill = None, stroke = None, stroke_width = None):
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
		return self.add_shape("circle", id, attributes, fill, stroke, Circle)

	def add_ellipse(self, id = None, centerx = None, centery = None, radiusx = None, radiusy = None, fill = None, stroke = None, stroke_width = None):
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
		return self.add_shape("ellipse", id, attributes, fill, stroke, Ellipse)

	def add_line(self, id = None, startx = None, starty = None, stopx = None, stopy = None, stroke = None, stroke_width = None):
		"""
		Add a line into this container
		"""
		attributes = {}
		if startx:
			attributes["x1"] = startx
		if starty:
			attributes["y1"] = starty
		if stopx:
			attributes["x2"] = stopx
		if stopy:
			attributes["y2"] = stopy
		if stroke_width:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("line", id, attributes, stroke, shape_type=Line)

	def add_polyline(self, id = None, x = None, y = None, points = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a polyline into this container
		"""
		attributes = {}
		if x and y:
			attributes["points"] = [(x, y),]
		if points:
			attributes["points"] = points
		if stroke_width:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("polyline", id, attributes, fill, stroke, PolyShape)

	def add_polygon(self, id = None, x = None, y = None, points = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a polygon into this container
		"""
		attributes = {}
		if x and y:
			attributes["points"] = [(x, y),]
		if points:
			attributes["points"] = points
		if stroke_width:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("polygon", id, attributes, fill, stroke, PolyShape)

	def add_path(self, id = None, data = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a path element into this container
		"""
		attributes = {}
		if data:
			attributes["d"] = data
		if stroke_width:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("path", id, attributes, fill, stroke, Path)

	def add_text(self, id = None, x = None, y = None, deviationx = None, deviationy = None, length = None, text = None, fill = None, stroke = None, stroke_width = None):
		"""
		Add a text element into this container
		"""
		attributes = {}
		if x:
			attributes["x"] = x
		if y:
			attributes["y"] = y
		if deviationx:
			attributes["dx"] = deviationx
		if deviationy:
			attributes["dy"] = deviationy
		if length:
			attributes["textLength"] = length
		if stroke_width:
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
		if stroke_width:
			attributes["stroke-width"] = stroke_width
		return self.add_shape("g", id, fill, stroke, attributes, Group)

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
		if attribute[:4] == "all_":
			recursive = True
			attribute = attribute[4:]
		else:
			recursive = False
		if attribute in ["linear_gradients", "radial_gradients", "gradients", \
						"patterns", "rects", "circles", "ellipses", "lines", \
						"polylines", "polygons", "paths", "texts", "tspans", \
						"trefs", "text_paths", "fills", "basic_shapes", \
						"text_shapes", "shapes", "defs", "groups", "containers"]:
			return get_special_attribute(self, attribute)

	def _set_attribute(self, attribute, value):
		"""
		Handle attribute setting
		"""
		if attribute[:4] == "all_":
			attribute = attribute[4:]
		if attribute in ["linear_gradients", "radial_gradients", "gradients", \
						"patterns", "rects", "circles", "ellipses", "lines", \
						"polylines", "polygons", "paths", "texts", "tspans", \
						"trefs", "text_paths", "fills", "basic_shapes", \
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
			try:
				self.__dict__["defs"] = self.get_children("defs", Container)[0]
			except:
				self.__dict__["defs"] = self.add_child_tag("defs", Container, { "id" : "defs" })
		else:
			# create a default SVG document
			XMLElement.__init__(self, getDOMImplementation().createDocument(None, "svg", None).documentElement)
			self.id = "New Document"
			self.width = "48pt"
			self.height = "48pt"
			self.xmlns = "http://www.w3.org/2000/svg"
			self.set_attribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
			self.__dict__["defs"] = self.add_child_tag("defs", Container, { "id" : "defs" })

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
