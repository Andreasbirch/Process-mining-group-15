#!/bin/sh

#BSUB -q hpc
#BSUB -J Cross_Validation
#BSUB -n 8
#BSUB -W 32:00
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -u s204708@dtu.dk
#BSUB -N
#BSUB -B
#BSUB -Ne

module load python3/3.8.11

cd /zhome/8c/a/156133/Iteration-2/Process-Discovery-Conformance
pwd | echo
source ../../procenv/bin/activate
pip install -r requirements.txt

python script.py