#!/bin/bash

#first thing: source ~/.bashrc
#this will activate the virtual myenv

source /path/for/plantismash/plantismash-1.0/myenv/bin/activate
#second thing: confirm it's reading the executables:
#which long-orfs
#which extract
#which build-icm
#which glimmer3
#which glimmerhmm

#optional: confirm py2 is available: find / -type f -name "python2.7" 2>/dev/null
#optional: check plantismash parameters: python run_antismash.py --help

# Input directories
fasta_dir="/path/fasta_genome"
gff3_dir="/path/gff3"

# Directory where antiSMASH results will be saved
output_dir="/path/output"

# Check if output directory exists, if not create it
mkdir -p "$output_dir"
#cd $fasta_dir
#pwd
# Loop through FASTA files in directory
for fasta_file in "$fasta_dir"/*.fasta; do
    # Extract base filename (without .fasta extension)
    base_name=$(basename "$fasta_file" .fasta)
    echo "$fasta_file"
    # Define path for corresponding GFF3 file
    gff3_file="$gff3_dir/$base_name.gff3"

    # Check if GFF3 file exists
    if [ -f "$gff3_file" ]; then
        echo "Processing $base_name ..."

        # Create a folder with base name inside output directory
        output_subdir="$output_dir/$base_name"
        mkdir -p "$output_subdir"

        # Run antiSMASH with FASTA file and corresponding GFF3 file
        python2 run_antismash.py --taxon plants --gff3 "$gff3_file" "$fasta_file" --limit -1 --outputfolder "$output_subdir" 
    else
        echo "Warning: Corresponding GFF3 file for $base_name not found."
    fi
done