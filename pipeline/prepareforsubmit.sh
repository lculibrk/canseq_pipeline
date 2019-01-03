#!/bin/bash
function usage ()
{
echo "Converts scaffolded assembly to unitigs in a way that works nicely with the CGEN150 pipeline"
echo "Usage:" 
echo ""
echo "prepareforsubmit.sh /path/to/data/prefix in.fa"
}

if [ "$1" == "" ]
then
    usage
    exit
fi

#echo $1/submission
mkdir $1/submission;
ln -s --relative $2 $1/submission/scaffolds.fa;
cd $1/submission
mkdir initial/
cd initial/
ln -s --relative ../scaffolds.fa scaffolds.fa
/projects/lculibrk_prj/CGEN150/resources/abyss-fatoagp -f contigs.fa scaffolds.fa > scaffolds.agp


