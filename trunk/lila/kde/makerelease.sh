#!/bin/sh

# Script to automate all the copy, generate, delete and archiving work
# required for a proper KDE release.
# Copyright 2005 by Jakob Petsovits
# Distributed under the terms of the GNU General Public License v2


VERSION="" # given as argument
OUTPUTPATH=../release-kde
COLORMODS="blue,red,white"
STATUS="fail"

# arguments parsing

for ARG in $@; do
	if [ "$ARG" = "--help" ]; then
		STATUS="help"
		break
	elif [ "$ARG" = "--nocolormods" ]; then
		COLORMODS=""
	elif [ `echo "$ARG" | grep -- "--colors="` ]; then # if the argument is a colors option
		# extract the color list
		COLORMODS="$ARG"
	else # a version string
		VERSION="$ARG"
		STATUS="pass"
	fi
done

if [ "$STATUS" != "pass" ]; then
	echo
	echo "Usage:"
	echo "$0 --help"
	echo "Displays this help message."
	echo
	echo "$0 [options] version"
	echo "Tries to make a lila-kde release, including color mods,"
	echo "PNG generation from SVG, and tarball creation."
	echo "version is the version number of this release, like '0.8' or '1.4.2'."
	echo
	echo "options: --nocolormods | --colors=list,of,colors"
	echo "By default, a predefined set of color mods will be created."
	echo "You can change this behaviour by handing over a list of colors"
	echo "(e.g. '--colors=blue,red,white') or by specifying '--nocolormods' as option."

	if [ "$STATUS" = "help" ]; then
		exit 0
	else
		exit $E_WRONG_ARGS
	fi
fi


# Part 1: copy

echo "Welcome! This script will try to make the lila-kde $VERSION release"
echo "in $OUTPUTPATH as output path."
echo "These color mods will be created: $COLORMODS"
echo
echo "Cleaning up previous release folder..."
rm -rf $OUTPUTPATH
mkdir -p $OUTPUTPATH

# convert the color list format from "bla,bla,bla" into "bla bla bla"
COLORMODS=`echo "$COLORMODS" | sed -e "s/--colors=//" -e "s/,/ /g"`

echo "Copying this directory's contents to $OUTPUTPATH/lila-kde..."
cp -r . $OUTPUTPATH/lila-kde

# replace %VERSION% in README with the version number
echo "Inserting version number ($VERSION) into README..."
cat README | sed -e "s/%VERSION%/$VERSION/g" > $OUTPUTPATH/lila-kde/README


# Part 2: make color mods

echo
echo "Making color mods..."
for COLOR in $COLORMODS; do
	mkdir $OUTPUTPATH/lila-kde-$COLOR
	./makecolormod.sh $COLOR $OUTPUTPATH/lila-kde $OUTPUTPATH/lila-kde-$COLOR
done


# Part 3: generate PNG files from the SVG sources

echo
echo "Generating PNG files in $OUTPUTPATH/lila-kde..."
echo
sh -c "cd $OUTPUTPATH/lila-kde && ./generate.py --noinstall"
for COLOR in $COLORMODS; do
	echo
	echo "Generating PNG files in $OUTPUTPATH/lila-kde-$COLOR..."
	echo

	# non-creatable files
	cp generate.py $OUTPUTPATH/lila-kde-$COLOR/
	cp *_connecting.mng $OUTPUTPATH/lila-kde-$COLOR/
	cp ChangeLog COPYRIGHT LICENSE README TODO FAQ $OUTPUTPATH/lila-kde-$COLOR/

	# replace the name of the theme with a color specific version
	cat index.desktop \
	  | sed -e "s/Name=.*/Name=Lila $COLOR/" \
	        -e "s/Comment=.*/Comment=A $COLOR version of the Lila Theme/" \
	  > $OUTPUTPATH/lila-kde-$COLOR/index.desktop

	sh -c "cd $OUTPUTPATH/lila-kde-$COLOR && ./generate.py --noinstall"
done


# Part 4: delete unnecessary files and directories

echo
echo "Removing unnecessary files and directories..."
rm -rf $OUTPUTPATH/lila-kde/.svn #> /dev/null
rm -rf $OUTPUTPATH/lila-kde/*/.svn #> /dev/null
rm -rf $OUTPUTPATH/lila-kde/*/*/.svn #> /dev/null
rm -rf $OUTPUTPATH/lila-kde/ksplash #> /dev/null
rm -rf $OUTPUTPATH/lila-kde/scalable #> /dev/null
rm -f $OUTPUTPATH/lila-kde/*.mng #> /dev/null
rm -f $OUTPUTPATH/lila-kde/*.sh #> /dev/null
rm -f $OUTPUTPATH/lila-kde/generate.py #> /dev/null
rm -f $OUTPUTPATH/lila-kde/convert-errors.log #> /dev/null
rm -f $OUTPUTPATH/lila-kde/index-scalable.desktop #> /dev/null

for COLOR in $COLORMODS; do
	rm -rf $OUTPUTPATH/lila-kde-$COLOR/ksplash #> /dev/null
	rm -rf $OUTPUTPATH/lila-kde-$COLOR/scalable #> /dev/null
	rm -f $OUTPUTPATH/lila-kde-$COLOR/*.mng #> /dev/null
	rm -f $OUTPUTPATH/lila-kde-$COLOR/generate.py #> /dev/null
	rm -f $OUTPUTPATH/lila-kde-$COLOR/convert-errors.log #> /dev/null
done


# Part 5: make a tarball

echo
echo "Making tarballs ($OUTPUTPATH/lila-kde[-color]-$VERSION.tar.bz2)..."
sh -c "cd $OUTPUTPATH && tar --create --bzip2 --file lila-kde-$VERSION.tar.bz2 lila-kde"

for COLOR in $COLORMODS; do
	sh -c "cd $OUTPUTPATH && tar --create --bzip2 --file lila-kde-$COLOR-$VERSION.tar.bz2 lila-kde-$COLOR"
done

echo
echo "...Done! Enjoy your fine lila-kde release."
