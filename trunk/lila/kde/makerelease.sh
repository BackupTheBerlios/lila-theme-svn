#!/bin/bash

# Script to automate all the copy, generate, delete and archiving work.
# Copyright 2005 Jakob Petsovits
# Distributed under the terms of the GNU General Public License v2


# Before using the script:

# Make sure you have updated the README file with the latest
# release version number, the script won't do that.


# Part 1: copy

cd ..
rm -rf lila-kde
mkdir lila-kde
cp kde lila-kde/lila
cd lila-kde/lila


# Part 2: generate PNG files from the SVG sources

# ...leave that for later. At the moment, I can't control generate.py
# with command line arguments, so expect that everything is already
# generated. Have I mentioned that I don't speak Python?

# Side note: When producing color mods, we have to automate generating
# as well, because I don't want to do that manually each time.


# Part 3: delete unnecessary files and directories

rm -rf CVS */CVS */*/CVS
rm -rf ksplash scalable
rm -f *_connecting.mng generate.sh makerelease.sh


# Part 4: make a tarball

cd ../..
tar --create --bzip2 --file lila-kde.tar.bz2 lila-kde
