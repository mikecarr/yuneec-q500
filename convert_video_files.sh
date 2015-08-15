#!/bin/sh

for file in *.avc; do ffmpeg -i ${file##*/} ${file##*/}.mov; done
