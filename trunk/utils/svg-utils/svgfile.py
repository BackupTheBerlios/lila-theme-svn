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
import svgutils
from xml.dom.minidom import parse, Element
from xml.dom.ext import PrettyPrint

class SVGCommon:
	"""SVG XML object common functions"""
	def __init__(self, element = None):
		"""Initialize the class"""
		if element:
			self.set_element(element)
		else:
			self._element = None

	def set_element(self, element):
		"""set our class to a specific stop XML object"""
		self._element = element

	def get_name(self):
		"""Returns the element's name"""
		if self._element:
			return self._element.getAttribute("id")
		return None

	def get_tag(self):
		"""Returns the element's tag"""
		if self._element:
			return self._element.tagName
		return None

	def set_name(self, name):
		"""Set the element's name"""
		if self._element:
			self._element.setAttribute("id", name)

class Stop(SVGCommon):
	"""Class to hold gradient stop data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGCommon.__init__(self, element)

	def get_offset(self):
		"""Returns the stop's offset value"""
		if self._element:
			return self._element.getAttribute("offset")
		return None

	def get_color(self):
		"""Returns the stop's color"""
		if self._element:
			color = svgutils.get_color(self._element, "stop-color:", "stop-opacity:")
			if color != -1:
				return color
		return None

	def set_offset(self, offset):
		"""Set the stop's offset"""
		if self._element:
			self._element.setAttribute("offset", offset)

	def set_color(self, color):
		"""Set the stop's color"""
		if self._element:
			svgutils.set_color(self._element, "stop-color:", "stop-opacity:", color)

class Gradient(SVGCommon):
	"""Class to hold gradient data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGCommon.__init__(self, element)

	def get_stops(self):
		"""Return a list of Stop objects in this gradient"""
		if self._element:
			stops = []
			for stop in self._element.getElementsByTagName("stop"):
				stops.append(Stop(stop))
			return stops
		return None

	def get_xlink(self):
		"""
		Returns the gradient's xlink if it is present
		The xlink is used to link to another gradient's colors
		"""
		if self._element:
			return self._element.getAttribute("xlink:href")

#	def set_stops(self, stops):
#		"""
#		Set the gradient's stops
#		stops must be a list of Stop objects
#		"""
#		# how oh how will this work?

	def set_xlink(self, xlink):
		"""
		Set the gradient's xlink value
		The xlink is used to link to another gradient's colors
		"""
		if self._element:
			self._element.setAttribute("xlink:href", xlink)

class LinearGradient(Gradient):
	"""Class to hold linear gradient data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		Gradient.__init__(self, element)

	def get_position(self):
		"""
		Return's the position of the gradient
		A tuple is returned (x1, y1, x2, y2)
		"""
		if self._element:
			pos = self._element.getAttribute("x1"),   \
					self._element.getAttribute("y1"), \
					self._element.getAttribute("x2"), \
					self._element.getAttribute("y2")
			return pos

	def set_position(self, position):
		"""
		Set the position of the gradient
		position must be a tuple (x1, y1, x2, y2)
		"""
		assert len(position) == 4
		if self._element:
			self._element.setAttribute("x1", position[0])
			self._element.setAttribute("y1", position[1])
			self._element.setAttribute("x2", position[2])
			self._element.setAttribute("y2", position[3])

class RadialGradient(Gradient):
	"""Class to hold radial gradient data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		Gradient.__init__(self, element)

	def get_position(self):
		"""
		Return's the position of the gradient
		A tuple is returned (cx, cy, r, fx, fy)
		"""
		if self._element:
			pos = self._element.getAttribute("cx"),   \
					self._element.getAttribute("cy"), \
					self._element.getAttribute("r"), \
					self._element.getAttribute("fx"), \
					self._element.getAttribute("fy")
			return pos

	def set_position(self, position):
		"""
		Set the position of the gradient
		position must be a tuple (cx, cy, r, fx, fy)
		"""
		assert len(position) == 5
		if self._element:
			self._element.setAttribute("cx", position[0])
			self._element.setAttribute("cy", position[1])
			self._element.setAttribute("r", position[2])
			self._element.setAttribute("fx", position[3])
			self._element.setAttribute("fy", position[4])

