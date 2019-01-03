# canseq_pipeline
Written and maintained by Luka Culibrk at Canada's Michael Smith Genome Sciences Centre
Currently under construction
Pipeline for de novo assemblies for the CanSeq150 project

Stored here is the pipeline that is being used to assemble metazoan 10X Chromium genomes as part of the CanSeq150 project. 

## Getting Started
The assembly process uses a number of software which must be installed:

[Supernova](https://support.10xgenomics.com/de-novo-assembly/software/overview/latest/welcome) is used to perform initial de novo assembly.

[Tigmint](https://github.com/bcgsc/tigmint) is used to break the assembly in regions with low 10X molecule coverage spanning them

[ARCS](https://github.com/bcgsc/arcs) and [LINKS](https://github.com/bcgsc/LINKS) are used to scaffold after Tigmint. The intention is that the breaks introduced by Tigmint can now participate in scaffolding.

[Abyss-Sealer](https://github.com/bcgsc/abyss/tree/master/Sealer) is used to fill gaps in the assembly.

[BUSCO](https://busco.ezlab.org/) is used to assess completeness of genomes.

[Snakemake](https://snakemake.readthedocs.io/en/stable/) is used to run the pipeline.

The pipeline is given as a snakemake workflow that can be run easily using the shell scripts under pipeline/, specifically assemble.sh and sealthis.sh.

After installing the requisite software, you need to configure the workflow for your system. Specifically, you need to add the paths to the software used in the assembly in the following locations:

assemble.sh: 
* Line 61 should point to your installation of Snakemake and the Snakefile for the pipeline

Snakefile:
* Line 141 should point to the "reagent_seqs.txt" file, found in this repo under resources/, and the word "HISEQ" changed to the appropriate term in your FASTQ headers (dependant on the sequencing instrument you use)
