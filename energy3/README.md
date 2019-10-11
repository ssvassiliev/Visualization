#### Render animation frames on a SLURM cluster:

Make sure that **pvbatch** from Paraview version 5.7 is in your path.

Usage: ./submit.sh [Config] [First frame] [Last frame] [Number of jobs]

Example:
`./submit.sh Petit 0 200 10`


#### Encode a movie:

FFMPEG usually efficiently uses up to 6-8 CPUS. As this process is fairly fast it can be run in interactive mode:

`[svassili@gra-login3 frames]$ salloc -c 6 --account=def-svassili --mem-per-cpu=4000M --time=1:0:0`
`salloc: Pending job allocation 20478277`
`salloc: job 20478277 queued and waiting for resources`
`salloc: job 20478277 has been allocated resources`
`salloc: Granted job allocation 20478277`
`salloc: Waiting for resource configuration`
`salloc: Nodes gra313 are ready for job`

`[svassili@gra313 frames]$ ffmpeg -i Petit.%04d.png -vcodec libx264 -crf 18 -s 1900x1200 -preset veryslow -filter:v "setpts=5.0*PTS"  movie.mp4`

PTS is presentation timestamp, the time at which the frame ought to be shown. Increasing PTS will slowdown a movie.

#### Rotate a movie 90 degrees counterclockwise:

`ffmpeg -i input.mp4 -vf "transpose=2" output.mp4`
