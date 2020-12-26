#!/bin/bash

########## Weired resolotions directory ##########
wrd="$HOME/Desktop/Weired_resolotions"

########## Requirement ##########
# ffmpeg	: For editing mp4 metadata
# exiftool	: For editing jpg metadata

resolution(){
	#$1 chemin
	#$2 video=0 else image

	if [ $2 -eq 0 ] ; then
		height=$(ffprobe -v error -show_streams "$1" | grep ^height=)
		height=${height:7}
		width=$(ffprobe -v error -show_streams "$1" | grep ^width=)
		width=${width:6}
	else
		height=$(exiftool -s -s -s -ImageHeight "$1")
		width=$(exiftool -s -s -s -ImageWidth "$1")
	fi
	param=''
	if [ $(echo $width / $height | bc -l) = $(echo 16 / 9 | bc -l) ] ; then
		if [ $height -gt 720 ] ; then
			param='scale=1280:720'
		fi
	elif [ $(echo $width / $height | bc -l) = $(echo 9 / 16 | bc -l) ] ; then
		if [ $height -gt 720 ] ; then
			param='scale=720:1280'
		fi
	elif [ $(echo $width / $height | bc -l) = $(echo 4 / 3 | bc -l) ] ; then
		if [ $height -gt 720 ] ; then
			param='scale=960:720'

		fi
	elif [ $(echo $width / $height | bc -l) = $(echo 3 / 4 | bc -l) ] ; then
		if [ $height -gt 720 ] ; then
			param='scale=720:960'
		fi
	elif [ $width -eq $height ] ; then
		if [ $height -gt 720 ] ; then
			param='scale=720:720'
		fi
	else
		ln -s "$1" "$wrd"
		param='weired'
	fi

}

racine="$1/"
if ! [ "$1" ] ; then
	racine="./"
fi

if ! [ -d "$wrd" ] ; then
	mkdir "$wrd"
fi

IFS=$'\n' #Input Field Separator : for i in mas'\n'assa'\n'qdfr

for i in $(ls -1 "$racine" ) ; do
	chemin="$racine$i"
	if [ -f "$chemin" ] ; then
		if [ $(echo "$chemin" | grep .mp4$) ] ; then
			if ! [ $(ffprobe -v error -show_format "$chemin" | grep ^TAG:comment=vlcuser_compression) ] ; then
				resolution "$chemin" 0
				if ! [ $param ] ; then
					echo "working on $chemin"
					mv "$chemin" "$chemin"_brute.mp4
					ffmpeg -v error -i "$chemin"'_brute.mp4' -metadata comment=vlcuser_compression "$chemin"
					if ! [ $? -eq 0 ] ; then
						mv "$chemin"_brute.mp4 "$chemin"
						exit 1
					fi
					rm "$chemin"_brute.mp4

				elif ! [ "$param" = 'weired' ] ; then
					echo "working on $chemin"
					mv "$chemin" "$chemin"_brute.mp4
					ffmpeg -v error -i "$chemin"'_brute.mp4' -vf "$param" -metadata comment=vlcuser_compression "$chemin"
					if ! [ $? -eq 0 ] ; then
						mv "$chemin"_brute.mp4 "$chemin"
						exit 1
					fi
					rm "$chemin"_brute.mp4
				fi
			fi
		fi
		if [ $(echo $chemin | grep .jpg$) ] ; then
			comment=$(exiftool -args -Comment $chemin)
			if  ! [ "$comment" ] || ( ! [ "$comment" = '-Comment=vlcuser_compression' ] ) ; then
				resolution "$chemin" 1
				if ! [ $param ] ; then
					echo "working on $chemin"
					mv "$chemin" "$chemin"_brute.jpg
					ffmpeg -v error -i "$chemin"'_brute.jpg' "$chemin"
					if ! [ $? -eq 0 ] ; then
						mv "$chemin"_brute.jpg "$chemin"
						exit 1
					fi
					exiftool -Comment=vlcuser_compression -overwrite_original "$chemin" > ~/Desktop/exiftool.carbage ; rm ~/Desktop/exiftool.carbage
					rm "$chemin"_brute.jpg

				elif ! [ "$param" = 'weired' ] ; then
					echo "working on $chemin"
					mv "$chemin" "$chemin"_brute.jpg
					ffmpeg -v error -i "$chemin"'_brute.jpg' -vf "$param" "$chemin"
					if ! [ $? -eq 0 ] ; then
						mv "$chemin"_brute.jpg "$chemin"
						exit 1
					fi
					exiftool -Comment=vlcuser_compression -overwrite_original "$chemin" > ~/Desktop/exiftool.carbage ; rm ~/Desktop/exiftool.carbage
					rm "$chemin"_brute.jpg
				fi
			fi
		fi
	else
		$0 "$chemin"
	fi
done

exit