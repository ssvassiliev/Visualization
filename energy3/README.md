#### Render animation frames on a SLURM cluster:

Make sure that **pvbatch** from Paraview version 5.7 is in your path.
You can use /home/razoumov/paraviewcpu/bin

Usage: ./submit.sh [Config] [First frame] [Last frame] [Number of jobs]

Example:
`./submit.sh Petit 0 200 10`


#### Encode a movie:

FFMPEG efficiently uses up to 6-8 CPUS. As this process is fairly fast it can be run in interactive mode.

The frame names are in format:  `x.xxxx.png` where the first number is the batch (job) number and the second number is the frame number. The frames of all jobs are numbered consecutively starting from 0000.

Allocate 6 CPUS:
`$ salloc -c 6 --account=def-svassili --mem-per-cpu=4000M --time=1:0:0`

Run ffmpeg to encode a movie:
`ls | sort -n | xargs cat | ffmpeg -f image2pipe  -vcodec png -i - -vcodec libx264 -pix_fmt yuv420p -crf 18 -s 1900x1200 -preset veryslow -filter:v "setpts=2.0*PTS" movie.mp4`

Make sure that the working directory containds only frames. We cannot use `ls *.png`, it hangs on directories with thousands of files.

PTS is presentation timestamp, the time at which the frame ought to be shown. Increasing PTS will slowdown a movie.

The pixel format option is for compatibility with QT player on MacOS

#### Rotate a movie 90 degrees counterclockwise:

`ffmpeg -i input.mp4 -vf "transpose=2" output.mp4`
