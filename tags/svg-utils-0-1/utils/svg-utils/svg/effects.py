#!/usr/bin/env python

"""
	effects
	Functions for applying effects and such to SVG files

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

def overlay(svg, overlay, x = 0, y = 0):
	"""
	Overlay an image onto another at (x,y)
	"""
	# move over any gradients/patterns
	if overlay.defs.has_attribute("fills"):
		for defined in overlay.defs.fills:
			svg.defs.add_element(defined)
	# group all the other data we find
	groups, shapes = [], []
	if overlay.has_attribute("groups"):
		groups = overlay.groups
	if overlay.has_attribute("shapes"):
		shapes = overlay.shapes

	new_group = svg.add_group(id = "overlay")
	new_group.translate(x, y)

	for element_type in [groups, shapes]:
		for element in element_type:
			new_group.add_element(element)
