#!/usr/bin/env python

"""
	svgoverlay
	Overlay one SVG file on top of another

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

from svg import SVGFile
from svg.effects import overlay

if __name__ == "__main__":
	from sys import argv, exit
	from os.path import basename

	if len(argv) not in [3, 4, 5, 6]:
		print "svgoverlay: Overlay SVG images"
		print "Copyright 2004 Daniel G. Taylor, released under the GNU GPL"
		print "Usage:"
		print "svgoverlay file.svg overlay.svg [file_to_save]"
		print "svgoverlay file.svg overlay.svg x_position y_position [file_to_save]"
		exit()

	# this has to be the same no matter how called
	filename = argv[1]
	overlay_filename = argv[2]

	# set some defaults
	file_to_save = None
	x_position = 0
	y_position = 0

	# get the actual options
	if len(argv) == 4:
		file_to_save = argv[3]
	elif len(argv) in [5, 6]:
		x_position = argv[3]
		y_position = argv[4]
		if len(argv) == 6:
			file_to_save = argv[5]

	print "Overlaying: " + basename(filename) + " + " + basename(overlay_filename) + " -> " + (file_to_save and file_to_save or basename(filename))

	# load the files
	svg = SVGFile(filename)
	overlay_svg = SVGFile(overlay_filename)

	# do the overlay
	overlay(svg, overlay_svg, x_position, y_position)

	# save the new file
	svg.save(file_to_save)
