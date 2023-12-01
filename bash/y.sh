#!/usr/bin/env bash


filename="$HOME/Videos/container/a/videos/ids.txt"
awk '{ for (i=1; i<=NF; i++) print $i }' "$filename"
