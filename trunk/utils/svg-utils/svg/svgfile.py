#!/usr/bin/env python

"""
	SVGFile class
	Class to hold an SVG file and retrieve/set its data

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

# Imports
from elements import Group, Defs
from utils import print_svg, get_color, set_color
from xml.dom.minidom import parse, getDOMImplementation, Document
from sys import exit

id_counter = 0

def get_special_attribute(element, attribute, recursive = False):
	"""
	Try to get a special attribute from an element
	"""
	if attribute == "text":
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
	if attribute == "text":
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

class SVGFile(Group, Defs):
	def __init__(self, filename = None):
		if filename:
			dom = parse(filename)
			Group.__init__(self, dom.documentElement)
			self.__filename = filename
			try:
				self.__dict__["defs"] = self.get_children("defs", Defs)[0]
			except:
				self.__dict__["defs"] = self.create_child("defs", Defs, { "id" : "defs" })
		else:
			# create a default SVG document
			Group.__init__(self, getDOMImplementation().createDocument(None, "svg", None).documentElement)
			self.id = "New Document"
			self.width = "48pt"
			self.height = "48pt"
			self.xmlns = "http://www.w3.org/2000/svg"
			self.set_attribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
			self.__dict__["defs"] = self.create_child("defs", Defs, { "id" : "defs" })
		#Defs.__init__(self, self.element)

	def save(self, filename = None):
		"""
		Save the SVG
		If no filename is given the same file that was loaded is used
		"""
		if filename:
			outfile = file(filename, "w")
		else:
			outfile = file(self.__filename, "w")
		print_svg(self, outfile)

	def __str__(self):
		"""
		Return the SVG's XML in a string
		"""
		class SVGString:
			def __init__(self):
				self.string = ''

			def write(self, data):
				self.string += str(data)

		svg = SVGString()

		print_svg(self, svg)

		return svg.string
