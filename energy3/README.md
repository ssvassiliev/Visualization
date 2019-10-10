#### Submit jobs on Graham:

./submit.sh Petit 0 200 10


#### Make movie:

ffmpeg -i Petit.%04d.png -vcodec libx264 -crf 18 -s 1900x1200  -preset veryslow -filter:v "setpts=5.0*PTS"  movie.mp4

#### Rotate movie 90 degrees counterclockwise:

ffmpeg -i Petit_Passage_5x.mp4 -vf "transpose=2" Petit_Passage_5x_rot.mp4
