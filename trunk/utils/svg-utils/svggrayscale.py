#!/usr/bin/env python

"""
	svggrayscale
	Convert SVG images to grayscale

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

from svg import SVGFile, SVGScript
from svg.color import grayscale

from os.path import basename

def convert_svg_to_grayscale(filename, file_to_save = None):
	"""
	Take a filename to an SVG image and convert it to grayscale
	if file_to_save is None, it will overwrite the file!
	"""
	print "Grayscaling: " + basename(filename) + " -> " + (file_to_save and file_to_save or basename(filename))

	# open and parse the file
	svg = SVGFile(filename)

	# grayscale the image
	grayscale(svg)

	# save the file
	svg.save(file_to_save)

if __name__ == "__main__":
	from sys import argv, exit
	import os

	# check if we are doing a single or multi file search
	if len(argv) not in [2, 3]:
		print "svggrayscale: Convert SVG images to grayscale"
		print "Copyright 2004 Daniel G. Taylor, released under the GNU GPL"
		print "Usage:"
		print "svggrayscale file.svg [newname.svg]"
		print "svggrayscale /path/to/search/for/svgs [/path/to/put/new/svgs]"
		print "Note that the SVG files must have an svg extension for them to be included!"
		exit()

	path = argv[1]

	try: save = argv[2]
	except: save = None

	# setup the script and run it :)
	script = SVGScript(path, convert_svg_to_grayscale, save)

	try:
		script.run()
	except IOError, err:
		print str(err)
		exit()
