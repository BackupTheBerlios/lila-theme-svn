#!/usr/bin/env python

"""
	SVGElement
	==========
		Easy access to SVG and XML elements
		
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

# Imports
from xml.dom.minidom import Document

from utils import get_style_element, set_style_element, print_xml

import log

class DummyDOMElement:
	"""
	A dummy element used for testing purposes.
	"""
	def __init__(self, name):
		self.nodeName = name
	
	def hasAttribute(self, attribute):
		return self.__dict__.has_key(attribute) and True or False
	
	def getAttribute(self, attribute):
		exec("return self." + attribute)
	
	def setAttribute(self, attribute, value):
		exec("self." + attribute + " = " + str(value))

class XMLElement:
	"""
	XML Element
	===========
		This class holds an XML element and provides easy access.
		
		Attributes
		----------
		Attributes of the element can be accessed as if they were variables
		within the class:
			- C{element.name}
			- C{element.width}
			- C{element.style}
		
		Attribute Aliases
		-----------------
		Attribute aliases can be used to provide intuitive access to attributes
		with strange names. Notice that the attribute and the alias will point
		to the same internal structure. As an example,
		
		>>> element = XMLElement()
		>>> element.w = 10
		>>> element.register_attribute_alias("width", "w")
		>>> element.width
		10
		>>> element.width = 15
		>>> element.width
		15
		>>> element.w
		15
	"""
	def __init__(self, element = None):
		"""
		Initialize
		
		@type element: xml.dom.Element
		@param element: An XML DOM element.
		"""
		if element:
			self.__dict__["element"] = element
		else:
			self.__dict__["element"] = Document().createElement("undefined")
			log.info("New element created")
		if not self.__dict__.has_key("attribute_aliases"):
			self.__dict__["attribute_aliases"] = {}

	def register_attribute_alias(self, alias, attribute):
		"""
		Register an alias for the given attribute
		
		@type alias: string
		@param alias: The new name to access attribute from.
		@type attribute: string
		@param attribute: The actual attribute that will be accessed.
		"""
		self.__dict__["attribute_aliases"][alias] = attribute
		log.debug("Alias registered: " + alias + " -> " + attribute + ".")

	def unregister_attribute_alias(self, alias):
		"""
		Remove an attribute alias
		
		@type alias: string
		@param alias: The alias to be removed
		"""
		del self.__dict__["attribute_aliases"][alias]
		log.debug("Alias unregistered: " + alias + ".")

	def flush_attribute_aliases(self):
		"""
		Flush all attribute aliases. After this function is called the attribute alias
		dict will be empty.
		"""
		self.__dict__["attribute_aliases"] = {}
		log.debug("Aliases flushed.")

	def __getattr__(self, attribute):
		"""
		Allow direct read access to xml element attributes. This is basically a pass-
		through to the xml element:
		
		XMLElement -> __getattr__ -> element.getAttribute
		
		Example: C{XMLElement.id}, C{XMLElement.xmlns}, etc...
		
		Aliases are resolved to their actual attributes.
		If the attribute doesn't exist, an exception is raised.
		
		@type attribute: string
		@param attribute: The attribute being requested.
		@rtype: string
		@return: The requested attribute.
		"""
		#print "__GETATTR__", attribute[:l], self.__dict__["element"].getAttribute("id")
		if attribute in self.__dict__["attribute_aliases"].keys():
			return self.__getattr__(self.__dict__["attribute_aliases"][attribute])
		# check for the attribute and return it
		if self.__dict__.has_key("element"):
			# check for some hard coded attributes
			if attribute == "element":	# the XML element object
				return self.__dict__["element"]
			elif attribute == "tag":	# the XML tag name of the element
				return self.__dict__["element"].nodeName
			# The line below checks the actual XML element for the given attribute
			# and then returns it if found
			elif self.__dict__["element"].hasAttribute(attribute):
				return self.__dict__["element"].getAttribute(attribute)
			else:	# not found... raise an exception!
				raise AttributeError, attribute
		else:
			raise AttributeError, "Element not set!"

	def __setattr__(self, attribute, value):
		"""
		Allow direct write access to xml element attributes. This is basically a pass-
		through to the xml element:
		
		XMLElement -> __setattr__ -> element.setAttribute
		
		Example: C{XMLElement.id = "my_file"}
		
		Aliases are resolved to their actual attributes.
		If the attribute doesn't exist, an exception is raised.
		
		@type attribute: string
		@param attribute: The attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		"""
		#print "__SETATTR__", attribute
		if attribute in self.__dict__["attribute_aliases"].keys():
			# it's an alias, so map to the real name and save that!
			return self.__setattr__(self.__dict__["attribute_aliases"][attribute], value)
		if attribute == "element":
			# we are setting the actual XML element... be careful!
			if type(value) != "instance":
				# we weren't passed a class instance!
				raise TypeError, "Not a class instance!"
			self.__dict__["element"] = value
		elif attribute == "tag":
			# don't know if this could ever be useful on it's own...
			self.__dict__["element"].nodeName = value
		elif self.__dict__.has_key("element"):
			self.__dict__["element"].setAttribute(attribute, str(value))
		else:
				raise AttributeError, "Element not set!"

	def has_attribute(self, attribute):
		"""
		This method lets you know if an attribute exists.
		
		@type attribute: string
		@param attribute: The attribute being searched for.
		@rtype: boolean
		@return: True if the attribute is found, else False.
		"""
		#print "HAS_ATTRIBUTE", attribute[:l]
		if self.__dict__.has_key("element"):
			try:
				tmp = self.__getattr__(attribute)
				if tmp:
					return True
			except:
				return False
		return False
	
	def __str__(self):
		"""
		Return a string representation of this object.
		
		@rtype: string
		@return: The XML for this object and it's children
		"""
		# quick class to fake a stream object
		class tempstr:
			def __init__(self): self.str = ""
			def write(self, value): self.str += value
		tmp = tempstr()
		print_xml(self.element, tmp)
		# return the value of the temporary stream as a string
		return tmp.str

	def get_attribute(self, attribute):
		"""
		Get an attribute from the element.
		
		This function is meant for attributes like "xmlns:inkscape" that cannot
		be used directly with __getattr__.
		
		@type attribute: string
		@param attribute: The attribute being requested.
		@rtype: string
		@return: The requested attribute.
		"""
		#print "GET_ATTRIBUTE", attribute[:l]
		return self.__getattr__(attribute)

	def set_attribute(self, attribute, value):
		"""
		Set an attribute within the element.
		
		This functioni is meant for attributes like "xmlns:inkscape" that cannot
		be used directly with __setattr__.
		
		@type attribute: string
		@param attribute: The attribute being set.
		@type value: string
		@param value: The value of the attribute being set.
		"""
		#print "SET_ATTRIBUTE", attribute[:l]
		self.__setattr__(attribute, value)

	def get_children(self, tag_name = '', class_type = None, recursive = False):
		"""
		Get the children of this element.
		
		@type tag_name: string
		@param tag_name: The type of tags to return. Leave blank to return all tags.
		@type class_type: class object
		@param class_type: A class object that will be applied to the children. If
						   this is left blank, they will be returned as 
						   L{XMLElement}s
		@type recursive: boolean
		@param recursive: Whether or not to search the children's children, etc.
		@rtype: list
		@return: A list of child objects, or an emtpy list if none exist.
		"""
		if self.__dict__.has_key("element"):
			elements = []
			if tag_name:
				if recursive:
					for element in self.__dict__["element"].getElementsByTagName(tag_name):
						if class_type:
							elements.append(class_type(element = element))
						else:
							elements.append(XMLElement(element = element))
				else:
					for element in self.__dict__["element"].childNodes:
						if element.nodeName == tag_name:
							if class_type:
								elements.append(class_type(element = element))
							else:
								elements.append(XMLElement(element = element))
			else:
				for element in self.__dict__["element"].childNodes:
					if class_type:
						elements.append(class_type(element = element))
					else:
						elements.append(XMLElement(element = element))
		else:
			raise AttributeError, "Element not set!"
		return elements

	def create_child(self, tag, tag_type = None, attributes = {}):
		"""
		Create an element of type tag as a child.
		
		@type tag: string
		@param tag: The name of the tag of new child object.
		@type tag_type: class object
		@param tag_type: A class object to be returned containing the new child. If
						 no class is specified, L{XMLElement} will be used.
		@type attributes: dictionary
		@param attributes: A dictionary of { attribute : value } pairs containing the
						   attributes to be given to the new child.
		"""
		log.info("Creating child node: " + tag)
		if self.__dict__.has_key("element"):
			tmp = Document().createElement(tag)
			element = self.__dict__["element"].appendChild(tmp)
			if tag_type:
				xmlelement = tag_type(attributes, element, True)
			else:
				xmlelement = XMLElement(element)
				for attribute in attributes:
					xmlelement.set_attribute(attribute, attributes[attribute])
			return xmlelement
		else:
			raise AttributeError, "Element not set!"

	def unlink(self):
		"""
		Destroys this element. Call this to delete the actual XML element that this
		class is a shell to.
		
		Why a seperate function instead of using the C{__del__} deconstructor? While it
		seemed like a good idea to use C{__del__}, we run into the problem of elements
		being garbage collected, which is fine for encapsulation classes, but not
		fine for automatically removing the actual XML element from the document tree.
		"""
		if self.__dict__.has_key("element"):
			if self.__dict__["element"].parentNode:
				self.__dict__["element"].parentNode.removeChild(self.__dict__["element"])
		log.info("Element destroyed.")


class SVGElement(XMLElement):
	"""
	SVG Element
	===========
		A class to hold an SVG element and provide easy access. This class acts just 
		like the L{XMLElement} class, with these enhancements:
		
		Style Attributes
		----------------
		Style attributes are searched when looking for an attribute. If an attribute
		is found to be in the style attribute of the element, it will remain in the
		style attribute if set later.
		
		Adding Existing Elements
		------------------------
		Existing elements can be added using the C{add_child()} method. This is useful
		for reparenting elements.
	"""
	def __init__(self, element = None):
		"""
		Initialize
		
		@type element: xml.dom.Element
		@param element: An optional pre-existing element.
		"""
		XMLElement.__init__(self, element)
		self.__dict__["extra_check"] = []

	def __getattr__(self, attribute, extra = True):
		"""
		Get attributes. For more information, see L{XMLElement.__getattr__}.
		
		This also searches within SVG "style" attributes.
		
		@type attribute: string
		@param attribute: The attribute being requested.
		@rtype: string
		@return: The requested attribute
		"""
		if extra:
			for check in self.__dict__["extra_check"]:
				value = check.__getattr__(self, attribute)
				if value:
					return value
		if attribute != "style":
			if self.__dict__["element"].hasAttribute("style"):
				# get and check the style element
				style = XMLElement.__getattr__(self, "style")
				if attribute + ":" in style:
					return get_style_element(style, attribute)
		return XMLElement.__getattr__(self, attribute)

	def __setattr__(self, attribute, value, extra = True):
		"""
		Set attributes. For more information, see L{XMLElement.__setattr__}.
		
		This also searches within SVG "style" attributes.
		
		@type attribute: string
		@param attribute: The attribute being set.
		@type value: string or number
		@param value: The value of the attribute being set.
		"""
		attribute_set = False
		if extra:
			for check in self.__dict__["extra_check"]:
				attribute_set = check.__setattr__(self, attribute, value)
				if attribute_set: break
		if not attribute_set:
			if attribute != "style":
				try:
					# get and check the style element, if it exists
					style = XMLElement.__getattr__(self, "style")
					if attribute + ":" in style:
						self.style = set_style_element(style, attribute, value)
				except: pass
			XMLElement.__setattr__(self, attribute, value)

	def add_child(self, element):
		"""
		Adds an existing element as a child into this element.
		
		@type element: XMLElement
		@param element: An XMLElement-based class object to add as a child.
		"""
		self.__dict__["element"].appendChild(element.element)
		log.info("Child added.")