class SVGObjectCommon(SVGCommon):
	"""SVG XML drawn object common functions"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGCommon.__init__(self, element)

	def get_fill_color(self):
		"""Returns the object's fill color"""
		if self._element:
			color = svgutils.get_color(self._element, "fill:", "fill-opacity:")
			if color != -1:
				return color
		return None

	def get_stroke_color(self):
		"""Returns the object's stroke color"""
		if self._element:
			color = svgutils.get_color(self._element, "stroke:", "stroke-opacity:")
			if color != -1:
				return color
		return None

	def get_stroke_width(self):
		"""Returns the object's stroke width"""
		if self._element:
			style = self._element.getAttribute("style")
			width = svgutils.get_style_element(style, "stroke-width:", "0")
			return width
		return None

	def set_fill_color(self, color):
		"""Set the object's fill color"""
		if self._element:
			svgutils.set_color(self._element, "fill:", "fill-opacity:", color)

	def set_stroke_color(self, color):
		"""Set the object's stroke color"""
		if self._element:
			svgutils.set_color(self._element, "stroke:", "stroke-opacity:", color)

	def set_stroke_width(self, width):
		"""Set the object's stroke width"""
		if self._element:
			style = self._element.getAttribute("style")
			svgutils.replace_style_element(style, "stroke-width:", width)

class Rect(SVGObjectCommon):
	"""Class to hold rectangle data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

	def get_position(self):
		"""
		Returns the position of the rect
		A tuple is returned (x, y, width, height)
		"""
		if self._element:
			pos = self._element.getAttribute("x"),   \
				self._element.getAttribute("y"),     \
				self._element.getAttribute("width"), \
				self._element.getAttribute("height")
			return pos

	def set_position(self, position):
		"""
		Sets the position of the rect
		position must be a tuple (x, y, width, height)
		"""
		assert len(position) == 4
		if self._element:
			self._element.setAttribute("x", position[0])
			self._element.setAttribute("y", position[1])
			self._element.setAttribute("width", position[2])
			self._element.setAttribute("height", position[3])

class Circle(SVGObjectCommon):
	"""Class to hold circle data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

class Ellipse(SVGObjectCommon):
	"""Class to hold elipse data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

class Line(SVGObjectCommon):
	"""Class to hold line data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

class Polyline(SVGObjectCommon):
	"""Class to hold polyline data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

class Polygon(SVGObjectCommon):
	"""Class to hold polygon data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

class Path(SVGObjectCommon):
	"""Class to hold path data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

class Text(SVGObjectCommon):
	"""Class to hold text data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

	def get_tspans(self):
		"""Returns a list of TSpan objects"""
		if self._element:
			tspans = []
			for tspan in self._element.getElementsByTagName("tspan"):
				tspans.append(TSpan(tspan))
			return tspans
		return None

class TSpan(SVGObjectCommon):
	"""Class to hold tspan data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

	def get_text(self):
		"""Returns the text held in this tspan"""
		if self._element:
			return self._element.nodeValue
		return None

class TRef(SVGObjectCommon):
	"""Class to hold tref data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

