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

from svgfile import SVGFile

def print_gradients(gradients, gradient_type):
	"""
	Print out the gradients and stops returned by
	SVGFile.get_linear_gradients or SVGFile.get_radial_gradients
	"""
	for gradient in gradients:
		stops = gradient.get_stops()
		if stops:
			print gradient_type + " Gradient '" + gradient.get_name() + "'"
			for stop in stops:
				print "\tStop '" + stop.get_name() + "': " + stop.get_color()
		else:
			xlink = gradient.get_xlink()
			if xlink:
				print gradient_type + " Gradient '" + gradient.get_name() + "'"
				print "\tXLink: " + xlink

def print_object_data(objects, object_type):
	"""
	Print out the objects' fill and stroke colors
	objects should be a list of Rects, Paths, or Polygons
	"""
	for object in objects:
		print object_type + " '" + object.get_name() + "':"
		fill = object.get_fill_color()
		stroke = object.get_stroke_color()
		if fill:
			if fill[:3] == "url":
				print "\tFill Link: " + fill[4:-3]
				print "\tFill Opacity: " + fill[-2:]
			else:
				print "\tFill Color: " + fill
		if stroke:
			print "\tStroke Color: " + stroke

def print_svg_color_data(linear_gradients, radial_gradients, rects, \
						circles, ellipses, lines, polylines, polygons, \
						paths, texts, tspans, trefs, text_paths, groups):
	"""
	Print out all the color data from an svg image nicely
	"""
	# print out the data
	print_gradients(linear_gradients, "Linear")
	print_gradients(radial_gradients, "Radial")
	print_object_data(rects, "Rect")
	print_object_data(circles, "Circle")
	print_object_data(ellipses, "Ellipse")
	print_object_data(lines, "Line")
	print_object_data(polylines, "Polyline")
	print_object_data(polygons, "Polygon")
	print_object_data(paths, "Path")
	print_object_data(texts, "Text")
	print_object_data(tspans, "TSpan")
	print_object_data(trefs, "TRef")
	print_object_data(text_paths, "Text Path")
	print_object_data(groups, "Group")

