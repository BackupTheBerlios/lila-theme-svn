#!/bin/bash

# Script to automate all the copy, generate, delete and archiving work.
# Copyright 2005 Jakob Petsovits
# Distributed under the terms of the GNU General Public License v2


# Before using the script:

# Make sure you have updated the README file with the latest
# release version number, the script won't do that.

OUTPUTPATH=../release-kde


# Part 1: copy

rm -rf $OUTPUTPATH
mkdir $OUTPUTPATH
mkdir $OUTPUTPATH/lila-kde
cp -r . $OUTPUTPATH/lila-kde/lila
mkdir $OUTPUTPATH/lila-kde/lila-blue
mkdir $OUTPUTPATH/lila-kde/lila-red


# Part 2: make color mods

./makecolormod.sh blue $OUTPUTPATH/lila-kde $OUTPUTPATH/lila-kde/lila-blue
./makecolormod.sh red  $OUTPUTPATH/lila-kde $OUTPUTPATH/lila-kde/lila-red


# Part 3: generate PNG files from the SVG sources

# ...leave that for later. At the moment, I can't control generate.py
# with command line arguments, so expect that everything is already
# generated. Have I mentioned that I don't speak Python?

# Side note: When producing color mods, we have to automate generating
# as well, because I don't want to do that manually each time.


# Part 4: delete unnecessary files and directories

#rm -rf CVS */CVS */*/CVS
rm -rf $OUTPUTPATH/lila-kde/lila/ksplash
rm -rf $OUTPUTPATH/lila-kde/lila/scalable
rm -f $OUTPUTPATH/lila-kde/lila/*_connecting.mng
rm -f $OUTPUTPATH/lila-kde/lila/generate.sh
rm -f $OUTPUTPATH/lila-kde/lila/makerelease.sh
rm -f $OUTPUTPATH/lila-kde/lila/makecolormod.sh


# Part 5: make a tarball

tar --create --bzip2 --file $OUTPUTPATH/lila-kde.tar.bz2 $OUTPUTPATH/lila-kde