class TextPath(SVGObjectCommon):
	"""Class to hold textpath data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGObjectCommon.__init__(self, element)

class Container(SVGCommon):
	"""Class for container objects"""
	def __init__(self, element = None):
		"""Initialize the class"""
		SVGCommon.__init__(self, element)

	def _get_element_list(self, element_tag, type_class):
		"""Returns a list of objects"""
		if self._element:
			objs = []
			for obj in self._element.getElementsByTagName(element_tag):
				objs.append(type_class(obj))
			return objs
		return None

	def get_groups(self):
		"""Return a list of Group objects"""
		return self._get_element_list("g", Group)

	def get_linear_gradients(self):
		"""Return a list of LinearGradient objects"""
		return self._get_element_list("linearGradient", LinearGradient)

	def get_radial_gradients(self):
		"""Return a list of RadialGradient objects"""
		return self._get_element_list("radialGradient", RadialGradient)

	def get_rects(self):
		"""Returns a list of Rect objects"""
		return self._get_element_list("rect", Rect)

	def get_circles(self):
		"""Returns a list of Circle objects"""
		return self._get_element_list("circle", Circle)

	def get_ellipses(self):
		"""Returns a list of Elipse objects"""
		return self._get_element_list("ellipse", Ellipse)

	def get_lines(self):
		"""Returns a list of Line objects"""
		return self._get_element_list("line", Line)

	def get_polylines(self):
		"""Returns a list of Polyline objects"""
		return self._get_element_list("polyline", Polyline)

	def get_polygons(self):
		"""Returns a list of Polygon objects"""
		return self._get_element_list("polygon", Polygon)

	def get_paths(self):
		"""Returns a list of Path objects"""
		return self._get_element_list("path", Path)

	def get_texts(self):
		"""Returns a list of Text objects"""
		return self._get_element_list("text", Text)

	def get_tspans(self):
		"""Returns a list of TSpan objects"""
		return self._get_element_list("tspan", TSpan)

	def get_trefs(self):
		"""Returns a list of TRef objects"""
		return self._get_element_list("tref", TSpan)

	def get_text_paths(self):
		"""Returns a list of TextPath objects"""
		return self._get_element_list("textPath", TSpan)

class Group(Container, SVGObjectCommon):
	"""Class to hold group data"""
	def __init__(self, element = None):
		"""Initialize the class"""
		Container.__init__(self, element)
		SVGObjectCommon.__init__(self, element)

class SVGFile(Container):
	"""Class to hold an SVG file and access its information"""
	def __init__(self, filename):
		"""Initialize the class"""
		Container.__init__(self, None)
		self.load(filename)

	def load(self, filename):
		"""
		Load an SVG file into this class
		"""
		# load the document
		self._dom = parse(filename)
		self._filename = filename
		self.set_element(self._dom.documentElement)

	def save(self, filename = None):
		"""
		Save an SVG file from this class
		If no filename is specified it will save to the same
		file that was sent on class init or by calling the
		load() function.
		This will OVERWRITE the file if it already exists!
		"""
		# save the document tree
		if filename:
			file = open(filename,"w")
		else:
			file = open(self._filename, "w")
		PrettyPrint(self._dom, file)
		file.close()

	def get_width(self):
		"""Return the document's width"""
		return self._element.getAttribute("width")

	def get_height(self):
		"""Return the document's height"""
		return self._element.getAttribute("height")

	def get_inkscape_version(self):
		"""Return the document's Inkscape version string"""
		return self._element.getAttribute("inkscape:version")

	def get_sodipodi_version(self):
		"""Return the document's Sodipodi version string"""
		return self._element.getAttribute("sodipodi:version")

	def get_xmlns(self):
		"""Return the document's XML Namespace"""
		return self._element.getAttribute("xmlns")

	def get_xmlns_inkscape(self):
		"""Return the document's Inkscape XML Namespace"""
		return self._element.getAttribute("xmlns:inkscape")

	def get_xmlns_sodipodi(self):
		"""Return the document's Sodipodi XML Namespace"""
		return self._element.getAttribute("xmlns:sodipodi")

	def get_xmlns_xlink(self):
		"""Return the document's XLink XML Namespace"""
		return self._element.getAttribute("xmlns:xlink")

	def set_width(self, width):
		"""Set the document's width"""
		self._element.setAttribute("width", width)

	def set_height(self, height):
		"""Set the document's height"""
		self._element.setAttribute("height", height)

	def set_inkscape_version(self, version):
		"""Set the document's Inkscape version string"""
		self._element.setAttribute("inkscape:version", version)

	def set_sodipodi_version(self, version):
		"""Set the document's Sodipodi version string"""
		self._element.setAttribute("sodipodi:version", version)

	def set_xmlns(self, xmlns):
		"""Set the document's XML Namespace"""
		self._element.setAttribute("xmlns", xmlns)

	def set_xmlns_inkscape(self, xmlns):
		"""Set the document's Inkscape XML Namespace"""
		self._element.setAttribute("xmlns:inkscape", xmlns)

	def set_xmlns_sodipodi(self, xmlns):
		"""Set the document's Sodipodi XML Namespace"""
		self._element.setAttribute("xmlns:sodipodi", xmlns)

	def set_xmlns_xlink(self, xmlns):
		"""Set the document's XLink XML Namespace"""
		self._element.getAttribute("xmlns:xlink", xmlns)
