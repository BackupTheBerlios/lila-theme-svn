#!/usr/bin/env python

from svg.svgfile import SVGFile

# create our SVG
test = SVGFile()

# add a colored gradient
a = test.add_linear_gradient("my_gradient")
a.add_stop(color="#ff0000ff", offset="0")
a.add_stop(color="#00ffffff", offset="1")

# add a positioned gradient with an xlink for the color
test.add_linear_gradient("full_diag", startx=0, starty=0, stopx=1, stopy=1, xlink="#my_gradient")

# add a rectangle
test.add_rect(x="10", y="10", width="40", height="40", fill="url(#full_diag)", stroke="#000000ff", stroke_width="2", roundedx="5", roundedy="5")

# add a circle
test.add_circle(centerx="40", centery="40", radius="15", fill="url(#full_diag)", stroke="#00ff00ff", stroke_width="0.5")

# add an ellipse
ellipse = test.add_ellipse(centerx="10", centery="40", radiusx="10", radiusy="20", fill="#ff00ffaa")

# test some translation and rotation functions
ellipse.translate(30, -10)
ellipse.rotate(5)

# add a text element
text = test.add_text(x="0", y="10", text="Testing...!", fill="#000000ff")
text.add_tspan(x="20", y="5", text="Boo!", fill="#ff0000ff")

# add a polyline
polyline = test.add_polyline(x="0", y="0", fill="#00ff00ff")
polyline.add_point(20, 0)
polyline.add_point(20, 20)
polyline.add_point(40,20)

test.save("/home/dan/test.svg")
