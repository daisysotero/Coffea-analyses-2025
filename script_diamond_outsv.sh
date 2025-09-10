#!/bin/bash


DIRETORIO_INPUT="/path/input_protein"
DIRETORIO_DB="/path/databases/uniref90/uniref90_makedbdiamond"
DIRETORIO_OUTPUT="/path/output"

BANCO="$DIRETORIO_DB/uniref90"

# Header for the output file
CABECALHO="qseqid\tsseqid\tqlen\tslen\tstitle\tlength\tpident\tmismatch\tgaps\tppos\tevalue\tscore"

mkdir -p "$DIRETORIO_OUTPUT"

# Loop
for arquivo in "$DIRETORIO_INPUT"/*.fasta; do
    
    base=$(basename "$arquivo" .fasta)

   
    output="$DIRETORIO_OUTPUT/${base}_blastp_diamond.tsv" #or _blastp_diamond.xml

    /data/execultaveis/diamond blastp \
        -d "$BANCO" \
        -q "$arquivo" \
        -o "$output" \
        -f 6 qseqid sseqid qlen slen stitle length pident mismatch gaps ppos evalue score \
        --max-target-seqs 1 \
        --evalue 1e-5 \
        --threads 50 \
        --sensitive \
        --unal 1

    
    sed -i "1i$CABECALHO" "$output"

    echo "Processado: $arquivo -> $output"
done