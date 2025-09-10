#!/bin/bash

# Configuration settings
INPUT_DIR="/path/inputs_prot"
CLASS_HMMS_DIR="/path/search_TPS/TPS/Tutorial/class-specific_hmms"
TABLE_FILE="/path/search_TPS/TPS/Tutorial/score_tables_dir/all.scores"
PFAMS_DIR="/path/search_TPS/TPS/Tutorial/PFAMs_dir"
OUTPUT_BASE="/path/outputs"
TPS_SCRIPT="/path/search_TPS/TPS/search_TPS.pl"

SEARCH_OPTION=1
CPU_CORES=5

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_BASE"

# Process each .faa file in input directory
for FASTA_FILE in "$INPUT_DIR"/*.faa; do
    FILENAME=$(basename "$FASTA_FILE" .faa)
    SAMPLE_OUTPUT="${OUTPUT_BASE}/${FILENAME}_output"

    echo "Starting analysis for: $FILENAME"

    # Run analysis with Perl script
    if "$TPS_SCRIPT"  -d "$CLASS_HMMS_DIR" \
                      -i "$FASTA_FILE" \
                      -t "$TABLE_FILE" \
                      -s "$SEARCH_OPTION" \
                      -p "$PFAMS_DIR" \
                      -o "$SAMPLE_OUTPUT" \
                      -cpu "$CPU_CORES"; then
        echo "Analysis completed successfully for $FILENAME"
    else
        echo "Analysis failed for $FILENAME"
    fi
done

echo -e "\n Processing finished. Results available in: $OUTPUT_BASE"