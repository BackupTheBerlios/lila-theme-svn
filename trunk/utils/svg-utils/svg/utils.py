#!/usr/bin/env python

"""
	Utilities
	Easy access to XML files, specifically SVG

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
from xml.dom.minidom import Document
from sys import exit

def get_style_element(style, element, default = None):
	"""
	Return the value of an element within a CSS type style string
	style can be any style string, like "stop-color: #000; stop-opacity: 1.0;"
	element can be any element within it, like "stop-color"
	In the example above, "#000" would be returned
	"""
	# find the element
	start = style.find(element + ":")
	if start == -1:
		if Default:
			return Default
		else:
			raise AttributeError, element
	else:
		# get and return the element's value
		start += len(element) + 1
		end = style.find(";", start)
		return style[start : end]

def set_style_element(style, element, value):
	"""
	Return an updated style string with element set to value
	"""
	# find the element
	start = style.find(element + ":")
	if start == -1:
		# if it's not there let's append it!
		style_string = style + ' ' + element + ": " + value + ';'
	else:
		# replace the old value and return the string
		start += len(element) + 1
		end = style.find(';', start)
		style_string = style[:start] + ' ' + value + style[end:]
	return style_string

def alpha_to_hex(alpha):
	"""
	Returns the hex version of the alpha value
	For example, an alpha of 1.0 will return ff,
	while an alpha of 0.4 will return 66
	Note: alpha MUST be 0.0 - 1.0!
	"""
	temp_hex = hex(int(float(alpha) * 255));
	if len(temp_hex) > 3:
		return temp_hex[-2:]
	else:
		return "0" + temp_hex[-1:]

def hex_to_alpha(hex_value):
	"""
	Returns the string alpha value of the hex number passed
	hex_value must be between 00 and ff for this to return
	a valid opacity setting
	"""
	temp_alpha = str(round(int(hex_value, 16) / 255.0, 2))
	return temp_alpha

def color_name_to_hex(color):
	"""
	Returns the hex value of a named color
	Will return #000000 when passed black, for example
	"""
	# the default will be the color we are passed
	hexval = color
	color = color.lower()
	if color == "black":
		hexval = "#000000"
	elif color == "red":
		hexval = "#ff0000"
	elif color == "green":
		hexval == "#00ff00"
	elif color == "blue":
		hexval == "#0000ff"
	elif color == "yellow":
		hexval == "#ffff00"
	elif color == "cyan":
		hexval == "#00ffff"
	elif color == "magenta":
		hexval == "#ff00ff"
	elif color == "gray":
		hexval == "#c0c0c0"
	elif color == "white":
		hexval = "#ffffff"
	elif color == "none":
		hexval = None
	# return the new color (or default if it hasn't changed)
	return hexval

def get_color(element, color_string, opacity_string):
	"""
	Return the hex value of the color and opacity of an element
	#RRGGBBAA is returned
	"""
	color = None
	opacity = "1"
	if element.has_attribute(color_string, False):
		# use the get_attribute method to be safe!
		color = element.__getattr__(color_string, False)
		# translate the color to hex
		color = color_name_to_hex(color)
	if element.has_attribute(opacity_string, False):
		opacity = element.__getattr__(opacity_string, False)
	if color and opacity:
		if color[:3] != "url":
			# expand a shorthand notation
			if len(color) < 7:
				color = color[:2] + color[1] + color[2] + color[2] + color[3] + color[3]
			# convert opacity to hex
			opacity = alpha_to_hex(opacity)
			return color + opacity
		else:
			return color
	else:
		raise AttributeError, (color and "Opacity " or "Color ") + "not set! (" + (color and opacit_string or color_string) + ")"

def set_color(element, color_string, opacity_string, hex_color):
	"""
	Set the color of element using a #RRGGBBAA style color
	"""
	if hex_color[0] == "#":
		color = hex_color[:-2]
		alpha = hex_color[-2:]
		alpha = hex_to_alpha(alpha)
		element.__setattr__(color_string, color, False)
		element.__setattr__(opacity_string, alpha, False)
	else:
		element.__setattr__(color_string, hex_color, False)

class ReadOnlyError(Exception):
	def __init__(self, value = ''):
		self.value = value

	def __str__(self):
		return repr(self.value)

class XMLElement:
	"""
	Holds an XML element and provides easy access
	"""
	def __init__(self, element):
		"""
		Initialize
		"""
		self.__dict__["element"] = element
		if not self.__dict__.has_key("attribute_aliases"):
			self.__dict__["attribute_aliases"] = {}

	def register_attribute_alias(self, alias, attribute):
		"""
		Register an alias for the given attribute
		"""
		self.__dict__["attribute_aliases"][alias] = attribute

	def unregister_attribute_alias(self, alias):
		"""
		Remove an attribute alias
		"""
		del self.__dict__["attribute_aliases"][alias]

	def __getattr__(self, attribute, custom = True):
		"""
		Allow direct read access to xml element attributes
		Example: XMLElement.id, XMLElement.xmlns, etc...
		If the attribute doesn't exist, an exception is raised
		"""
		# first line keeps us from getting infinite recursion
		if attribute == "_get_attribute": return
		elif attribute == "_set_attribute": return lambda a,b: False
		#l = len(attribute)
		#if l > 10: l = 10
		#print "__GETATTR__", attribute[:l], self.__dict__["element"].getAttribute("id")
		if attribute in self.__dict__["attribute_aliases"].keys():
			return self.__getattr__(self.__dict__["attribute_aliases"][attribute], False)
		if custom:
			try:
				# see if a subclass added the _get_attribute function
				value, cont = self._get_attribute(attribute)
				# cont is passed when the result is Null but we should
				# still continue
				if not cont: return value
			except: pass
		# check for the attribute and return it
		if self.__dict__.has_key("element"):
			if attribute == "element":
				return self.__dict__["element"]
			elif attribute == "tag":
				return self.__dict__["element"].nodeName
			elif self.__dict__["element"].hasAttribute(attribute):
				return self.__dict__["element"].getAttribute(attribute)
			else:
				if attribute != "style":
					try:
						style = self.__dict__["element"].getAttribute("style")
						if str(attribute) + ':' in style:
							return get_style_element(style, attribute)
						else:
							raise AttributeError, attribute
					except:
						raise AttributeError, attribute
				else:
					raise AttributeError, attribute
		else:
			raise AttributeError, "Element not set!"

	def __setattr__(self, attribute, value, custom = True):
		"""
		Allow direct write access to xml element attributes
		Example: XMLElement.id = "my_file"
		"""
		#l = len(attribute)
		#if l > 10: l = 10
		#print "__SETATTR__", attribute[:l]
		if attribute in self.__dict__["attribute_aliases"].keys():
			return self.__setattr__(self.__dict__["attribute_aliases"][attribute], value, False)
		if custom:
			try:
				if self._set_attribute(attribute, value):
					return True
			except ReadOnlyError, msg:
				raise ReadOnlyError, msg
			else:
				pass
		if attribute == "element":
			self.__dict__["element"] = value
		elif attribute == "tag":
			self.__dict__["element"].nodeName = value
		elif self.__dict__.has_key("element"):
			if attribute != "style":
				try:
					style = self.__dict__["element"].getAttribute("style")
					if attribute + ':' in style:
						self.style = set_style_element(style, attribute, value)
						return
				except: pass
			self.__dict__["element"].setAttribute(attribute, str(value))
		else:
				raise AttributeError, "Element not set!"

	def has_attribute(self, attribute, custom = True):
		"""
		This method lets you know if an attribute exists
		"""
		#l = len(attribute)
		#if l > 10: l = 10
		#print "HAS_ATTRIBUTE", attribute[:l]
		if self.__dict__.has_key("element"):
			try:
				tmp = self.__getattr__(attribute, custom)
				if tmp:
					return True
				else:
					return False
			except:
				return False
			#if self.__dict__["element"].hasAttribute(attribute) or \
			#	(self.__dict__["element"].hasAttribute("style") and attribute + ':' in self.style) or \
			#	(attribute == "tag"):
			#	return True
		return False

	def get_attribute(self, attribute, custom = True):
		"""
		Backup for items that can't be used with __getattr__
		xmlns:inkscape is a good example!
		"""
		#l = len(attribute)
		#if l > 10: l = 10
		#print "GET_ATTRIBUTE", attribute[:l]
		return self.__getattr__(attribute, custom)

	def set_attribute(self, attribute, value, custom = True):
		"""
		Backup for items that can't be used with __setattr__
		xmlns:inkscape is a good example!
		"""
		#l = len(attribute)
		#if l > 10: l = 10
		#print "SET_ATTRIBUTE", attribute[:l]
		self.__setattr__(attribute, value, custom)

	def get_children(self, tag_name = '', class_type = None, recursive = False):
		"""
		Return a list of child elements
		If tag_name is specified, only those elements with that name
		will be included in the list
		class_type is the class to which the actual XML element is passed
		recursive will search children's children, etc...
		"""
		if self.__dict__.has_key("element"):
			elements = []
			if tag_name:
				if recursive:
					for element in self.__dict__["element"].getElementsByTagName(tag_name):
						if class_type:
							elements.append(class_type(element))
						else:
							elements.append(XMLElement(element))
				else:
					for element in self.__dict__["element"].childNodes:
						if element.nodeName == tag_name:
							if class_type:
								elements.append(class_type(element))
							else:
								elements.append(XMLElement(element))
			else:
				for element in self.__dict__["element"].childNodes:
					if class_type:
						elements.append(class_type(element))
					else:
						elements.append(XMLElement(element))
		else:
			raise AttributeError, "Element not set!"
		return elements

	def add_child_tag(self, tag, tag_type = None, attributes = {}):
		"""
		Add an element with tag as a child
		tag_type will be XMLElement if it is None
		attributes should be a dict of { "attribute" : "value }
		"""
		if self.__dict__.has_key("element"):
			tmp = Document().createElement(tag)
			element = self.__dict__["element"].appendChild(tmp)
			if tag_type:
				xmlelement = tag_type(element)
			else:
				xmlelement = XMLElement(element)
			for attribute in attributes:
				xmlelement.set_attribute(attribute, attributes[attribute])
			return xmlelement
		else:
			raise AttributeError, "Element not set!"

	def unlink(self):
		"""
		Destroy this element
		"""
		if self.__dict__.has_key("element"):
			if self.__dict__["element"].parentNode:
				self.__dict__["element"].parentNode.removeChild(self.__dict__["element"])

def red(text):
	"""
	Return given text in red (using bash colors)
	"""
	return '\x1b[31;01m' + text + '\x1b[0m'

def green(text):
	"""
	Return given text in green (using bash colors)
	"""
	return '\x1b[32;01m' + text + '\x1b[0m'

def blue(text):
	"""
	Return given text in blue (using bash colors)
	"""
	return '\x1b[34;01m' + text + '\x1b[0m'
