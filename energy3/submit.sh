#!/bin/bash

echo "Usage: ./submit config_file first_frame last_frame njobs"
echo "Example: ./submit Petit 0 238 50"

if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    exit
fi

start=$2
end=$3
nframes=$(($end-$start))
ncpu=$4

i=0
job=1

read -d '' slurm << EOF
#SBATCH --account=def-svassili
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4000M
#SBATCH --time=3:0:0
EOF

part=$(($nframes/$ncpu))
remainder=$(($nframes % $ncpu))
while [ $(($i+$part)) -le $nframes ]
do
  echo "$slurm" > slurm
  echo pvbatch Flow.py $1 $(($i+$start)), $(($i + $start + $part - 1)) >> slurm
  echo sqsub slurm
  echo "submitted job" $job:
  cat slurm
  job=$(($job+1))
  i=$(($i+$part))
done
echo "$slurm" > slurm
echo pvbatch Flow.py $1 $(($i + $start)) $(($i + $start+ $remainder)) >> slurm
  echo sqsub slurm
echo "submitted job" $job:
cat slurm
job=$(($job+1))
rm slurm
