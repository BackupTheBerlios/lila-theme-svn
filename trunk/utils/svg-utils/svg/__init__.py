#!/usr/bin/env python

"""
	Python SVG Manipulation Library
	===============================
		A library for creating and editing SVG files.
		
		About the SVG Specification
		---------------------------
		This software implements part of the W3C SVG 1.1 Specification.
		Access to objects and data have been changed for ease-of-use.
		For more information on SVG, see:
		U{http://www.w3.org/TR/SVG11/}
		
		Usage
		-----
		Most of the various classes and functions you will need in general use
		are imported into this module by default, so you should only have to
		C{import svg} and will have access most stuff directly (e.g. C{svg.SVGFile()}
		and such).

		License
		-------
		Copyright (C) 2005 Daniel G. Taylor

		This program is free software; you can redistribute it and/or modify
		it under the terms of the GNU General Public License as published by
		the U{Free Software Foundation<http://www.fsf.org>}; either version 2
		of the License, or (at your option) any later version.

		This program is distributed in the hope that it will be useful,
		but WITHOUT ANY WARRANTY; without even the implied warranty of
		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
		GNU General Public License for more details.

		You should have received a copy of the GNU General Public License
		along with this program; if not, write to the Free Software
		Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

# use imports to create shortcuts to make the library easier to use
from svgfile import SVGFile
from scripts import SVGScript
from elements import *
from containers import *
from error import *

# some data on the library
authors = [("Daniel G. Taylor", "http://programmer-art.org")]
copyright = "Copyright 2005 Daniel G. Taylor"
homepage = "http://programmer-art.org/svg-utils"
documentation = "http://programmer-art.org/svg-utils-documentation"
version = "0.2"
