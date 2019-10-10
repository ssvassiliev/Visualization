#### Render animation frames on a SLURM cluster:

Make sure that **pvbatch** from Paraview version 5.7 is in your path.

Usage: ./submit.sh [Config] [First frame] [Last frame] [Number of jobs]

Example:
`./submit.sh Petit 0 200 10`


#### Encode a movie:

`ffmpeg -i Petit.%04d.png -vcodec libx264 -crf 18 -s 1900x1200 -preset veryslow -filter:v "setpts=5.0*PTS"  movie.mp4`

PTS is presentation timestamp, the time at which the frame ought to be shown. Increasing PTS will slowdown a movie.

#### Rotate a movie 90 degrees counterclockwise:

`ffmpeg -i input.mp4 -vf "transpose=2" output.mp4`
