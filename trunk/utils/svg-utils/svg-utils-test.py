#!/usr/bin/env python

"""
	SVG-Utils Test Script
	Used to test SVG-Utils functionality

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
from svg.utils import red, green, blue
from svg.scripts import SVGScript


def test_create_svg():
	"""
	Create an SVG file with some elements
	"""
	print blue("Starting SVG creation test")
	# create our SVG
	print "Creating blank SVG"
	test = SVGFile()

	# add a colored gradient
	print "Adding colored gradient"
	a = test.add_linear_gradient("my_gradient")
	print "Adding gradient stops"
	a.add_stop(color="#ff0000ff", offset="0")
	a.add_stop(color="#00ffffff", offset="1")

	# add a positioned gradient with an xlink for the color
	print "Adding positioned gradient"
	test.add_linear_gradient("full_diag", startx=0, starty=0, stopx=1, stopy=1, xlink="#my_gradient")

	# add a rectangle
	print "Adding rectangle"
	test.add_rect(x="10", y="10", width="40", height="40", fill="url(#full_diag)", stroke="#000000ff", stroke_width="2", roundedx="5", roundedy="5")

	# add a circle
	print "Adding circle"
	test.add_circle(centerx="40", centery="40", radius="15", fill="url(#full_diag)", stroke="#00ff00ff", stroke_width="0.5")

	# add an ellipse
	print "Adding ellipse"
	ellipse = test.add_ellipse(centerx="10", centery="40", radiusx="10", radiusy="20", fill="#ff00ffaa")

	# test some translation and rotation functions
	print "Testing transformation functions"
	ellipse.translate(30, -10)
	ellipse.rotate(5)

	# add a text element
	print "Adding text element"
	text = test.add_text(x="0", y="10", text="Testing...!", fill="#000000ff")
	print "Adding tspan"
	text.add_tspan(x="20", y="5", text="Boo!", fill="#ff0000ff")

	# add a polyline
	print "Adding polyline"
	polyline = test.add_polyline(x="0", y="0", fill="#00ff00ff")
	print "Adding polyline points"
	polyline.add_point(20, 0)
	polyline.add_point(20, 20)
	polyline.add_point(40,20)

	# save the file
	print "Saving SVG"
	test.save("./test.svg")

	print green("SVG Creation test completed")

if __name__ == "__main__":
	try:
		test_create_svg()
	except Exception, err:
		print red("Warning, SVG creation test failed! Error message was:")
		print red(str(err))
