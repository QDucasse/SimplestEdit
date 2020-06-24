#!/bin/bash
echo "Starting conversion..."
for filename in *.pdf; do
    [ -e "$filename" ] || continue
    magick -density 400 $filename[0] ${filename%.*}.png
done
echo "Conversion completed!"
