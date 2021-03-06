#!/usr/bin/env python

"""
	Utilities
	SVG-Utils utility functions

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

import log

id_counter = 0

def get_new_id(name = ""):
	"""
	Get a new unique identifier string
	
	@type name: string
	@param name: An optional name to be prepended to the unique id number. This
				 lets you create identifiers like "Rect3" or "Stop87" and so on.
	@rtype: string
	@return: A new unique id
	"""
	global id_counter
	id_counter += 1
	log.debug("New identifier created: " + name + str(id_counter) + ".")
	return name + str(id_counter)

def handle_attributes(self, tag, attributes):
	"""
	Handle attributes passed to shape classes
	"""
	self.tag = tag
	if not attributes.has_key("id"):
		attributes["id"] = get_new_id(tag)
	for key in attributes.keys():
		self.__setattr__(key, attributes[key])

def get_style_element(style, element, default = None):
	"""
	Return the value of an element within a CSS type style string
	style can be any style string, like "stop-color: #000; stop-opacity: 1.0;"
	element can be any element within it, like "stop-color"
	In the example above, "#000" would be returned
	"""
	log.debug("Searching for " + element + " in " + style + ".")
	# find the element
	start = style.find(element + ":")
	if start == -1:
		if default:
			return default
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
	# This code is autogenerated from the SVG specification!
	svgcolors = { 
		"aliceblue"				: "#f0f8ff",
		"antiquewhite"			: "#faebd7",
		"aqua"					: "#00ffff",
		"aquamarine"			: "#7fffd4",
		"azure"					: "#f0ffff",
		"beige"					: "#f5f5dc",
		"bisque"				: "#ffe4c4",
		"black"					: "#000000",
		"blanchedalmond"		: "#ffebcd",
		"blue"					: "#0000ff",
		"blueviolet"			: "#8a2be2",
		"brown"					: "#a52a2a",
		"burlywood"				: "#deb887",
		"cadetblue"				: "#5f9ea0",
		"chartreuse"			: "#7fff00",
		"chocolate"				: "#d2691e",
		"coral"					: "#ff7f50",
		"cornflowerblue"		: "#6495ed",
		"cornsilk"				: "#fff8dc",
		"crimson"				: "#dc143c",
		"cyan"					: "#00ffff",
		"darkblue"				: "#00008b",
		"darkcyan"				: "#008b8b",
		"darkgoldenrod"			: "#b886bb",
		"darkgray"				: "#a9a9a9",
		"darkgreen"				: "#006400",
		"darkgrey"				: "#a9a9a9",
		"darkkhaki"				: "#bdb76b",
		"darkmagenta"			: "#8b008b",
		"darkolivegreen"		: "#556b2f",
		"darkorange"			: "#ff8c00",
		"darkorchid"			: "#9932cc",
		"darkred"				: "#8b0000",
		"darksalmon"			: "#e9967a",
		"darkseagreen"			: "#8fbc8f",
		"darkslateblue"			: "#483d8b",
		"darkslategray"			: "#2f4f4f",
		"darkslategrey"			: "#2f4f4f",
		"darkturquoise"			: "#00ced1",
		"darkviolet"			: "#9400d3",
		"deeppink"				: "#ff1493",
		"deepskyblue"			: "#00bfff",
		"dimgray"				: "#696969",
		"dimgrey"				: "#696969",
		"dodgerblue"			: "#1e90ff",
		"firebrick"				: "#b22222",
		"floralwhite"			: "#fffaf0",
		"forestgreen"			: "#228b22",
		"fuchsia"				: "#ff00ff",
		"gainsboro"				: "#dcdcdc",
		"ghostwhite"			: "#f8f8ff",
		"gold"					: "#ffd700",
		"goldenrod"				: "#daa520",
		"gray"					: "#808080",
		"green"					: "#008000",
		"greenyellow"			: "#adff2f",
		"grey"					: "#808080",
		"honeydew"				: "#f0fff0",
		"hotpink"				: "#ff69b4",
		"indianred"				: "#cd5c5c",
		"indigo"				: "#4b0082",
		"ivory"					: "#fffff0",
		"khaki"					: "#f0e68c",
		"lavender"				: "#e6e6fa",
		"lavenderblush"			: "#fff0f5",
		"lawngreen"				: "#7cfc00",
		"lemonchiffon"			: "#fffacd",
		"lightblue"				: "#add8e6",
		"lightcoral"			: "#f08080",
		"lightcyan"				: "#e0ffff",
		"lightgoldenrodyellow"	: "#fafad2",
		"lightgray"				: "#d3d3d3",
		"lightgreen"			: "#90ee90",
		"lightgrey"				: "#d3d3d3",
		"lightpink"				: "#ffb6c1",
		"lightsalmon"			: "#ffa07a",
		"lightseagreen"			: "#20b2aa",
		"lightskyblue"			: "#87cefa",
		"lightslategray"		: "#778899",
		"lightslategrey"		: "#778899",
		"lightsteelblue"		: "#b0c4de",
		"lightyellow"			: "#ffffe0",
		"lime"					: "#00ff00",
		"limegreen"				: "#32cd32",
		"linen"					: "#faf0e6",
		"magenta"				: "#ff00ff",
		"maroon"				: "#800000",
		"mediumaquamarine"		: "#66cdaa",
		"mediumblue"			: "#0000cd",
		"mediumorchid"			: "#ba55d3",
		"mediumpurple"			: "#9370db",
		"mediumseagreen"		: "#3cb371",
		"mediumslateblue"		: "#7b68ee",
		"mediumspringgreen"		: "#00fa9a",
		"mediumturquoise"		: "#48d1cc",
		"mediumvioletred"		: "#c71585",
		"midnightblue"			: "#191970",
		"mintcream"				: "#f5fffa",
		"mistyrose"				: "#ffe4e1",
		"moccasin"				: "#ffe4b5",
		"navajowhite"			: "#ffdead",
		"navy"					: "#000080",
		"oldlace"				: "#fdf5e6",
		"olive"					: "#808000",
		"olivedrab"				: "#6b8e23",
		"orange"				: "#ffa500",
		"orangered"				: "#ff4500",
		"orchid"				: "#da70d6",
		"palegoldenrod"			: "#eee8aa",
		"palegreen"				: "#98fb98",
		"paleturquoise"			: "#afeeee",
		"palevioletred"			: "#db7093",
		"papayawhip"			: "#ffefd5",
		"peachpuff"				: "#ffdab9",
		"peru"					: "#cd853f",
		"pink"					: "#ffc0cb",
		"plum"					: "#dda0dd",
		"powderblue"			: "#b0e0e6",
		"purple"				: "#800080",
		"red"					: "#ff0000",
		"rosybrown"				: "#bc8f8f",
		"royalblue"				: "#4169e1",
		"saddlebrown"			: "#8b4513",
		"salmon"				: "#fa8072",
		"sandybrown"			: "#f4a460",
		"seagreen"				: "#2e8b57",
		"seashell"				: "#fff5ee",
		"sienna"				: "#a0522d",
		"silver"				: "#c0c0c0",
		"skyblue"				: "#87ceeb",
		"slateblue"				: "#6a5acd",
		"slategray"				: "#708090",
		"slategrey"				: "#708090",
		"snow"					: "#fffafa",
		"springgreen"			: "#00ff7f",
		"steelblue"				: "#4682b4",
		"tan"					: "#d2b48c",
		"teal"					: "#008080",
		"thistle"				: "#d8bfd8",
		"tomato"				: "#ff6347",
		"turquoise"				: "#40e0d0",
		"violet"				: "#ee82ee",
		"wheat"					: "#f5deb3",
		"white"					: "#ffffff",
		"whitesmoke"			: "#f5f5f5",
		"yellow"				: "#ffff00",
		"yellowgreen"			: "#9acd32"
	}
	# the default will be the color we are passed
	hexval = color
	color = color.lower()
	if color in svgcolors.keys():
		hexval = svgcolors[color]
	# return the new color (or default if it hasn't changed)
	return hexval

def get_color(self, element, color_string, opacity_string):
	"""
	Return the hex value of the color and opacity of an element
	#RRGGBBAA is returned
	"""
	try:
		# get the color string
		color = element.__getattr__(self, color_string, False)
		# translate the color to hex
		color = color_name_to_hex(color)
	except: color = None
	try:
		opacity = element.__getattr__(self, opacity_string, False)
	except: opacity = "1"
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

def set_color(self, element, color_string, opacity_string, hex_color):
	"""
	Set the color of element using a #RRGGBBAA style color
	"""
	if hex_color[0] == "#":
		color = hex_color[:-2]
		alpha = hex_color[-2:]
		alpha = hex_to_alpha(alpha)
		element.__setattr__(self, color_string, color, False)
		element.__setattr__(self, opacity_string, alpha, False)
	else:
		element.__setattr__(self, color_string, hex_color, False)
		element.__setattr__(self, opacity_string, "1", False)

def print_svg(element, stream):
	"""
	Print a nicely formatted SVG file to a stream
	"""
	stream.write("<?xml version=\"1.0\" standalone=\"no\"?>\n<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">" + "\n\n")
	print_xml(element.element, stream)

def print_xml(element, stream, tabs=""):
	"""
	Print the nicely formatted XML to a stream.
	The stream can be a file or any object with a write(string) function
	"""
	if(element.nodeName != "#text"):
		stream.write(tabs + "<" + element.nodeName)
	try:
		for attribute in element.attributes.keys():
			stream.write(" " + attribute + "=\"" + \
					 str(element.attributes[attribute].value) + "\"")
		if element.childNodes != []:
			stream.write(">\n")
			for child in element.childNodes:
				print_xml(child, stream, tabs + "\t")
			stream.write(tabs + "</" + element.nodeName + ">\n")
		else:
			stream.write("/>\n")
	except: pass

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
