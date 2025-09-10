#!/bin/bash

# Activate Conda and the desired environment
eval "$(conda shell.bash hook)"
#conda activate orthofinder-env
#conda activate ortho_cafe
conda activate orthofinder3.1_env

# Define input directory
INPUT_DIR="/folder/with/proteins.fasta/of/the/species"

# Run OrthoFinder with 5 threads and 5 CPU cores using Diamond ultra-sensitive mode
orthofinder -t 5 -a 5 -S diamond_ultra_sens -f "$INPUT_DIR"

# Completion message
echo "OrthoFinder finished successfully!"
