#!/bin/bash

#INSTALLATION: install hmmer - conda install -c bioconda hmmer
#            Install TEsorter from github
#            If database doesn't have h3f, h3m, h3i, h3p files, you need to generate them:
#               for file in *.hmm; do hmmpress "$file"; done -> this will generate files in the database

# Directories
INPUT_DIR="/path/input_fasta_protein_or_cds"
OUTPUT_DIR="/path/output_fasta_protein_or_cds"
DB_PATH="/path/REXdb_protein_database_viridiplantae_v4.0.hmm"
TEMP_DIR='/path/Files_temporarios'

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Number of processors (adjust as needed)
THREADS=5

# Press the HMM database (only once)
echo "Pressing HMM database..."
hmmpress "$DB_PATH"

# Loop to process each fasta file
for fasta_file in "$INPUT_DIR"/*.fasta; do
    # Get filename without extension
    base_name=$(basename "$fasta_file" .fasta)
    
    # Create subdirectory for the species
    species_out="$OUTPUT_DIR/$base_name"
    mkdir -p "$species_out"

    echo "Running TEsorter for: $base_name"
    
    # TEsorter command - protein = -st prot | cds = -st nucl 
    TEsorter "$fasta_file" \
    -st prot \
    --db-hmm "$DB_PATH" \
    -p "$THREADS" \
    -tmp "$TEMP_DIR" \
    -cov 50 \
    -prob 0.8 \
    -pre "$species_out/${base_name}_TEsorter"

    echo "Completed: $base_name"
done