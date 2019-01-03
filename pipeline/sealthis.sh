#!/bin/bash
function usage()
{
    echo "Automatically generates bloom filters and runs Sealer for assemblies at k={90, 100 . . . 120}"
    echo ""
    echo "Usage:"
    echo "./sealthis.sh [MANDATORY] n_cores prefix in_fasta [OTHER_SMK_ARGS]"
    echo ""
    echo "MANDATORY Variables:"
    echo "n_cores = Number of cores to use. Factor of 16 (16 cores per bloom filter job)"
    echo "prefix = assembly prefix you used for assemble.sh"
    echo "in_fasta = path to FASTA. Matches the directory data/NAME"
    echo ""
    echo ""
    echo "OTHER_SMK_ARGS:"
    echo "Pass additional snakemake arguments here ie. -n for dryrun"
}

if [ "$1" == "" ]
then
    usage
    exit
fi

if [ ! -f data/$2/filtered_basic/basic.fq.gz ]
then
    echo "Error: No basic files found. Exiting"
    usage
    exit
fi
echo "/projects/lculibrk_prj/CGEN150/pipeline/sealthis.sh ${@:1}"
/home/lculibrk/miniconda3/bin/snakemake -s /projects/lculibrk_prj/CGEN150/pipeline/Snakefile_sealer -j$1 --config prefix=$2 fasta=$3 -p ${@:4}
