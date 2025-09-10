#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate clinker

base_dir="./gbks_familia_para_clinker"
# base_dir contains subdirectories for each gene cluster family as defined by BiG-SCAPE.  
# Inside each subdirectory are the corresponding .gbk files for that family,  
# which were obtained from antiSMASH (via plantiSMASH).

output_dir="./out_clinker"
mkdir -p "$output_dir"

# Loop 
for family_dir in "$base_dir"/*/; do
    
    family_name=$(basename "$family_dir")
    
    echo "🔍 Rodando Clinker para: $family_name"

    
    clinker "$family_dir"/*.gbk -p "$output_dir/mapa_${family_name}.html"
done