if __name__ == "__main__":
	from sys import argv, exit
	import os

	# check if we are doing a single or multi file search
	if len(argv) != 2:
		print "svgdump: A utility for dumping SVG information"
		print "Copyright 2004 Daniel G. Taylor, released under the GNU GPL"
		print "Usage:"
		print "svgdump file.svg"
		print "svgdump /path/to/search/for/svgs"
		print "Note that the SVG files must have an svg extension for them to be included!"
		exit()

	path = argv[1]

	if not os.path.exists(path):
		print "That path does not exist!"
		exit()

	if os.path.isfile(path):
		# single file, so let's print out some info
		svg = SVGFile(path)
		print "Name: " + svg.get_name()
		print "Width: " + svg.get_width()
		print "Height: " + svg.get_height()
		ink_ver = svg.get_inkscape_version()
		sod_ver = svg.get_sodipodi_version()
		xmlns = svg.get_xmlns()
		xmlns_ink = svg.get_xmlns_inkscape()
		xmlns_sod = svg.get_xmlns_sodipodi()
		xmlns_x = svg.get_xmlns_xlink()
		if ink_ver:
			print "Inkscape Version: " + ink_ver
		if sod_ver:
			print "Sodipodi Version: " + sod_ver
		if xmlns:
			print "XML Namespace: " + xmlns
		if xmlns_ink:
			print "Inkscape Namespace: " + xmlns_ink
		if xmlns_sod:
			print "Sodipodi Namespace: " + xmlns_sod
		if xmlns_x:
			print "Xlink Namespace: " + xmlns_x

		# get the image's info
		linear_gradients = svg.get_linear_gradients()
		radial_gradients = svg.get_radial_gradients()
		rects = svg.get_rects()
		circles = svg.get_circles()
		ellipses = svg.get_ellipses()
		lines = svg.get_lines()
		polylines = svg.get_polylines()
		polygons = svg.get_polygons()
		paths = svg.get_paths()
		texts = svg.get_texts()
		tspans = svg.get_tspans()
		trefs = svg.get_trefs()
		text_paths = svg.get_text_paths()
		groups = svg.get_groups()

		# print out the color data
		print_svg_color_data(linear_gradients, radial_gradients, rects, \
							circles, ellipses, lines, polylines, polygons, \
							paths, texts, tspans, trefs, text_paths, groups)

	elif os.path.isdir(path):
		# multiple files, let's get all the colors
		def crawl_dir(path, lg, rg, r, c, e, l, pl, pg, pa, te, ts, tr, tp, g):
			"""
			recursively crawl a directory and get all the used
			gradients and colors of the SVG files within
			"""
			print "Scanning " + path
			# for each file or dir (let's just call it a node)
			for node in os.listdir(path):
				abspath = os.path.join(path, node)
				if os.path.isfile(abspath) and node[-3:].lower() == "svg":
					# parse the file
					svg = SVGFile(abspath)
					# let's get the file's data
					linear_gradients = svg.get_linear_gradients()
					radial_gradients = svg.get_radial_gradients()
					rects = svg.get_rects()
					circles = svg.get_circles()
					ellipses = svg.get_ellipses()
					lines = svg.get_lines()
					polylines = svg.get_polylines()
					polygons = svg.get_polygons()
					paths = svg.get_paths()
					texts = svg.get_texts()
					tspans = svg.get_tspans()
					trefs = svg.get_trefs()
					text_paths = svg.get_text_paths()
					groups = svg.get_groups()
					# add unique values to the passed containers
					for gradient in linear:
						color = []
						for stop in gradient.get_stops():
							color.append(stop.get_color())
						if color not in lg:
							lg.append(color)
					for gradient in radial:
						color = []
						for stop in gradient.get_stops():
							color.append(stop.get_color())
						if color not in rg:
							rg.append(color)
					for objs,ls in [(rects, r), (circles, c), (ellipses, e), (lines, l), (polylines, pl), (polygons, pg), (paths, pa), (texts, te), (tspans, ts), (trefs, tr), (text_paths, tp), (groups, g)]:
						for obj in objs:
							fcolor = obj.get_fill_color()
							scolor = obj.get_stroke_color()
							# we don't care about url() links right now
							if fcolor:
								fcolor.strip()
								if fcolor[:3] == "url":
									fcolor = None
							if scolor:
								scolor.strip()
								if scolor[:3] == "url":
									scolor = None
							if (fcolor, scolor) not in ls:
								ls.append((fcolor, scolor))

				elif os.path.isdir(abspath):
					# oh, fun! recursion!
					crawl_dir(abspath, lg, rg, r, c, e, l, pl, pg, pa, te, ts, tr, tp, g)

		def print_multi(lg, rg, r, c, e, l, pl, pg, pa, te, ts, tr, tp, g):
			"""
			Print out the info from multiple files
			This only prints out the colors from the lists passed to it
			"""
			for gradient in lg:
				if len(gradient):
					print "Linear Gradient:"
				for color in gradient:
					print "\tStop: " + color
			for gradient in rg:
				if len(gradient):
					print "Radial Gradient:"
				for color in gradient:
					print "\tStop: " + color
			for objs,name in [(r, "Rect"), (c, "Cirlce"), (e, "Elipse"), (l, "Line"), (pl, "Polyline"), (pg, "Polygon"), (pa, "Path"), (te, "Text"), (ts, "TSpan"), (tr, "TRef"), (tp, "Text Path"), (g, "Group")]:
				for obj in objs:
					fill, stroke = obj
					if fill or stroke:
						print name + ":"
					if fill:
						print "\tFill: " + fill
					if stroke:
						print "\tStroke: " + stroke

		# =====================================================================
		print "Multi-file mode activated, printing all found gradients and colors:"
		lg, rg, r, c, e, l, pl, pg, pa, te, ts, tr, tp, g = \
		([], [], [], [], [], [], [], [], [], [], [], [], [], [])
		crawl_dir(path, lg, rg, r, c, e, l, pl, pg, pa, te, ts, tr, tp, g)
		# print out all the data
		print_multi(lg, rg, r, c, e, l, pl, pg, pa, te, ts, tr, tp, g)
