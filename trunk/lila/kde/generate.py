#!/usr/bin/python
# Generate icon theme in png


import os, re, string, sys

# Path where you want the icons installed
KDEIconPath = os.path.join(os.path.expanduser("~"), ".kde/share/icons")

# Find inkscape/sodipodi
app = None
if not re.search('^which:', os.popen('which inkscape 2>&1').read()):
	app = 'inkscape'
elif not re.search('^which:', os.popen('which sodipodi 2>&1').read()):
	app = 'sodipodi'
elif not re.search('^which:', os.popen('which rsvg 2>&1').read()):
	app = 'rsvg'
elif not re.search('^which:', os.popen('which ksvgtopng 2>&1').read()):
	app = 'ksvgtopng'
if not app:
	print "No suitable SVG->PNG application found, aborting!"
	sys.exit(42)

sizes = ['16x16', '22x22', '32x32', '48x48']

# Larger?
answer = raw_input("Generate larger icons (64x64 & 128x128)? [y/N]")
if answer == 'y':
	sizes.append('64x64')
	sizes.append('128x128')

print "Autocleaning old icons"
os.popen("rm -r 16x16 22x22 32x32 48x48 64x64 128x128 2>/dev/null")

print "Starting to generate png icons with %s" % (app)
print "Putting errors into ~/lila_errors.log"

for s in sizes:
	try: os.mkdir(s)
	except: pass
	(w,h) = string.split(s, 'x')
	for d in os.listdir('scalable'):
		try: os.mkdir('%s/%s' % (s, d))
		except: pass
		print "Working on %s/%s" % (s, d)
		for f in os.listdir('scalable/%s' % (d)):
			png = re.sub('\.svg', '\.png', f)
			out = s + '/' + d + '/' + png
			if d == 'actions' and f == 'kde.svg':
				wh = '-w %s' % (w)
			elif app == 'ksvgtopng':
				wh = '%s %s' % (w,h)
			elif app == 'sodipodi':
				wh = '-w %s -t %s' % (w,h)
			else:
				wh = '-w %s -h %s' % (w,h)
			if app == 'rsvg':
				cmd = 'rsvg %s scalable/%s/%s %s' % (wh, d, f, out)
			elif app == 'ksvgtopng':
				cmd = 'ksvgtopng %s scalable/%s/%s %s' % (wh, d, f, out)
			else:
				cmd = '%s -z %s -e %s -f scalable/%s/%s' % (app, wh, out, d, f)
			os.popen(cmd + " 2>>~/lila_errors.log")
			#print cmd

# Manually copy certain icons that can't be auto-generated properly, or at all
os.popen("cp *_connecting.mng 16x16/actions")

print "Done!"

answer = raw_input("Install to %s? [y/N] " % (KDEIconPath))
if answer == 'y':
	os.popen("rm -rf %s/lila" % (KDEIconPath))
	os.popen("mkdir %s/lila" % (KDEIconPath))
	os.popen("cp -r 16x16 22x22 32x32 48x48 64x64 128x128 scalable index.desktop %s/lila" % (KDEIconPath))
	print "Done!"
else:
	print answer
