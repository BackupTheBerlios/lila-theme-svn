#!/bin/sh

# Script to automate all the copy, generate, delete and archiving work
# required for a proper KDE release.
# Copyright 2005 Jakob Petsovits
# Distributed under the terms of the GNU General Public License v2


# Before using the script:

# Make sure you have updated the README file with the latest
# release version number, the script won't do that.

OUTPUTPATH=../release-kde
COLORMODS="blue red"


# Part 1: copy

echo "Welcome! This script will try to make a lila-kde release"
echo "in $OUTPUTPATH as output path."
echo
echo "Cleaning up previous release folder..."
rm -rf $OUTPUTPATH
mkdir -p $OUTPUTPATH/lila-kde

echo "Copying this directory's contents to $OUTPUTPATH/lila-kde/lila..."
cp -r . $OUTPUTPATH/lila-kde/lila


# Part 2: make color mods

echo
echo "Making color mods..."
for COLOR in $COLORMODS; do
	mkdir $OUTPUTPATH/lila-kde/lila-$COLOR
	./makecolormod.sh $COLOR $OUTPUTPATH/lila-kde/lila $OUTPUTPATH/lila-kde/lila-$COLOR
done


# Part 3: generate PNG files from the SVG sources

echo
echo "Generating PNG files in $OUTPUTPATH/lila-kde/lila..."
echo
sh -c "cd $OUTPUTPATH/lila-kde/lila && ./generate.py --noinstall"
for COLOR in $COLORMODS; do
	echo
	echo "Generating PNG files in $OUTPUTPATH/lila-kde/lila-$COLOR..."
	echo
	cp generate.py $OUTPUTPATH/lila-kde/lila-$COLOR/
	cp *_connecting.mng $OUTPUTPATH/lila-kde/lila-$COLOR/  # non-creatable files
	sh -c "cd $OUTPUTPATH/lila-kde/lila-$COLOR && ./generate.py --noinstall"
done


# Part 4: delete unnecessary files and directories

echo
echo "Removing unnecessary files and directories..."
rm -rf $OUTPUTPATH/lila-kde/lila/ksplash
rm -rf $OUTPUTPATH/lila-kde/lila/scalable
rm -f $OUTPUTPATH/lila-kde/lila/*_connecting.mng
rm -f $OUTPUTPATH/lila-kde/lila/generate.py
rm -f $OUTPUTPATH/lila-kde/lila/makerelease.sh
rm -f $OUTPUTPATH/lila-kde/lila/makecolormod.sh

for COLOR in "$COLORS"; do
	rm -rf $OUTPUTPATH/lila-kde/lila-$COLOR/ksplash
	rm -rf $OUTPUTPATH/lila-kde/lila-$COLOR/scalable
	rm -f $OUTPUTPATH/lila-kde/lila-$COLOR/generate.py
done


# Part 5: make a tarball

echo
echo "Making a tarball ($OUTPUTPATH/lila-kde.tar.bz2)..."
tar --create --bzip2 --file $OUTPUTPATH/lila-kde.tar.bz2 $OUTPUTPATH/lila-kde

echo
echo "...Done! Enjoy your fine lila-kde release."