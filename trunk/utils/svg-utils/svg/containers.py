#!/usr/bin/env python

"""
	Containers
	==========
		Helper classes for container elements.
		
		Using Container Helper Classes
		------------------------------
		In general, two things need to be done to use a container helper class.
			1. Inherit the container helper class. This is the easiest part :-)
				- C{class Test(SVGElement, Container):}
			2. Define the required container maps. These are map names that are used
			   by the helper classes to create new objects.
				- C{self.__dict__["container_maps"]["class"] = Class}
				
		As an example take a look at the L{Gradient<svg.elements.Gradient>} class.
		
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

from xml.dom.minidom import Document

from error import SVGReadOnlyError
from utils import get_new_id
import log

class StopContainer:
	"""
	A container helper class to hold L{Stop<svg.elements.Stop>} objects. This is
	not a stand-alone class and should be used in conjunction with an
	L{XMLElement<svg.svgelement.XMLElement>}-based class.
	
	This class will respond to C{stops} and C{all_stops}, both of whic are
	read-only
	
	If you use this class, you should make sure your class has
	C{self.__dict__["container_map"]["stop"]} defined, as this class uses it to
	create new stops. Generally it should just be the L{Stop<svg.elements.Stop>}
	class.
	"""
	def __init__(self):
		"""
		Initialize
		"""
		self.__dict__["extra_check"].append(StopContainer)
	
	def __getattr__(self, attribute):
		"""
		Get the value an attribute. Note that this function only handles special
		attributes that pertain to this container.
		
		@type attribute: string
		@param attribute: The name of the requested attribute.
		@rtype: string or list
		@return: Returns the value of the requested attribute.
		"""
		# see if we are requesting direct descendents or all children
		try:
			recurse = attribute[:4] == "all_" and True or False
		except: recurse = False
		
		if attribute in ["stops", "all_stops"]:
			return self.get_children("stop", self.__dict__["container_map"]["stop"], recurse)
		else:
			return None
	
	def __setattr__(self, attribute, value):
		"""
		Set the value of an attribute. Note that this function only handles special
		attributes that pertain to this container.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		@rtype: boolean
		@return: True on attribute set, False if this function doesn't handle
				 this attribute, which can be used to send it along to an
				 L{XMLElement<svg.svgelement.XMLElement>}-based class.
		"""
		if attribute in ["stops", "all_stops"]:
			log.error(attribute + " is read-only!")
			raise SVGReadOnlyError, attribute
		else:
			return False
	
	def create_stop(self, id = None, color = "#000000ff", offset = "1"):
		"""
		Append a gradient stop as a child.
		
		@type id: string
		@param id: The unique ID of the stop. One will be generated if none is passed.
		@type color: string
		@param color: The color value of the stop. It can be either a named color or
					  a color in #RRGGBBAA form.
		@type offset: float
		@param offset: The offset of the gradient, which should be a value between
					   0.0 and 1.0.
		@rtype: L{Stop<svg.elements.Stop>}
		@return: The newly created L{Stop<svg.elements.Stop>} element.
		"""
		if id == None:
			id = get_new_id()
		stop = self.create_child("stop", self.__dict__["container_map"]["stop"],
						{ "id" : str(id), "color" : color, "offset" : offset })
		return stop

class TextElementContainer:
	"""
	A container helper class to hold Text, Tspan and Tref objects. This is
	not a stand-alone class and should be used in conjunction with an
	L{XMLElement<svg.svgelement.XMLElement>}-based class.
	
	This class will respond to C{tspans}, C{all_tspans}, C{trefs}, C{all_trefs},
	and C{text} attribute requests. Only the C{text} attribute can be written to.
	
	Setting the text attribute is easy: C{container.text = "My text"}.
	
	If you use this class, you should make sure your class has certain values in
	C{self.__dict__["container_map"]} defined, as this class uses it to
	create new elements. The elements you want to define are as follows:
		- tspan
		- tref
	"""
	def __init__(self):
		self.__dict__["extra_check"].append(TextElementContainer)
	
	def __getattr__(self, attribute):
		"""
		Get the value an attribute. Note that this function only handles special
		attributes that pertain to this container.
		
		@type attribute: string
		@param attribute: The name of the requested attribute.
		@rtype: string or list
		@return: Returns the value of the requested attribute.
		"""
		# see if we are requesting direct descendents or all children
		try:
			recurse = attribute[:4] == "all_" and True or False
		except: recurse = False
		
		if attribute == "text":
			if recurse: log.warning("There is no need for 'all_' in front of the text attribute!")
			text = ''
			for child in self.__dict__["element"].childNodes:
				if child.nodeType == child.TEXT_NODE:
					text += child.data.strip()
			return text
		elif attribute in ["tspans", "all_tspans"]:
			return self.get_children("tspan", self.__dict__["container_map"]["tspan"], recurse)
		elif attribute in ["trefs", "all_trefs"]:
			return self.get_children("tref", self.__dict__["container_map"]["tref"], recurse)
		else:
			return None
	
	def __setattr__(self, attribute, value):
		"""
		Set the value of an attribute. Note that this function only handles special
		attributes that pertain to this container.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		@rtype: boolean
		@return: True on attribute set, False if this function doesn't handle
				 this attribute, which can be used to send it along to an
				 L{XMLElement<svg.svgelement.XMLElement>}-based class.
		"""
		if attribute == "text":
			for node in self.__dict__["element"].childNodes:
				if node.nodeType == node.TEXT_NODE:
					self.__dict__["element"].removeChild(node)
			self.__dict__["element"].appendChild(Document().createTextNode(value))
		elif attribute in ["tspans", "all_tspans", "trefs", "all_trefs"]:
			log.error(attribute + " is read-only!")
			raise SVGReadOnlyError, attribute
		else:
			return False
	
	def create_tspan(self, id = None, text = None, pos = [0, 0], deviation = None,
					 rotation = None, length = None, font_weight = None,
					 fill = None, stroke = None):
		"""
		Create a tspan object within this container.
		
		@type id: string or number
		@param id: A unique identifier for this L{Tspan<svg.elements.Tspan>} element.
		@type text: string
		@param text: The text that this tspan holds.
		@type pos: list
		@param pos: [x, y] coordinates of the L{Tspan<svg.elements.Tspan>} element.
		@type deviation: list
		@param deviation: [x, y] deviation amount.
		@type rotation: number
		@param rotation: The number of degrees the text is rotated.
		@type length: number
		@param length: The length of the text.
		@type font_weight: number
		@param font_weight: The boldness of the text's font.
		@type fill: #RRGGBBAA form color
		@param fill: The fill value of this text.
		@type stroke: #RRGGBBAA form color
		@param stroke: The stroke value of the text.
		"""
		if id == None or id == "":
			id = get_new_id("tspan")
		attributes = {"id" : tspan_id, "x" : pos[0], "y" : pos[1]}
		if text: attributes["text"] = text
		if deviation:
			attributes["dx"] = deviation[0]
			attributes["dy"] = deviation[1]
		if rotation: attributes["rotation"] = rotation
		if length: attributes["length"] = length
		if font_weight: attributes["font-weight"] = font_weight
		
		tspan = self.add_child_tag("tspan", self.__dict__["container_map"]["tspan"], attributes)
		
		# do this because the fill/stroke are special attributes!
		if fill: tspan.fill = fill
		if stroke: tspan.stroke = stroke
		
		return tspan
	
	def create_tref(self, id = None, xlink = None, text = None, pos = [0, 0],
					deviation = None, rotation = None, length = None,
					font_weight = None, fill = None, stroke = None):
		"""
		Create a tref object within this container.
		
		@type id: string or number
		@param id: A unique identifier for this L{Tref<svg.elements.Tref>} element.
		@type text: string
		@param text: The text that this tref holds.
		@type pos: list
		@param pos: [x, y] cooridnates of this L{Tref<svg.elements.Tref>} element.
		@type deviation: list
		@param deviation: [x, y] deviation amount.
		@type rotation: number
		@param rotation: The number of degrees the text is rotated.
		@type length: number
		@param length: The length of the text.
		@type font_weight: number
		@param font_weight: The boldness of the text's font.
		@type fill: #RRGGBBAA form color
		@param fill: The fill value of this text.
		@type stroke: #RRGGBBAA form color
		@param stroke: The stroke value of the text.
		"""
		if id == None or id == "":
			id = get_new_id("tref")
		attributes = {"id" : tref_id, "x" : pos[0], "y" : pos[1]}
		if text: attributes["text"] = text
		if deviation:
			attributes["dx"] = deviation[0]
			attributes["dy"] = deviation[1]
		if rotation: attributes["rotation"] = rotation
		if length: attributes["length"] = length
		if font_weight: attributes["font-weight"] = font_weight
		
		tref = self.add_child_tag("tref", self.__dict__["container_map"]["tref"], attributes)
		
		# do this because the fill/stroke are special attributes!
		if fill: tref.fill = fill
		if stroke: tref.stroke = stroke
		
		return tref

class DefinitionContainer:
	"""
	A container helper class to hold gradient and fill definitions. This is
	not a stand-alone class and should be used in conjunction with an
	L{XMLElement<svg.svgelement.XMLElement>}-based class.
	
	This class will respond to C{gradients}, C{linear_gradients},
	C{radial_gradients}, C{fills}, and C{patterns}, all of which are read-only.
	
	The layout of those attributes is as such::
	
		- fills
			|
			- gradients
			|	|
			|	- linear_gradients
			|	|
			|	- radial_gradients
			|
			- patterns
	
	So, C{fills} will return all gradients and patterns, C{gradients} will return
	all linear and radial gradients. Each element will be returned using the
	correct class, e.g. fills will return linear_gradients using the
	linear_gradient class defined in the container map.
	
	If you use this class, you should make sure your class has certain elements
	in C{self.__dict__["container_map"]} defined, specifically:
		- linear_gradient
		- radial_gradient
		- pattern
	"""
	def __init__(self):
		"""
		Initialize
		"""
		self.__dict__["extra_check"].append(DefinitionContainer)
	
	def __getattr__(self, attribute):
		"""
		Get the value an attribute. Note that this function only handles special
		attributes that pertain to this container.
		
		@type attribute: string
		@param attribute: The name of the requested attribute.
		@rtype: string or list
		@return: Returns the value of the requested attribute.
		"""
		if attribute in ["fills", "gradients", "linear_gradients", "radial_gradients",
						 "patterns"]:
			elements = []
			if attribute in ["fills", "gradients", "linear_gradients"]:
				elements += self.get_children("linearGradient",
							self.__dict__["container_map"]["linear_gradient"], False)
			if attribute in ["fills", "gradients", "radial_gradients"]:
				elements += self.get_children("radialGradient",
							self.__dict__["container_map"]["radial_gradient"], False)
			if attribute in ["fills", "patterns"]:
				elements += self.get_children("pattern",
							self.__dict__["container_map"]["pattern"], False)
			return elements
		else:
			return None
	
	def __setattr__(self, attribute, value):
		"""
		Set the value of an attribute. Note that this function only handles special
		attributes that pertain to this container.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		@rtype: boolean
		@return: True on attribute set, False if this function doesn't handle
				 this attribute, which can be used to send it along to an
				 L{XMLElement<svg.svgelement.XMLElement>}-based class.
		"""
		if attribute in ["fills", "gradients", "linear_gradients", "radial_gradients",
						 "patterns"]:
			log.error(attribute + " is read-only!")
			raise SVGReadOnlyError, attribute
		else:
			return False
	
	def create_linear_gradient(self, id = None, start = None, stop = None, xlink = None):
		"""
		Create a new L{linear gradient<svg.elements.LinearGradient>} within this container.
		
		Note that you need to define either start/end or an xlink for the gradient. You can
		also just create a blank gradient and add them later, but don't specify both.
		
		@type id: string
		@param id: A unique identifier for this L{gradient<svg.elements.LinearGradient>}.
		@type start: list
		@param start: The [x, y] coordinates of the start of the gradient.
		@type stop: list
		@param stop: The [x, y] coordinate of the stop of the gradient.
		@type xlink: string
		@param xlink: A link to a defined gradient's identifier.
		"""
		if not id:
			id = get_new_id("linearGradient")
		attributes = { "id" : id }
		if start:
			if not stop: log.warning("Please specify stop coordinates for the gradient!")
			attributes["x1"] = start[0]
			attributes["y1"] = start[1]
		if stop:
			if not start: log.warning("Please specify start coordinates for the gradient!")
			attributes["x2"] = stop[0]
			attributes["y2"] = stop[1]
		if xlink:
			if start or stop:
				log.warning("You may not want to specify a start/stop and xlink!")
			attributes["xlink"] = xlink
		return self.create_child("linearGradient",
					self.__dict__["container_map"]["linear_gradient"], attributes)
	
	def create_radial_gradient(self, id = None, center = None, radius = None, focus = None,
							   xlink = None):
		"""
		Create a new L{radial gradient<svg.elements.RadialGradient>} within this container.
		
		Make sure you specify either center/radius or an xlink, but not both. You can
		also just create a blank gradient and add the attributes later.
		
		@type id: string
		@param id: A unique identifier for this L{radial gradient<svg.elements.RadialGradient>}.
		@type center: list
		@param center: The [x, y] coordinates of the center of the gradient.
		@type radius: string or number
		@param radius: The radius of the gradient.
		@type focus: list
		@param focus: The [x, y] coordinates of the focal point of the gradient.
		@type xlink: string
		@param xlink: A link to a defined gradient's identifier.
		"""
		if not id:
			id = get_net_id("radialGradient")
		attributes = { "id" : id }
		if center:
			if not radius: log.warning("Please specify a radius for the gradient!")
			attributes["cx"] = center[0]
			attributes["cy"] = center[0]
		if radius:
			if not center: log.warning("Please specify a center for the gradient!")
			attributes["r"] = radius
		if focus:
			if not (center and radius):
				log.warning("Please specify a radius and center for the gradient!")
			attributes["fx"] = focus[0]
			attributes["fy"] = focus[1]
		if xlink:
			if center or radius:
				log.warning("You may not want to specify a center/radius and xlink!")
			attributes["xlink"] = xlink
		return self.create_child("radialGradient",
					self.__dict__["container_map"]["radial_gradient"], attributes)
	
	def create_pattern(self, id = None):
		"""
		Create a new pattern in this container.
		
		@type id: string
		@param id: A unique identifier for the L{pattern<svg.elements.Pattern>}.
		"""
		if not id:
			id = get_new_id("pattern")
		attributes = { "id" : id }
		return self.add_child_tag("pattern",
					self.__dict__["container_map"]["pattern"], attributes)

class ShapeContainer:
	"""
	A container helper class to hold shapes. This is
	not a stand-alone class and should be used in conjunction with an
	L{XMLElement<svg.svgelement.XMLElement>}-based class.
	
	This class will respond to C{shapes}, C{rects}, C{circles}, C{ellipses},
	C{lines}, C{polylines}, C{polygons}, C{paths}, and C{groups}, all of which
	are read-only.
	
	The layout of those attributes is as such::
	
		- shapes
			- rects
			- circles
			- ellipses
			- lines
			- polylines
			- polygons
			- paths
			- groups
	
	So, C{shapes} will return all of the shapes that are direct children of this
	container. C{all_shapes} will return all of the shapes below this container.
	Each element will be returned using the correct class as defined in the
	container map.
	
	If you use this class, you should make sure your class has certain elements
	in C{self.__dict__["container_map"]} defined, specifically:
		- rect
		- circle
		- ellipse
		- line
		- polyline
		- polygon
		- path
		- group
	"""
	def __init__(self):
		"""
		Initialize
		"""
		self.__dict__["extra_check"].append(ShapeContainer)
	
	def __getattr__(self, attribute):
		"""
		Get the value an attribute. Note that this function only handles special
		attributes that pertain to this container.
		
		@type attribute: string
		@param attribute: The name of the requested attribute.
		@rtype: string or list
		@return: Returns the value of the requested attribute.
		"""
		recursive = False
		if attribute[:4] == "all_":
			attribute = attribute[4:]
			recursive = True
		
		if attribute in ["shapes", "rects", "circles", "ellipses", "lines",
						 "polylines", "polygons", "paths", "groups"]:
			elements = []
			if attribute in ["shapes", "rects"]:
				elements += self.get_children("rect",
							self.__dict__["container_map"]["rect"], recursive)
			if attribute in ["shapes", "circles"]:
				elements += self.get_children("circle",
							self.__dict__["container_map"]["circle"], recursive)
			if attribute in ["shapes", "ellipses"]:
				elements += self.get_children("ellipse",
							self.__dict__["container_map"]["ellipse"], recursive)
			if attribute in ["shapes", "lines"]:
				elements += self.get_children("line",
							self.__dict__["container_map"]["line"], recursive)
			if attribute in ["shapes", "polylines"]:
				elements += self.get_children("polyline",
							self.__dict__["container_map"]["polyline"], recursive)
			if attribute in ["shapes", "polygons"]:
				elements += self.get_children("polygon",
							self.__dict__["container_map"]["polygon"], recursive)
			if attribute in ["shapes", "paths"]:
				elements += self.get_children("path",
							self.__dict__["container_map"]["path"], recursive)
			if attribute in ["shapes", "group"]:
				elements += self.get_children("g",
							self.__dict__["container_map"]["group"], recursive)
			return elements
		else:
			return None
	
	def __setattr__(self, attribute, value):
		"""
		Set the value of an attribute. Note that this function only handles special
		attributes that pertain to this container.
		
		@type attribute: string
		@param attribute: The name of the attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		@rtype: boolean
		@return: True on attribute set, False if this function doesn't handle
				 this attribute, which can be used to send it along to an
				 L{XMLElement<svg.svgelement.XMLElement>}-based class.
		"""
		if attribute[:4] == "all_":
			attribute = attribute[4:]
		
		if attribute in ["shapes", "rects", "circles", "ellipses", "lines",
						 "polylines", "polygons", "paths", "groups"]:
			log.error(attribute + " is read-only!")
			raise SVGReadOnlyError, attribute
		else:
			return False
	
	def create_shape(self, tag = None, shape_id = None, attributes = {},
							fill = None, stroke = None, stroke_width = None,
							shape_type = None):
		"""
		Add a new shape to this container. Provides common functionality for all
		shapes that can be added.
		
		@type tag: string
		@param tag: The name of the shape's XML tag
		@type shape_id: string
		@param shape_id: The unique identifier of the shape
		@type attributes: dict
		@param attributes: A dictionary of attribute:value pairs for attributes
						to be set in the new shape.
		@type fill: string
		@param fill: The fill value of this shape
		@type stroke: string
		@param stroke: The stroke value of this shape
		@type stroke_width: string
		@param stroke_width: The width of the stroke value
		@type shape_type: L{XMLElement<svg.svgelement.XMLElement>}-based class
		@param shape_type: The class type of the shape to be created
		@rtype: shape_type
		@return: The newly added shape.
		"""
		# if no shape id is specified get a numerical one
		if shape_id == None:
			shape_id = get_new_id(tag)
		attributes["id"] = str(shape_id)
		if stroke_width != None:
			attributes["stroke-width"] = stroke_width
		shape = self.create_child(tag, shape_type, attributes)
		if fill:
			shape.fill = fill
		if stroke:
			shape.stroke = stroke
		return shape
	
	def create_rect(self, id = None, start = None, dimensions = None,
					fill = None, stroke = None, stroke_width = None,
					rounded = None):
		"""
		Add a new L{Rect<svg.elements.Rect>} to this container
		
		@type id: string
		@param id: The unique identifier of the new rect
		@type start: list
		@param start: The [x, y] coordinate of the top left of the rectangle
		@type dimensions: list
		@param dimensions: The [width, height] of the rectangle
		@type fill: string
		@param fill: The fill value of the rectangle
		@type stroke: string
		@param stroke: The stroke value of the rectangle
		@type stroke_width: string
		@param stroke_width: The width of the stroke of the rectangle
		@type rounded: list
		@param rounded: The [x, y] amount of rounding done to the edges of the
						rectangle
		@rtype: L{Rect<svg.elements.Rect>}
		@return: The newly created rect
		"""
		attributes = {}
		if start:
			attributes["x"] = start[0]
			attributes["y"] = start[1]
		if dimensions:
			attributes["width"] = dimensions[0]
			attributes["height"] = dimensions[1]
		if rounded:
			attributes["rx"] = rounded[0]
			attributes["ry"] = rounded[1]
		return self.create_shape("rect", id, attributes, fill, stroke,
								stroke_width,
								self.__dict__["container_map"]["rect"])
	
	def create_circle(self, id = None, center = None, radius = None,
					  fill = None, stroke = None, stroke_width = None):
		"""
		Add a new L{Circle<svg.elements.Circle>} to this container
		
		@type id: string
		@param id: The unique identifier of the new circle
		@type center: list
		@param center: The [x, y] coordinates of the center of the circle
		@type radius: number
		@param radius: The radius of the circle
		@type fill: string
		@param fill: The fill value of the circle
		@type stroke: The stroke value of the rectangle
		@type stroke_width: string
		@param stroke_width: The width of the stroke of the circle
		@rtype: L{Circle<svg.elements.Circle>}
		@return: The newly created circle.
		"""
		attributes = {}
		if center:
			attributes["cx"] = center[0]
			attributes["cy"] = center[1]
		if radius != None:
			attributes["r"] = radius
		return self.create_shape("circle", id, attributes, fill, stroke,
								stroke_width,
								self.__dict__["container_map"]["circle"])

	def create_ellipse(self, id = None, center = None, radius = None,
					  fill = None, stroke = None, stroke_width = None):
		"""
		Add a new L{Circle<svg.elements.Circle>} to this container
		
		@type id: string
		@param id: The unique identifier of the new circle
		@type center: list
		@param center: The [x, y] coordinates of the center of the ellipse
		@type radius: list
		@param radius: The [x, y] coordinates of the radius of the ellipse
		@type fill: string
		@param fill: The fill value of the circle
		@type stroke: The stroke value of the rectangle
		@type stroke_width: string
		@param stroke_width: The width of the stroke of the ellipse
		@rtype: L{Ellipse<svg.elements.Ellipse>}
		@return: The newly created ellipse.
		"""
		attributes = {}
		if center:
			attributes["cx"] = center[0]
			attributes["cy"] = center[1]
		if radius:
			attributes["rx"] = radius[0]
			attributes["ry"] = radius[1]
		return self.create_shape("ellipse", id, attributes, fill, stroke,
								stroke_width,
								self.__dict__["container_map"]["ellipse"])
	
	def create_line(self, id = None, start = None, stop = None, stroke = None,
					stroke_width = None):
		"""
		Add a new L{Line<svg.elements.Line>} to this container.
		
		@type id: string
		@param id: The unique identifier of the new line
		@type start: list
		@param start: The [x, y] coordinates of the start of the line.
		@type stop: list
		@param stop: The [x, y] coordinates of the stop of the line.
		@type stroke: string
		@param stroke: The stroke value of the rectangle
		@type stroke_width: string
		@param stroke_width: The width of the stroke of the line
		@rtype: L{Line<svg.elements.Line>}
		@return: The newly created line.
		"""
		attributes = {}
		if start:
			attributes["x1"] = start[0]
			attributes["y1"] = start[1]
		if stop:
			attributes["x2"] = start[0]
			attributes["y2"] = start[1]
		return self.create_shape("line", id, attributes, None, stroke,
								stroke_width,
								self.__dict__["container_map"]["line"])
