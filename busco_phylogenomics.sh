#!/bin/bash

# Activate Conda and BUSCO_phylogenomics environment
conda activate BUSCO_phylogenomics

# =============================================================================
# GENERIC COMMAND TEMPLATE
# =============================================================================
# python path/to/BUSCO_phylogenomics.py \
#        -i path/to/busco_results \ #input is busco results
#        --nt \                    # Use for nucleotide BUSCO results (remove for protein mode - default)
#        -o path/to/output_busco_phylogenomics \  # Provide path - script creates directory (do NOT create beforehand)
#        -t 5 \                    # Number of threads
#        -psc 80                   # Percentage of species required for single-copy orthologs
# =============================================================================


# =============================================================================
# EXAMPLE: Protein Mode
# =============================================================================
# Run BUSCO_phylogenomics on protein data
# - No --nt flag (protein mode is default)
# - Runs in background with nohup
# - Redirects output to busco-phylo_prot.log

nohup python path/to/BUSCO_phylogenomics.py \
       -i path/to/input/RESULTS_busco/ \
       -o path/to/OUTPUT_busco-phylo/ \
       -t 5 \
       -psc 85 \
       > busco-phylo_prot.log 2>&1 &

# =============================================================================
# USAGE NOTES
# =============================================================================
# Parameters:
#   -i   : Input directory with BUSCO results
#   --nt : Nucleotide mode (remove for protein mode)
#   -o   : Output directory (script creates it - DO NOT pre-create)
#   -t   : Number of CPU threads
#   -psc : Percentage of species cutoff for single-copy orthologs (e.g., 85 = 85%)
#
