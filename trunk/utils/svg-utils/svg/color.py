#!/usr/bin/env python

"""
	Color
	SVG color modification functions

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

def color_to_grayscale(color):
	"""
	Return the grayscale version of color
	color must be in hex (i.e. #000000ff)
	Note that the alpha value is NOT changed!
	"""
	# grab the different colors
	red = color[1:3]
	green = color[3:5]
	blue = color[5:7]
	# find the average
	gray = hex((int(red, 16) + int(green, 16) + int(blue, 16)) / 3)[2:]
	# return the grayscale value
	return "#" + gray + gray + gray + color[-2:]

def grayscale(svg):
	"""
	Convert an svg to grayscale
	svg should be an SVGFile (but can also be any container element)
	"""
	# change the gradient stop colors
	for gradient in svg.all_gradients:
		for stop in gradient.stops:
			try:
				stop.color = color_to_grayscale(stop.color)
			except: pass

	# change the shape and group fill/stroke colors
	for shapes in [svg.all_shapes, svg.all_groups]:
		for shape in shapes:
			try:
				fill = shape.fill
				if fill[0] == "#":
					shape.fill = color_to_grayscale(fill)
			except: pass
			try:
				stroke = shape.stroke
				if stroke[0] == "#":
					shape.stroke = color_to_grayscale(stroke)
			except: pass
