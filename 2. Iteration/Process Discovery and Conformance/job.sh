
#!/bin/sh

#BSUB -q hpc
#BSUB -J Cross_Validation
#BSUB -n 4
#BSUB -W 24:00
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -M 4GB
#BSUB -u s204708@dtu.dk
#BSUB -N
#BSUB -B
#BSUB -Ne

module load python/3.8.5

python script.py
