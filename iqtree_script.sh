#!/bin/bash

# Activate Conda environment
eval "$(conda shell.bash hook)"
conda activate iqtree

# Array of input supermatrix files
arquivos=(
    "path/to/input/supermatrix/SUPERMATRIX.fasta"
)

# Base output directory
output_dir="path/to/output/RESULTS_iqtree"

# Fixed prefix for output files
prefix="RESULTS_iqtree"

# Create base output directory
mkdir -p "$output_dir"

# Process each input file
for arquivo in "${arquivos[@]}"; do

    echo "Processing: $arquivo"
    echo "Fixed prefix: $prefix"

    # IQ-TREE COMMAND
    # -s      : input sequence alignment file
    # -m TEST : automatic model selection (tests all available models)
    # -T 70   : use 70 CPU threads
    # -B 1000 : 1000 ultrafast bootstrap replicates
    # --alrt 1000 : 1000 SH-aLRT branch tests
    # --bnni  : optimize UFBoot trees by NNI on bootstrap alignments
    # --safe  : numerically stable likelihood calculations (avoids underflow errors)
    # -pre    : prefix for output files
    
    iqtree -s "$arquivo" \
        -m TEST \
        -T 70 \
        -B 1000 \
        --alrt 1000 \
        --bnni \
        --safe \
        -pre "$output_dir/$prefix"

done

# =============================================================================
# OPTION NOTES
# =============================================================================
# --safe : Makes likelihood calculations more numerically stable by preventing
#          errors caused by extremely small probabilities (underflow protection)
#
# --bnni : Optimize UFBoot trees by Nearest Neighbor Interchange on bootstrap alignments
#          For each bootstrap replicate:
#          1. Generates a bootstrap alignment
#          2. Builds a rapid initial tree
#          3. Applies NNI (small local branch swaps)
#          4. Increases tree likelihood
#          5. Uses optimized tree for support calculations
# =============================================================================