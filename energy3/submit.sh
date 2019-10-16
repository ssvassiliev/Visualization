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

i=1
job=1

read -d '' slurm << EOF
#!/bin/bash
#SBATCH --account=def-svassili
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4000M
#SBATCH --time=12:0:0
EOF

part=$(($nframes/$ncpu))
remainder=$(($nframes % $ncpu))
while [ $(($i+$part+$remainder)) -le $nframes ]
  do
    echo i=$i job=$job
    echo "$slurm" > slurm
    echo pvbatch Flow.py $1 $(($i + $start - 1)) $(($i + $start + $part - 1)) >> slurm
    sbatch slurm
    echo "submitted job" $job: "frames" $(($i + $start - 1)) "to" $(($i + $start + $part - 1))
    job=$(($job+1))
    i=$(($i+$part))
  done
if [ $remainder -gt 0 ]; then
  echo "$slurm" > slurm
  echo pvbatch Flow.py $1 $(($i + $start - 1)) $(($i + $start + $remainder)) >> slurm
  sbatch slurm
  echo "submitted job" $job: "frames" $(($i + $start - 1)) "to" $(($i + $start + $remainder))
fi
rm slurm
