#!/usr/bin/python
# Generate icon theme in png

import os, re, string, sys

# Path where you want the icons installed
KDEIconPath = os.path.join(os.path.expanduser("~"), ".kde/share/icons")

if sys.argv.count("--help") >= 1 or sys.argv.count("-h") >= 1:
	print "usage: %s [options]" % sys.argv[0]
	print "Command Line Options:"
	print "--install:   Install the converted icons for KDE without asking"
	print "--noinstall: Don't even ask for installing the converted icons"
	print "-h, --help:  Display this message\n"
	sys.exit(0)

# Find an SVG->PNG converter
app = None
if not re.search('^which:', os.popen('which inkscape 2>&1').read()):
	app = 'Inkscape'
	w = '-w'
	h = '-h'
elif not re.search('^which:', os.popen('which sodipodi 2>&1').read()):
	app = 'Sodipodi'
	w = '-w'
	h = '-t'
elif not re.search('^which:', os.popen('which rsvg 2>&1').read()):
	app = 'rsvg'
	w = '-w'
	h = '-h'
elif not re.search('^which:', os.popen('which ksvgtopng 2>&1').read()):
	app = 'ksvgtopng'
	w = ''
	h = ''
if not app:
	print "No suitable SVG->PNG application found, aborting!"
	sys.exit(42)

sizes = ['16x16', '22x22', '32x32', '48x48', '64x64', '128x128']

print "Autocleaning old icons..."
os.popen("rm -r 16x16 22x22 32x32 48x48 64x64 128x128 2>/dev/null")

print "Starting to generate PNG icons with %s." % (app)
print "%s's error output goes into ./convert-errors.log" % (app)

# create and process all size dirs
for size in sizes:

	try: os.mkdir(size)
	except: pass

	(width,height) = string.split(size, 'x')
	print "\nWorking on %s icons:" % (size)

	# create and process subdirectories like apps, mimetypes and such
	for subdir in os.listdir('scalable'):

		try: os.mkdir('%s/%s' % (size, subdir))
		except: pass

		if subdir[0] == ".":
			continue;

		print "   %s/" % (subdir)

		# convert every .svg file in this directory
		for filename in os.listdir('scalable/%s' % (subdir)):

			if filename[-4:] != ".svg":
				continue

			filenamepng = re.sub('\.svg', '\.png', filename)
			outputpath = size + '/' + subdir + '/' + filenamepng

			# width and height parameters for the specific app
			if subdir == 'actions' and filename == 'kde.svg':
				widthheight = '%s %s' % (w, width)
			else:
				widthheight = '%s %s %s %s' % (w, width, h, height)

			# construct the command line
			if app == 'Inkscape':
				command = 'inkscape -z %s -f scalable/%s/%s -e %s' % (widthheight, subdir, filename, outputpath)
			elif app == 'Sodipodi':
				command = 'sodipodi -z %s -f scalable/%s/%s -e %s' % (widthheight, subdir, filename, outputpath)
			elif app == 'rsvg':
				command = 'rsvg %s scalable/%s/%s %s' % (widthheight, subdir, filename, outputpath)
			elif app == 'ksvgtopng':
				command = 'ksvgtopng %s scalable/%s/%s %s' % (widthheight, subdir, filename, outputpath)

			# Go for it!
			os.popen(command + " 2>>./convert-errors.log")
			#print command  # debug

# Manually copy certain icons that can't be auto-generated properly, or at all
os.popen("cp *_connecting.mng 16x16/actions")

print "PNG icons have been generated!"

answer = None
if sys.argv.count("--install") >= 1:
	answer = 'y'
if sys.argv.count("--noinstall") >= 1:
	answer = 'n'
if not answer:
	answer = raw_input("Install to %s? [y/n] " % (KDEIconPath))

if answer == 'y':
	os.popen("rm -rf %s/lila" % (KDEIconPath))
	os.popen("mkdir %s/lila" % (KDEIconPath))
	os.popen("cp -r 16x16 22x22 32x32 48x48 64x64 128x128 scalable index.desktop %s/lila" % (KDEIconPath))
	print "Icons have been installed to %s." % (KDEIconPath)
else:
	print "Icons have not been installed to %s." % (KDEIconPath)
