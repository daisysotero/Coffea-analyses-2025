#!/bin/bash 

# Activate Conda and environment
eval "$(conda shell.bash hook)"
conda activate agat

# folder inputs and outputs
FASTA_DIR="/path/for/genome" 
GFF3_DIR="/path/for/gff3"
OUTPUT_GFF3_FIL="/path/for/output_gff3_longest"
OUTPUT_CDS="/path/for/output_cds_longest"
OUTPUT_PROT="/path/for/output_protein_longest"


# Create species list based on FASTA filenames
# 1. `ls "$FASTA_DIR"/*.fasta` -> Lists all FASTA files in the directory.
# 2. `xargs -n 1 basename` -> Gets just the filenames (without path).
# 3. `sed 's/.fasta//'` -> Removes the `.fasta` extension from names.
species=($(ls "$FASTA_DIR"/*.fasta | xargs -n 1 basename | sed 's/.fasta//'))

# Temporary directory for modifications
TEMP_DIR=$(mktemp -d)

# Loop to process each listed species
for sp in "${species[@]}"; do
    echo "🔹 Processing: $sp"  # Shows message indicating the start of species processing.

    # Define full paths of input files for current species
    FASTA_FILE="${FASTA_DIR}/${sp}.fasta"  # Species FASTA file
    GFF3_FILE="${GFF3_DIR}/${sp}.gff3"     # Corresponding GFF3 file

    # Check if required files exist before proceeding
    if [[ -f "$FASTA_FILE" && -f "$GFF3_FILE" ]]; then

        ###########################################################
        # If file doesn't have "protein_match", skip Steps 1, 2, 3
        ###########################################################
        if ! grep -q "protein_match" "$GFF3_FILE"; then
            echo "File $GFF3_FILE doesn't have 'protein_match', skipping Steps 1, 2 and 3."
            FINAL_GFF="$GFF3_FILE"  # Uses original GFF3 for Step 4
        ###############################################################
        ###############################################################

        else

            # Step 1: Remove lines containing "protein_match"
            NO_PROTEIN_GFF="${TEMP_DIR}/${sp}_noProtein_match.gff3"
            echo "Execut: No_protein_match --gff \"$GFF3_FILE\" -o \"$NO_PROTEIN_GFF\"" | tee -a output.txt
            awk '$3 != "protein_match"' "$GFF3_FILE" > "$NO_PROTEIN_GFF"
            
            # Step 2: Generate GFF3 with locus_tag
            LOCUS_TAG_GFF="${TEMP_DIR}/${sp}_locus_tag.gff3"
            echo "Execut: locus_tag --gff \"$NO_PROTEIN_GFF\" -o \"$LOCUS_TAG_GFF\"" | tee -a output.txt
            agat_sq_manage_attributes.pl --gff "$NO_PROTEIN_GFF" --att Parent/locus_tag --cp -o "$LOCUS_TAG_GFF"
            
            # Step 3: Adjust locus_tag format
            FINAL_GFF="${TEMP_DIR}/${sp}_final_agat.gff3"
            echo "Execut: locus_tag_sed --gff \"$LOCUS_TAG_GFF\" -o \"$FINAL_GFF\"" | tee -a output.txt
            sed -n 's/\(.*;locus_tag=\)\([^\.]*\)\..*/\1\2/p' "$LOCUS_TAG_GFF" > "$FINAL_GFF"
            
        fi
        ###############################################################
        ####### if the gff3 is already formatted this isn't needed #######
        ###############################################################

        # Filter GFF3 to keep only the longest isoform
        # The `agat_sp_keep_longest_isoform.pl` script generates a new filtered file.
        FIL_GFF="${OUTPUT_GFF3_FIL}/${sp}_longest.gff"
        echo "Executing: agat_sp_keep_longest_isoform.pl --gff \"$FINAL_GFF\" -o \"$FIL_GFF\"" | tee -a output.txt
        agat_sp_keep_longest_isoform.pl --gff "$FINAL_GFF" -o "$FIL_GFF"
    
        # Extract CDS sequences (Coding DNA Sequence)
        # The `agat_sp_extract_sequences.pl` script generates a FASTA file with coding sequences.
        CDS_FILE="${OUTPUT_CDS}/${sp}_cds.fasta"
        echo "Executing: agat_sp_extract_sequences.pl --gff \"$FIL_GFF\" --fasta \"$FASTA_FILE\" -o \"$CDS_FILE\"" | tee -a output.txt
        agat_sp_extract_sequences.pl --gff "$FIL_GFF" --fasta "$FASTA_FILE" -o "$CDS_FILE"


        # Extract protein sequences
        # The `-p` parameter indicates the output will be protein FASTA instead of DNA.
        PROT_FILE="${OUTPUT_PROT}/${sp}_prot.fasta"
        echo "Executing: agat_sp_extract_sequences.pl --gff \"$FIL_GFF\" --fasta \"$FASTA_FILE\" -p -o \"$PROT_FILE\"" | tee -a output.txt
        agat_sp_extract_sequences.pl --gff "$FIL_GFF" --fasta "$FASTA_FILE" -p -o "$PROT_FILE"

        echo "Completed: $sp"  # Indicates the species was processed successfully.
    else
        echo "Missing files for $sp, skipping..."  # Warning message if files are missing.
    fi
done 

# Move index files to temporary directory
mv "${FASTA_DIR}"/*.index* "${TEMP_DIR}/"

# Clean up temporary directory
rm -r "$TEMP_DIR"

conda deactivate

echo "Processing completed!"