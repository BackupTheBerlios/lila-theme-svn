#!/bin/sh
# Written by Andrew Conkling (andrewski@fr.st), with the help of the Advanced Bash Scripting Guide (http://www.tldp.org/LDP/abs/html/).
# Modified by Jakob Petsovits (jpetso@gmx.at), with the help of 'info bash' and 'man test'.

#  Ideally, this little scripty-doodle will take any
#+ tarballs in a directory and create a tarball for each
#+ with the appropriate modifications made to match the
#+ colour desired.

if [ $# -lt 1 -o $# -gt 4 ]
then
  echo
  echo "Usage:"
  echo "$0 color [/path/to/svgs [/path/to/output [/path/to/svg-utils]]]"
  echo "The default values for the arguments are:"
  echo "  source-svg path:   . (this directory)"
  echo "  output-svg path:   [svg-path]/../svg-[colorname]"
  echo "  path to svg-utils: /usr/share/svg-utils"
  echo "Beware: Don't let the output path be a subdirectory of the source-svg path."
  echo "        This will cause an infinite recursive loop."
  exit $E_WRONG_ARGS
else
  COLOR=$1
fi

if [ $# -ge 2 ]; then
  SVGPATH=$2;
else
  SVGPATH=.
fi

if [ $# -ge 3 ]; then
  OUTPUTPATH=$3
else
  OUTPUTPATH=$SVGPATH/../svg-$COLOR
fi

if [ $# -eq 4 ]; then
  SVGUTILSPATH=$4
else
  SVGUTILSPATH=/usr/share/svg-utils
fi

mkdir -p $OUTPUTPATH

echo
echo "Making $COLOR color-mod in $OUTPUTPATH..."
$SVGUTILSPATH/svgcolor.py $SVGUTILSPATH/svgcolor-xml/lila/lila-$COLOR.xml $SVGPATH $OUTPUTPATH > /dev/null
if [ $? -ne 0 ]; then
	echo "There was an error while making the color-mod."
	exit 1
else
	echo "$COLOR color-mod has been created."
	exit
fi