#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate bigscape

INPUT_DIR="/path/input_bigscape"
OUTPUT_DIR="/path/out_bigscape"
PFAM="/path/pfam/Pfam-A.hmm"

#input_bigscape is the main directory (containing the plantismash results) 
#includes subdirectories for each species. 
#Inside each species subdirectory, there are multiple .gbk files—one .gbk file per identified cluster.

mkdir -p "$OUTPUT_DIR"

bigscape cluster \
  -i "$INPUT_DIR" \
  -o "$OUTPUT_DIR" \
  --mibig-version 4.0 \
  --pfam-path "$PFAM" \
  -v \
  --include-singletons \
  -c 6 

echo "✅ BiG-SCAPE finalizado. Veja o log em: $OUTPUT_DIR"