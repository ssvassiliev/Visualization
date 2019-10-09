ffmpeg -i Grand.%04d.png -vcodec libx264 -crf 18 -s 1900x1200  -preset veryslow -filter:v "setpts=5.0*PTS"  movie.mp4
