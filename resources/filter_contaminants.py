## Import necessary modules
import os
import sys
import re
from Bio import SeqIO
from Bio.Seq import MutableSeq
from Bio.Alphabet import generic_dna

## Argument parsing
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("Contamination.txt", help="The contamination file provided by NCBI")
parser.add_argument("in.fa", help="The SCAFFOLDS fasta file")
parser.add_argument("in.agp", help="The AGP generated from the scaffolds fasta")
parser.add_argument("out", help="Name of output FASTAs without extension - think of this like a base name")
parser.add_argument("out_dir/", help="Name of directory where outputs will be made")
parser.parse_args()

## Read file
with open(sys.argv[1]) as f:
    contamination = f.readlines()
## Strip special characters (notably line breaks)
contamination=[line.strip() for line in contamination]

## Get fasta
fasta_dict = SeqIO.to_dict(SeqIO.parse(sys.argv[2], "fasta"))

## Get AGP
with open(sys.argv[3]) as agp:
    agpfile = agp.readlines()
AGP=[line.strip().split("\t") for line in agpfile]
AGP={t[5]:t for t in AGP}

print(AGP.keys())


## Get sequences
trim=[]
duplicated=[]
exclude=[]
record_trim = False
record_dup = False
record_exclude = False
for element in contamination:
    ## Detect the "Trim:" block
    if element == "Trim:":
        record_trim = True
        continue
    ## Detect the "Duplicated:" block
    if element == "Duplicated:":
        record_dup = True
        continue
    if element == "Exclude:":
        record_exclude = True
        continue
    ## If we're at the "Trim:" block
    if record_trim:
        ## Detect if blank line (line after last entry) and turn off recording
        if len(element) == 0:
            record_trim = False
            continue
        ## Skip the "sequence name... etc line
        if re.match("Sequence name", element) is not None:
            continue
        trim.append(element)
    ## If we're at the "duplicated" block
    if record_dup:
        ## Detect if blank line (line after last entry) and turn off recording
        if len(element) == 0:
            record_dup = False
            continue
        ## Skip the "sequence name... etc line
        if re.match("Sequence name", element) is not None:
            continue
        duplicated.append(element)
    ## If we're at the "Exclude:" block
    if record_exclude:
        if len(element) == 0:
            record_exclude = False
            continue
        if re.match("Sequence name", element) is not None:
            continue
        exclude.append(element)


for element in trim:
    # Split by tab-delimination
    split = element.split("\t")
    contig = split[0]
    # Grab the contig
    scaffold = AGP[contig][0]
    # Grab the corresponding scaffold
    scaffoldnumeric = re.sub("\D", "", scaffold)
    coordinates=split[2].split("..")
    coordinates[0] = int(coordinates[0]) - 1 + int(AGP[contig][1]) - 1
    coordinates[1] = int(coordinates[1]) - 1 + int(AGP[contig][1]) - 1
    #coordinates = [(int(coord) + int(AGP[contig][1]) - 2) for coord in coordinates]
    #print(coordinates)
    #print(fasta_dict[scaffoldnumeric])
    #print(type(fasta_dict[scaffoldnumeric].seq))
    seq = fasta_dict[scaffoldnumeric].seq.tomutable()
    tomut = seq[coordinates[0]:coordinates[1]]
    lengthN = len(tomut)
    seq[coordinates[0]:coordinates[1]] = "N" * lengthN
    fasta_dict[scaffoldnumeric].seq = seq.toseq()


#for element in duplicated:
#    torm = element.split(" ")[0].split("|")[1]
#    del(fasta_dict[torm])
    #print(element)
    #print(element.split(" ")[1].split("|")[1])
    #print(fasta_dict[element.split(" ")[0].split("|")[1]])
    #print(fasta_dict[element.split(" ")[1].split("|")[1]])
mito={}
for element in exclude:
    split = element.split("\t")
    #print(split)
    if split[2].split("-")[0] == "mitochondrion":
        contig = split[0]
        scaffold = AGP[contig][0]
        scaffoldnumeric = re.sub("\D", "", scaffold)
        fasta_dict[scaffoldnumeric].description = "[location=mitochondrion]"
        mito[scaffoldnumeric] = fasta_dict[scaffoldnumeric]
        del(fasta_dict[scaffoldnumeric])

#SeqIO.write([fasta_dict, mito], "example.fasta", "fasta-2line")
with open(os.path.join(sys.argv[5], sys.argv[4] + ".fa"), 'w') as handle:
    SeqIO.write(fasta_dict.values(), handle, 'fasta-2line')

with open(os.path.join(sys.argv[5], sys.argv[4] + ".fa"), 'a') as handle:
    SeqIO.write(mito.values(), handle, 'fasta-2line')

os.system("/projects/lculibrk_prj/CGEN150/resources/abyss-fatoagp -f " + os.path.join(sys.argv[5], sys.argv[4] + "_contigs.fa") + " " + os.path.join(sys.argv[5], sys.argv[4] + ".fa") + " > " + os.path.join(sys.argv[5], sys.argv[4] + "_contigs.agp"))


# Open the new AGP file
with open(os.path.join(sys.argv[5], sys.argv[4] + "_contigs.agp")) as f:
    newagp = f.readlines()
AGP=[element.strip().split('\t') for element in newagp]

## Split the AGP into mito and non-mito
if(len(mito) > 0):
    mitoAGP = AGP[-len(mito):]
else:
    mitoAGP = []
print(mitoAGP)
AGP = AGP[0:(len(AGP) - len(mito))]

## Rename mitoAGP contig names and scaffold names
mitotigs=[]
for mito_tig in range(len(mito)):
    mitotigs.append(mitoAGP[mito_tig][5])
    mitoAGP[mito_tig][0] = mitoAGP[mito_tig][0] + "_MT"
    #mitoAGP[mito_tig][5] = mitoAGP[mito_tig][5] + " [location=mitochondrion]"

## Save mitoAGP and mito to files

with open(os.path.join(sys.argv[5], sys.argv[4] + "_contigs.agp"), 'w') as file:
    file.writelines('\t'.join(i) + '\n' for i in AGP)

with open(os.path.join(sys.argv[5], sys.argv[4] + "_contigs_MITO.agp"), 'w') as file:
    file.writelines('\t'.join(i) + '\n' for i in mitoAGP)


## Rename mito contigs in the fasta file
fasta_dict = SeqIO.to_dict(SeqIO.parse(os.path.join(sys.argv[5], sys.argv[4] + "_contigs.fa"), "fasta"))

for mito_tig in mitotigs:
    fasta_dict[mito_tig].description = "[location=mitochondrion]"

with open(os.path.join(sys.argv[5], sys.argv[4] + "_contigs.fa"), 'w') as handle:
    SeqIO.write(fasta_dict.values(), handle, 'fasta-2line')


