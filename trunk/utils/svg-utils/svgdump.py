#!/usr/bin/env python

"""
	svgdump
	Load an SVG image and dump some information to the screen

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

from svg.svgfile import SVGFile

def print_info(element, tabs = ''):
	"""
	Print information about an SVG element
	"""
	try:
		# get any containers
		for container in element.containers:
			if container.tag == "defs": tag = "Defs"
			elif container.tag == "g": tag = "Group"
			print tabs + tag
			print tabs + "  Name: " + container.id
			print_info(container, tabs + "  ")
	except: pass
	try:
		# get the gradients
		for grad in element.gradients:
			print tabs + grad.tag
			print tabs + "  Name: " + grad.id
			for stop in grad.stops:
				print tabs + "  Stop"
				print tabs + "    Name: " + stop.id
				print tabs + "    Color: " + stop.color
				print tabs + "    Offset: " + stop.offset
			if grad.has_attribute("xlink"):
				print tabs + "  xlink: " + grad.xlink
	except: pass
	try:
		# get the shapes
		for shape in element.shapes:
			print tabs + shape.tag
			print tabs + "  Name: " + shape.id
			if shape.has_attribute("fill"):
				print tabs + "  Fill: " + shape.fill
			if shape.has_attribute("stroke"):
				print tabs + "  Stroke: " + shape.stroke
	except: pass

if __name__ == "__main__":
	from sys import argv, exit
	import os

	# check if we are doing a single or multi file search
	if len(argv) != 2:
		print "svgdump: A utility for dumping SVG information"
		print "Copyright 2004 Daniel G. Taylor, released under the GNU GPL"
		print "Usage:"
		print "svgdump file.svg"
		exit()

	path = argv[1]

	if not os.path.exists(path):
		print "That path does not exist!"
		exit()

	svg = SVGFile(path)

	print "Name: " + svg.id
	print "Width: " + svg.width
	print "Height: " + svg.height
	print_info(svg)
