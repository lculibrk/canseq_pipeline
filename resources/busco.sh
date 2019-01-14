#!/bin/bash
#SBATCH -p all
#SBATCH -n 24
#SBATCH --mem=120G
#SBATCH --job-name=busco
#SBATCH -o %x.%j.log
#SBATCH -t 4-18:00:00
#SBATCH -N 1-1

source /projects/seqdev/CGEN150/Whitesided_Dolphin/BUSCO/busco-env.sh

seqfile=$1 # fasta format
shift
prefix=$1
shift
reference=$1 # path to file
shift
mode=$1 # geno, tran, or prot

# numbers cluster /tmp is 200G SSD
export TMPDIR=/tmp

threads=24

/home/shammond/src/busco/BUSCO.py -i $seqfile -o $prefix -l $reference -m $mode -c $threads -t $TMPDIR
