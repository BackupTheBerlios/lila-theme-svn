#!/usr/bin/env python

"""
	svgutils
	Utility functions for the svg-utils package

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

def get_style_element(style, element, default = None):
	"""
	Returns the value of an element in a style string
	style can be any style string like "stop-color:#ffffff;stop-opacity:1;"
	element can be any element within that string, like "stop-color:"
	note that the element must end with the colon!
	"""
	# find the position of the element in the string
	element_start = style.find(element)
	if element_start == -1:
		# if it can't be found just return the default
		return default
	else:
		# else, add the length of the element (to get to it's value)
		element_start += len(element)
		# then find the end of the value denoted by a ;
		element_stop = style.find(";", element_start)
		# return just the element's value
		return style[element_start : element_stop]

def replace_style_element(style, element, new_value):
	"""
	Returns a style string with the given element replaced with
	the string in new_value. Example:
	Given:
		style = 'stop-color: #123456; stop-opacity: 1.0;'
		element = 'stop-opacity:'
		new_value = '0.8'
	It will return:
		'stop-color: #123456; stop-opacity: 0.8;'
	If there is an error, -1 is returned
	Note that the element must end in a colon!
	"""
	# find the position of the element in the string
	element_start = style.find(element)
	if element_start == -1:
		# if it can't be found just add it on to the style string
		style_string = style + " " + element + " " + new_value + ";"
	else:
		# else, add the length of the element (to get to it's value)
		element_start += len(element)
		# then find the end of the value denoted by a ;
		element_stop = style.find(";", element_start)
		# compose the new style string
		style_string = style[:element_start] + " " + new_value + style[element_stop:]
		# return the new style string
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
	# return the new color (or default if it hasn't changed)
	return hexval

def get_color(element, color_string, opacity_string):
	"""
	Return the color of an element (such as a stop or fill)
	color_string should be something like 'stop-color:'
	opacity_string should be something like 'stop-opacity:'
	"""
	style = element.getAttribute("style")
	color = get_style_element(style, color_string)
	# make sure we aren't just getting a link
	if color and color != "none":
		color = color.strip()
		# make sure the color is in hex
		color = color_name_to_hex(color)
		opacity = get_style_element(style, opacity_string, "1")
		# make sure the color's length is right
		if len(color) < 7:
			color = color[:2] + color[1] + color[2] + color[2] + color[3] + color[3]
		# convert opacity to hex
		opacity = alpha_to_hex(opacity)
		return color + opacity
	# if we got a link or error return -1
	return -1

def set_color(element, color_string, opacity_string, color):
	"""
	Set the color of an element (such as a stop or fill)
	color_string should be something like 'stop-color:'
	opacity_string should be something like 'stop-opacity:'
	color should be something like '#000000ff'
	"""
	style = element.getAttribute("style")
	c = color[:-2]
	a = color[-2:]
	a = hex_to_alpha(a)
	style = replace_style_element(style, color_string, c)
	style = replace_style_element(style, opacity_string, a)
	if style != -1:
		element.setAttribute("style", style)
