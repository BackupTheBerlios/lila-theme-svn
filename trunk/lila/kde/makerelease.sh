#!/bin/sh

# Script to automate all the copy, generate, delete and archiving work
# required for a proper KDE release.
# Copyright 2005 Jakob Petsovits
# Distributed under the terms of the GNU General Public License v2


# Before using the script:

# Make sure you have updated the README file with the latest
# release version number, the script won't do that.

if [ "$1" = "--help" ] # duplicating contents is not exactly clean, but I don't want to do extensive research for this.
then
  echo
  echo "Usage:"
  echo "$0 color [/path/to/svgs [/path/to/output [/path/to/svg-utils]]]"
  echo "This script will try to make a lila-kde release, including"
  echo "color mods, PNG generation from SVG, and tarball creation."
  exit 0
fi

OUTPUTPATH=../release-kde
COLORMODS="blue red"


# Part 1: copy

echo "Welcome! This script will try to make a lila-kde release"
echo "in $OUTPUTPATH as output path."
echo
echo "Cleaning up previous release folder..."
rm -rf $OUTPUTPATH
mkdir -p $OUTPUTPATH/lila-kde

echo "Copying this directory's contents to $OUTPUTPATH/lila-kde/lila-kde..."
cp -r . $OUTPUTPATH/lila-kde/lila-kde


# Part 2: make color mods

echo
echo "Making color mods..."
for COLOR in $COLORMODS; do
	mkdir $OUTPUTPATH/lila-kde/lila-kde-$COLOR
	./makecolormod.sh $COLOR $OUTPUTPATH/lila-kde/lila-kde $OUTPUTPATH/lila-kde/lila-kde-$COLOR
done


# Part 3: generate PNG files from the SVG sources

echo
echo "Generating PNG files in $OUTPUTPATH/lila-kde/lila-kde..."
echo
sh -c "cd $OUTPUTPATH/lila-kde/lila-kde && ./generate.py --noinstall"
for COLOR in $COLORMODS; do
	echo
	echo "Generating PNG files in $OUTPUTPATH/lila-kde/lila-kde-$COLOR..."
	echo

	# non-creatable files
	cp generate.py $OUTPUTPATH/lila-kde/lila-kde-$COLOR/
	cp *_connecting.mng $OUTPUTPATH/lila-kde/lila-kde-$COLOR/
	cp ChangeLog COPYRIGHT LICENSE README TODO FAQ $OUTPUTPATH/lila-kde/lila-kde-$COLOR/
	cp index-$COLOR.desktop $OUTPUTPATH/lila-kde/lila-kde-$COLOR/index.desktop

	sh -c "cd $OUTPUTPATH/lila-kde/lila-kde-$COLOR && ./generate.py --noinstall"
done


# Part 4: delete unnecessary files and directories

echo
echo "Removing unnecessary files and directories..."
rm -rf $OUTPUTPATH/lila-kde/lila-kde/.svn #> /dev/null
rm -rf $OUTPUTPATH/lila-kde/lila-kde/*/.svn #> /dev/null
rm -rf $OUTPUTPATH/lila-kde/lila-kde/*/*/.svn #> /dev/null
rm -rf $OUTPUTPATH/lila-kde/lila-kde/ksplash #> /dev/null
rm -rf $OUTPUTPATH/lila-kde/lila-kde/scalable #> /dev/null
rm -f $OUTPUTPATH/lila-kde/lila-kde/*_connecting.mng #> /dev/null
rm -f $OUTPUTPATH/lila-kde/lila-kde/generate.py #> /dev/null
rm -f $OUTPUTPATH/lila-kde/lila-kde/makerelease.sh #> /dev/null
rm -f $OUTPUTPATH/lila-kde/lila-kde/makecolormod.sh #> /dev/null
rm -f $OUTPUTPATH/lila-kde/lila-kde/convert-errors.log #> /dev/null
rm -f $OUTPUTPATH/lila-kde/lila-kde/index-scalable.desktop #> /dev/null

for COLOR in $COLORMODS; do
	rm -rf $OUTPUTPATH/lila-kde/lila-kde-$COLOR/ksplash #> /dev/null
	rm -rf $OUTPUTPATH/lila-kde/lila-kde-$COLOR/scalable #> /dev/null
	rm -f $OUTPUTPATH/lila-kde/lila-kde-$COLOR/generate.py #> /dev/null
	rm -f $OUTPUTPATH/lila-kde/lila-kde-$COLOR/convert-errors.log #> /dev/null
	rm -f $OUTPUTPATH/lila-kde/lila-kde-$COLOR/*_connecting.mng #> /dev/null
	rm -f $OUTPUTPATH/lila-kde/lila-kde/index-$COLOR.desktop #> /dev/null
done


# Part 5: make a tarball

echo
echo "Making tarballs ($OUTPUTPATH/lila-kde[-color].tar.bz2)..."
sh -c "cd $OUTPUTPATH/lila-kde && tar --create --bzip2 --file lila-kde.tar.bz2 lila-kde"

for COLOR in $COLORMODS; do
	sh -c "cd $OUTPUTPATH/lila-kde && tar --create --bzip2 --file lila-kde-$COLOR.tar.bz2 lila-kde-$COLOR"
done

echo
echo "...Done! Enjoy your fine lila-kde release."
