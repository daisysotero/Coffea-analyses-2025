#!/bin/bash

#install
#1. Create and activate Conda environment
#conda create -n kofamscan_env ruby=2.7 hmmer parallel -c bioconda -c conda-forge -y
#conda activate kofamscan_env
#2. Check dependencies
#ruby --version       # Should show Ruby >= 2.4
#hmmsearch -h         # HMMER should work
#parallel --version   # GNU Parallel should be available
#3. Install KofamScan
#git clone https://github.com/takaram/kofam_scan.git
#cd kofam_scan
#chmod +x exec_annotation
#4. Download KOfam database
#wget ftp://ftp.genome.jp/pub/db/kofam/profiles.tar.gz
#wget ftp://ftp.genome.jp/pub/db/kofam/ko_list.gz
#tar -xzf profiles.tar.gz
#gunzip ko_list.gz
#5. Create config.yml file
# config.yml
#profile: ./profiles
#ko_list: ./ko_list
#threshold: use

# Activate Conda environment
eval "$(conda shell.bash hook)"
conda activate kofamscan_env

# Directories
INPUT_DIR="/path//input"
KOFAMSCAN_DIR="/path/executable/kofamscan/kofam_scan"
OUTPUT_DIR="/path/out_kofam"

# Path to executable
EXEC="$KOFAMSCAN_DIR/exec_annotation/"

# Paths to profiles and lists (adjust if needed)
PROFILE="$KOFAMSCAN_DIR/profiles"
KO_LIST="$KOFAMSCAN_DIR/ko_list"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through input files (e.g. .faa)
for file in "$INPUT_DIR"/*.faa; do
    base=$(basename "$file" .faa)
    output_file="$OUTPUT_DIR/${base}_kofam.txt"
    
    perl "$EXEC" -o "$output_file" -f mapper-oneline -p "$PROFILE" -k "$KO_LIST" "$file"
    
    echo "Processed: $file → $output_file"
done
# --cpu=50 is in config.yml file
# Final message
echo "All files have been processed."