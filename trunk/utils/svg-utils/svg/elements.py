#!/usr/bin/env python

"""
	SVG Elements
	============
		Classes for SVG elements
		
		Special Attributes
		------------------
		Many of the elements have special attributes for ease of use, such as color,
		fill, and stroke attributes for easy RGBA color value access. Note that you
		can still access many original attributes through their real names:
		
			>>> element = Rect()
			>>> element.fill = "#af0033ff"
			>>> element.fill
			#af0033ff
			>>> element.get_attribute("fill-color")
			#af0033
			>>> element.get_attribute("fill-opacity")
			1.0
		
		Objects with such special elements will have the special names listed in their
		documentation.

		License
		-------
		Copyright (C) 2005 Daniel G. Taylor

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

from svgelement import SVGElement
from containers import *
from utils import get_color, set_color, handle_attributes
from error import SVGReadOnlyError

class Stop(SVGElement):
	"""
	Holds and manages a gradient stop.
	
	Special attribute:
		- color : The stop color in #RRGGBBAA format.
	
	When creating a new stop, the C{color} attribute defaults to #000000ff and
	the C{offset} defaults to 0.
	"""
	def __init__(self, attributes = {}, element = None, setdefaults = False):
		"""
		Initialize the stop.
		
		@type element: xml.dom.Element
		@param element: An existing DOM element
		"""
		SVGElement.__init__(self, element)
		if not element or setdefaults:
			if not attributes.has_key("color"): attributes["color"] = "#000000ff"
			if not attributes.has_key("offset"): attributes["offset"] = "0"
			handle_attributes(self, "stop", attributes)

	def __getattr__(self, attribute):
		"""
		Get an attribute. See L{SVGElement.__getattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The attribute being requested.
		@rtype: string
		@return: The requested attribute.
		"""
		if attribute == "color":
			color = get_color(self, SVGElement, "stop-color", "stop-opacity")
			if color: return color
		return SVGElement.__getattr__(self, attribute)

	def __setattr__(self, attribute, value):
		"""
		Set an attribute. See L{SVGElement.__setattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		"""
		if attribute == "color":
			set_color(self, SVGElement, "stop-color", "stop-opacity", value)
		else:
			SVGElement.__setattr__(self, attribute, value)

class Gradient(SVGElement, StopContainer):
	"""
	Hold and manage a gradient
	
	Note that this class should not stand alone, it is meant to help in making
	gradient classes like LinearGradient and RadialGradient!
	
	Special Attributes:
		- stops : A list of child L{Stop} elements. [Read Only]
	"""
	def __init__(self, element = None):
		"""
		Initialize the gradient.
		
		@type element: xml.dom.Element
		@param element: An existing DOM element
		"""
		SVGElement.__init__(self, element)
		StopContainer.__init__(self)
		self.__dict__["container_map"] = {"stop" : Stop}
		self.register_attribute_alias("xlink", "xlink:href")

class LinearGradient(Gradient):
	"""
	Holds and manages a linear gradient.
	
	For more information, see L{Gradient}.
	
	Special Attributes:
		- start : The [x, y] coordinate of the start of the gradient.
		- stop : The [x, y] coordinate of the stop of the gradient.
	"""
	def __init__(self, attributes = {}, element = None):
		Gradient.__init__(self, element)
		if element == None:
			handle_attributes(self, "linearGradient", attributes)
	
	def __getattr__(self, attribute):
		"""
		Get an attribute. See L{Gradient.__getattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The attribute being requested.
		@rtype: string
		@return: The requested attribute.
		"""
		if attribute == "start":
			x1 = Gradient.__getattr__(self, "x1")
			y1 = Gradient.__getattr__(self, "y1")
			return [x1, y1]
		elif attribute == "stop":
			x2 = Gradient.__getattr__(self, "x2")
			y2 = Gradient.__getattr__(self, "y2")
			return [x2, y2]
		return Gradient.__getattr__(self, attribute)
	
	def __setattr__(self, attribute, value):
		"""
		Set an attribute. See L{Gradient.__setattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		"""
		if attribute == "start":
			Gradient.__setattr__(self, "x1", value[0])
			Gradient.__setattr__(self, "y1", value[1])
		elif attribute == "stop":
			Gradient.__setattr__(self, "x2", value[0])
			Gradient.__setattr__(self, "y2", value[1])
		else:
			Gradient.__setattr__(self, attribute, value)

class RadialGradient(Gradient):
	"""
	Holds and manages a radial gradient.
	
	For more information, see L{Gradient}.
	
	Special Attributes:
		- center : The [x, y] coordinate of the center of the gradient.
		- radius : The radius of the gradient.
		- focus : The [x, y] coordinate of the focal point of the gradient.
	"""
	def __init__(self, element = None, attributes = {}):
		Gradient.__init__(self, element)
		self.register_attribute_alias("radius", "r")
		if element == None:
			handle_attributes(self, "radialGradient", attributes)
	
	def __getattr__(self, attribute):
		"""
		Get an attribute. See L{Gradient.__getattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The attribute being requested.
		@rtype: string
		@return: The requested attribute.
		"""
		if attribute == "center":
			cx = Gradient.__getattr__(self, "cx")
			cy = Gradient.__getattr__(self, "cy")
			return [cx, cy]
		elif attribute == "focus":
			fx = Gradient.__getattr__(self, "fx")
			fy = Gradient.__getattr__(self, "fy")
			return [fx, fy]
		return Gradient.__getattr__(self, attribute)
	
	def __setattr__(self, attribute, value):
		"""
		Set an attribute. See L{Gradient.__setattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		"""
		if attribute == "center":
			if len(value) != 2: raise ValueError, value
			Gradient.__setattr__(self, "cx", value[0])
			Gradient.__setattr__(self, "cy", value[1])
		elif attribute == "focus":
			if len(value) != 2: raise ValueError, value
			Gradient.__setattr__(self, "fx", value[0])
			Gradient.__setattr__(self, "fy", value[1])
		else:
			Gradient.__setattr__(self, attribute, value)

class Pattern:
	"""
	Holds and manages a pattern.
	"""
	def __init__(self, element = None):
		pass

class FilledElement:
	"""
	Helper class for filled elements. This class defines the "fill" attribute.
	
	B{This is NOT a stand-alone element! Use L{SVGElement} with it!}
	
	Special attributes:
		- fill : The fill of the element, in #RRGGBBAA form.
	"""
	def __init__(self):
		"""
		Initialize
		"""
		# The extra_check values are used by container classes!
		self.__dict__["extra_check"].append(FilledElement)
	
	def __getattr__(self, attribute):
		"""
		Get an attribute. This function is used to get the "fill" attribute;
		if the attribute being requested isn't "fill" None will be returned.
		
		@type attribute: string
		@param attribute: The name of the requested attribute.
		@rtype: string or None
		@return: The attribute's value or None.
		"""
		if attribute == "fill":
			return get_color(self, SVGElement, "fill", "fill-opacity")
		else:
			return None
	
	def __setattr__(self, attribute, value):
		"""
		Set an attribute. This function is used to set the "fill" attribute;
		if the attribute being set isn't "fill" None will be returned.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		@rtype: boolean
		@return: True if the fill was set, otherwise False.
		"""
		if attribute == "fill":
			set_color(self, SVGElement, "fill", "fill-opacity", value)
			return True
		else:
			return False

class StrokedElement:
	"""
	Helper class for stroked elements. This class defines the "stroke" attribute.
	
	B{This is NOT a stand-alone element! Use L{SVGElement} with it!}
	
	Special attributes:
		- stroke : The stroke of the element, in #RRGGBBAA form.
	"""
	def __init__(self):
		"""
		Initialize
		"""
		# The extra check values are used by container classes!
		self.__dict__["extra_check"].append(StrokedElement)
	
	def __getattr__(self, attribute):
		"""
		Get an attribute. This function is used to get the "stroke" attribute;
		if the attribute being requested isn't "stroke" None will be returned.
		
		@type attribute: string
		@param attribute: The name of the requested attribute.
		@rtype: string or None
		@return: The attribute's value or None.
		"""
		if attribute == "stroke":
			return get_color(self, SVGElement, "stroke", "stroke-opacity")
		else:
			return False
	
	def __setattr__(self, attribute, value):
		"""
		Set an attribute. This function is used to set the "stroke" attribute;
		if the attribute being set isn't "stroke" None will be returned.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		@rtype: boolean
		@return: True if the fill was set, otherwise False.
		"""
		if attribute == "stroke":
			set_color(self, SVGElement, "stroke", "stroke-opacity", value)
			return True
		else:
			return False

class TransformableElement:
	"""
	Handles and manages transformable objects. This class defines the C{translate},
	C{scale}, and C{rotate} functions for transformable elements.
	
	B{This is NOT a stand-alone element! Use L{SVGElement} with it!}
	
	This class defines the translate, rotate, and scale functions.
	"""
	def __init__(self):
		"""
		Initialize
		"""
		pass

	def __transform(self, name, attributes):
		"""
		Do a transformation. Note that currently this transformation does B{not}
		add to existing transformations, but I{overwrites them}!
		
		@type name: string
		@param name: The name of the transformation (translate, scale, or rotate).
		@type attributes: list
		@param attributes: A list of transformation attributes, such as the x and y
						   values for a linear translation.
		"""
		transform = ''
		if self.has_attribute("transform"):
			# see if an old translation is there
			# if it is, remove it and replace
			# this needs to be fixed at some point...
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
		Move a shape by x and y linear units.
		
		@type x: integer or string
		@param x: The shift in horizontal movement.
		@type y: integer or string
		@param y: The shift in vertical movement.
		"""
		attributes = []
		if x:
			attributes.append(x)
		if y:
			attributes.append(y)
		self.__transform("translate", attributes)

	def scale(self, x = None, y = None):
		"""
		Scale a shape by x and y linear units. To scale proportionately, make sure
		x and y are equal.
		
		@type x: integer or string
		@param x: The amount of horizontal scaling.
		@type y: integer or string
		@param y: The amount of vertical scaling.
		"""
		attributes = []
		if x:
			attributes.append(x)
		if y:
			attributes.append(y)
		self.__transform("scale", attributes)

	def rotate(self, degrees, centerx = None, centery = None):
		"""
		Rotate a shape in degrees, around the point (centerx, centery).
		
		@type degrees: integer or string
		@param degrees: The amount of rotation in degrees.
		@type centerx: integer or string
		@param centerx: The horizontal value of the center of rotation.
		@type centery: integer or string
		@param centery: The vertical value of the center of rotation.
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
	Holds normal colorable, transformable shapes (excluding lines).
	
	This is just a class to combine some previously defined classes to make life
	easier later (as many shapes will now just have to inherit the Shape class).
	See the inherited classes for more information.
	
	Use this class to create new elements that can have fill/stroke values and
	can have transformations applied to them.
	"""
	def __init__(self, element = None):
		"""
		Initialize
		
		@type element: xml.dom.Element
		@param element: An existing XML DOM element object to encapsulate.
		"""
		SVGElement.__init__(self, element)
		FilledElement.__init__(self)
		StrokedElement.__init__(self)
		TransformableElement.__init__(self)
		self.__dict__["container_map"] = {}

class Rect(Shape):
	"""
	Holds a rectangle shape (an SVG rect).
	
	Special attributes:
		- dimensions : The [x, y, width, height] of the rectangle.
			(measured from the top left corner)
		- roundedx : Amount of horizontal roundness of the rectangle's corners.
		- roundedy : Amount of vertical roundness of the rectangle's corners.
	
	The dimensions default to [0, 0, 100, 100] and the fill defaults to solid black
	on new rectangles.
	"""
	def __init__(self, attributes = {}, element = None, setdefaults = False):
		Shape.__init__(self, element)
		self.register_attribute_alias("roundedx", "rx")
		self.register_attribute_alias("roundedy", "ry")
		if not element or setdefaults:
			if not attributes.has_key("dimensions"):
				if not attributes.has_key("x"): attributes["x"] = 0
				if not attributes.has_key("y"): attributes["y"] = 0
				if not attributes.has_key("width"): attributes["width"] = "100"
				if not attributes.has_key("height"): attributes["height"] = "100"
			self.fill = "#000000ff"
			handle_attributes(self, "rect", attributes)
	
	def __getattr__(self, attribute):
		"""
		Get an attribute. See L{SVGElement.__getattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The attribute being requested.
		@rtype: string
		@return: The requested attribute.
		"""
		if attribute == "dimensions":
			x = Shape.__getattr__(self, "x")
			y = Shape.__getattr__(self, "y")
			width = Shape.__getattr__(self, "width")
			height = Shape.__getattr__(self, "height")
			return [x, y, width, height]
		return Shape.__getattr__(self, attribute)
	
	def __setattr__(self, attribute, value):
		"""
		Set an attribute. See L{SVGElement.__setattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		"""
		if attribute == "dimensions":
			if len(value) != 4: raise ValueError, value
			Shape.__setattr__(self, "x", value[0])
			Shape.__setattr__(self, "y", value[1])
			Shape.__setattr__(self, "width", value[2])
			Shape.__setattr__(self, "height", value[3])
		else:
			Shape.__setattr__(self, attribute, value)

class Circle(Shape):
	"""
	Holds a circle shape (an SVG circle).
	
	Special attributes:
		- center : The [x, y] coordinate of the center of the circle.
		- radius : The radius of the circle.
	
	The center defaults to [0, 0], the radius defaults to 50, and the fill
	defaults to solid black on new circles.
	"""
	def __init__(self, attributes = {}, element = None, setdefaults = False):
		Shape.__init__(self, element)
		self.register_attribute_alias("radius", "r")
		if not element or setdefaults:
			if not attributes.has_key("center"):
				if not attributes.has_key("cx"): attributes["cx"] = 0
				if not attributes.has_key("cy"): attributes["cy"] = 0
			if not attributes.has_key("radius"):
				if not attributes.has_key("r"): attributes["r"] = 50
			if not attributes.has_key("fill"): attributes["fill"] = "#000000ff"
			handle_attributes(self, "circle", attributes)
	
	def __getattr__(self, attribute):
		"""
		Get an attribute. See L{SVGElement.__getattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The attribute being requested.
		@rtype: string
		@return: The requested attribute.
		"""
		if attribute == "center":
			cx = Shape.__getattr__(self, "cx")
			cy = Shape.__getattr__(self, "cy")
			return [cx, cy]
		return Shape.__getattr__(self, attribute)
	
	def __setattr__(self, attribute, value):
		"""
		Set an attribute. See L{SVGElement.__setattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		"""
		if attribute == "center":
			if len(value) != 2: raise ValueError, value
			Shape.__setattr__(self, "cx", value[0])
			Shape.__setattr__(self, "cy", value[1])
		else:
			Shape.__setattr__(self, attribute, value)

class Ellipse(Shape):
	"""
	Holds an ellipse shape (an SVG ellipse).
	
	Special attributes:
		- center : The [x, y] coordinate of the center of the elllpse.
		- radius : The [x, y] lengths of the radius.
	
	Center defaults to [0, 0], radius defaults to [50, 100], and the fill
	defaults to a solid black on new ellipses.
	"""
	def __init__(self, attributes = {}, element = None, setdefaults = False):
		Shape.__init__(self, element)
		if not element or setdefaults:
			if not attributes.has_key("center"):
				if not attributes.has_key("cx"): attributes["cx"] = 0
				if not attributes.has_key("cy"): attributes["cy"] = 0
			if not attributes.has_key("radius"):
				if not attributes.has_key("rx"): attributes["rx"] = 50
				if not attributes.has_key("ry"): attributes["ry"] = 100
			if not attributes.has_key("fill"): attributes["fill"] = "#000000ff"
			handle_attributes(self, "ellipse", attributes)
	
	def __getattr__(self, attribute):
		"""
		Get an attribute. See L{SVGElement.__getattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The attribute being requested.
		@rtype: string
		@return: The requested attribute.
		"""
		if attribute == "center":
			cx = Shape.__getattr__(self, "cx")
			cy = Shape.__getattr__(self, "cy")
			return [cx, cy]
		if attribute == "radius":
			rx = Shape.__getattr__(self, "rx")
			ry = Shape.__getattr__(self, "ry")
			return [rx, ry]
		return Shape.__getattr__(self, attribute)
	
	def __setattr__(self, attribute, value):
		"""
		Set an attribute. See L{SVGElement.__setattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		"""
		if attribute == "center":
			if len(value) != 2: raise ValueError, value
			Shape.__setattr__(self, "cx", value[0])
			Shape.__setattr__(self, "cy", value[1])
		elif attribute == "radius":
			if len(value) != 2: raise ValueError, value
			Shape.__setattr__(self, "rx", value[0])
			Shape.__setattr__(self, "ry", value[1])
		else:
			Shape.__setattr__(self, attribute, value)

class Line(SVGElement, StrokedElement, TransformableElement):
	"""
	Holds a line element (an SVG line).
	
	Note that this class does B{not} have a fill value.
	
	Special attributes:
		- start: The [x, y] coordinates of the start of the line.
		- stop: The [x, y] coordinates of the end of the line.
	"""
	def __init__(self, attributes = {}, element = None, setdefaults = False):
		SVGElement.__init__(self, element)
		StrokedElement.__init__(self)
		TransformableElement.__init__(self)
		if not element or setdefaults:
			if not attributes.has_key("start"):
				if not attributes.has_key("x1"): attributes["x1"] = 0
				if not attributes.has_key("y1"): attributes["y1"] = 0
			if not attributes.has_key("stop"):
				if not attributes.has_key("x2"): attributes["x2"] = 50
				if not attributes.has_key("y2"): attributes["y2"] = 50
			if not attributes.has_key("stroke"):
				attributes["stroke"] = "#000000ff"
			handle_attributes(self, "line", attributes)
	
	def __getattr__(self, attribute):
		"""
		Get an attribute. See L{SVGElement.__getattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The attribute being requested.
		@rtype: string
		@return: The requested attribute.
		"""
		if attribute == "start":
			x1 = SVGElement.__getattr__(self, "x1")
			y1 = SVGElement.__getattr__(self, "y1")
			return [x1, y1]
		if attribute == "stop":
			x2 = SVGElement.__getattr__(self, "x2")
			y2 = SVGElement.__getattr__(self, "y2")
			return [x2, y2]
		try:
			return StrokedElement.__getattr__(self, attribute)
		except:
			return SVGElement.__getattr__(self, attribute)
	
	def __setattr__(self, attribute, value):
		"""
		Set an attribute. See L{SVGElement.__setattr__} for more information, as
		this function passes on unresolved attributes to it.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		"""
		if attribute == "start":
			if len(value) != 2: raise ValueError, value
			SVGElement.__setattr__(self, "x1", value[0])
			SVGElement.__setattr__(self, "y1", value[1])
		elif attribute == "stop":
			if len(value) != 2: raise ValueError, value
			SVGElement.__setattr__(self, "x2", value[0])
			SVGElement.__setattr__(self, "y2", value[1])
		else:
			if not StrokedElement.__setattr__(self, attribute, value):
				SVGElement.__setattr__(self, attribute, value)

class PolyShape(Shape):
	"""
	Holds a polyline/polygon (SVG polyline and polygon).
	
	Special attributes:
		- points : The points of the polyshape, as defined by the SVG specification.
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
	Hold and manage a path element (an SVG path).
	
	Special attributes:
		- data : The path data, as defined by the SVG specification.
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
		Add a bezier curve to this path [unimplemented]
		"""
		pass

	def curveto_smooth(self, curve_node_x, curve_node_y, x, y, relative = False):
		"""
		Add a smooth bezier curve to this path [unimplemented]
		"""
		pass

	def clear(self):
		"""
		Clear the path
		"""
		self.d = ''

class Text(Shape, TextElementContainer):
	"""
	Holds a text element.
	
	This element can hold L{Tspan} and L{Tref} elements.
	
	Special attributes:
		- text : The text to be displayed.
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		TextElementContainer.__init__(self)
		self.__dict__["container_map"]["tref"] = Tref
		self.__dict__["container_map"]["tspan"] = Tspan

class Tref(Shape):
	"""
	Holds a tref element.
	
	Special attributes:
		- xlink : The link to the element this element is referencing.
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		self.register_attribute_alias("xlink", "xlink:href")

class Tspan(Shape, TextElementContainer):
	"""
	Holds a tspan element.

	This element can hold L{Tspan} and L{Tref} elements.
	
	Special attributes:
		- text : The text to be displayed.
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		TextElementContainer.__init__(self)
		self.__dict__["container_map"]["tref"] = Tref
		self.__dict__["container_map"]["tspan"] = Tspan

class TextPath(SVGElement, TransformableElement, TextElementContainer):
	"""
	Holds a textPath element. This element can hold L{Tref} and L{Tspan}
	elements.
	
	Special attributes:
		- xlink : A link to a L{Tref} or L{Tspan} element.
	"""
	def __init__(self, element = None):
		SVGElement.__init__(self, element)
		TransformableElement.__init__(self)
		TextElementContainer.__init__(self)
		self.register_attribute_alias("xlink", "xlink:href")
		self.__dict__["container_map"]["tref"] = Tref
		self.__dict__["container_map"]["tspan"] = Tspan

class Defs(SVGElement, DefinitionContainer):
	"""
	Holds a definition element (defs).
	
	See the inherited classes for more information.
	"""
	def __init__(self, element = None, attributes = {}):
		SVGElement.__init__(self, element)
		DefinitionContainer.__init__(self)
		if not self.__dict__.has_key("container_map"):
			self.__dict__["container_map"] = {}
		self.__dict__["container_map"]["linear_gradient"] = LinearGradient
		self.__dict__["container_map"]["radial_gradient"] = RadialGradient
		self.__dict__["container_map"]["pattern"] = Pattern
		if element == None:
			handle_attributes(self, "defs", attributes)

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

class Group(Shape, ShapeContainer):
	"""
	Hold and manage a container that can be transformed
	"""
	def __init__(self, element = None):
		Shape.__init__(self, element)
		ShapeContainer.__init__(self)
		self.__dict__["container_map"]["rect"] = Rect
		self.__dict__["container_map"]["circle"] = Circle
		self.__dict__["container_map"]["ellipse"] = Ellipse
		self.__dict__["container_map"]["line"] = Line
		self.__dict__["container_map"]["polyline"] = PolyShape
		self.__dict__["container_map"]["polygon"] = PolyShape
		self.__dict__["container_map"]["path"] = Path
		self.__dict__["container_map"]["group"] = Group
		if element == None:
			handle_attributes(self, "group", {})
