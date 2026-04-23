#!/bin/bash

# Activate Conda and BUSCO environment
eval "$(conda shell.bash hook)"
conda activate busco

# Input directory with protein FASTA files
input_dir="path/to/input_directory/"

# Output directory for BUSCO results
output_dir="path/to/output_directory/"

# Path to BUSCO lineage dataset
# Download from: https://busco-data.ezlab.org/v5/data/lineages/viridiplantae_odb10.2024-01-08.tar.gz
lineage="viridiplantae_odb12"

# Number of threads to use
threads=100

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Iterate over each FASTA file in the input directory
for fasta_file in "$input_dir"/*.fasta; do
    # Extract species name from filename (removes .fasta extension)
    species_name=$(basename "$fasta_file" .fasta)

    # Run BUSCO in protein mode
    # -m protein : protein mode
    # -c threads : number of threads
    # -f : force overwrite if exists
    echo "Processing: $species_name"
    busco -m protein -i "$fasta_file" -l "$lineage" -c "$threads" -o "$species_name" -f --out_path "$output_dir"
done

# Deactivate Conda environment
conda deactivate