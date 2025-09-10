#!/bin/bash

#!/bin/bash

#export JAVA_HOME=$PWD/jdk-11.0.2
#export PATH=$JAVA_HOME/bin:$PATH

# Path to InterProScan (adjust if needed)
INTERPROSCAN_PATH="/data/execultaveis/interproscan/interproscan-5.74-105.0"

DIRETORIO_INPUT="/path/input/prot/"
DIRETORIO_CLEAN="/path/daisy/interpro/input_interpro"
DIRETORIO_OUTPUT="/data/daisy/interpro/out"

# Create output directory if it doesn't exist
mkdir -p "$CLEAN_DIR"
mkdir -p "$OUTPUT_DIR"

# Loop through .fasta files in input directory
for file in "$INPUT_DIR"/*.fasta; do
    # Base filename
    base=$(basename "$file")
    base_no_ext=$(basename "$file" .fasta)

    # Replace '*' with 'N' in sequences and save to new directory
    awk '/^>/ {print; next} {gsub(/\*/,"X"); print}' "$file" > "$CLEAN_DIR/$base"

    echo "Clean file generated: $CLEAN_DIR/$base"

    # Run InterProScan
    # Run InterProScan with the clean file
    "$INTERPROSCAN_PATH/interproscan.sh" \
        -i "$CLEAN_DIR/$base" \
        -f tsv \
        -b "$OUTPUT_DIR/${base_no_ext}_interpro" \
        -goterms \
        -iprlookup \
        -pa \
        -dp \
        -t p \
        --cpu 30 \
        -appl CDD,PANTHER,Pfam,PRINTS,SMART,SUPERFAMILY

    echo "Completed: ${base_no_ext}_interpro.tsv"
done

# -i: Specifies input file 
# -f: Defines output format
# -b: Defines output filename prefix
# -goterms: Include Gene Ontology terms in results
# -iprlookup: Performs additional search to include InterPro term information
# -pa: Generates a protein annotation report via kegg or reactome
# -dp: Enables predictive domain analysis