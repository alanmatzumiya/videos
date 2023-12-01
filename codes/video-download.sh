#!/bin/bash


key=$1
value=$2
no_download=false
folderpath=$HOME/Downloads/

if [[ $3 == "--folder" ]]; then
    folderpath=$4
    if [[ $5 == "--only-data" ]]; then
        no_download=true
    fi
fi

if [[ $3 == "--only-data" ]]; then
    no_download=true
    if [[ $4 == "--folder" ]]; then
        folderpath=$5
    fi
fi

yt_url="https://www.youtube.com"
opts="-f mp4 \
--download-archive ids.txt \
--write-description \
--write-info-json \
--write-annotations \
--write-sub \
--write-thumbnail\
"

if $no_download; then
    opts+=" --skip-download"
fi

if [[ $key == "video_id" ]]; then
    cd $folderpath && yt-dlp $opts "$yt_url/watch?v=$value"
elif [[ $key == "playlist_id" ]]; then
    cd $folderpath && yt-dlp $opts "$yt_url/playlist?list=$value"
elif [[ $key == "video_title" ]]; then
    cd $folderpath && yt-dlp $opts "ytsearch:$value"
fi