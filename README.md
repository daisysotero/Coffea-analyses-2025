## Repository structure

### Annotation and preprocessing
- `script_agat_allsteps.sh` → Script for generating a GFF3 file with the longest isoforms using AGAT, as well as extracting the corresponding CDS and protein sequences by combining the processed annotation (longest GFF3) with the genome FASTA file.
- `script_interpro.sh` → Performs protein functional annotation by identifying conserved domains and signatures using InterProScan.
- `script_tesorter.sh` → Detects and classifies transposable elements in sequences using TEsorter.
- - `script_kofamscan.sh` → Script for obtaining KEGG Orthology (KO) assignments using KofamScan.

### Orthology analysis
- `script_orthofinder3.1.sh` → Performs orthogroup inference across species using OrthoFinder v3.1.

### Biosynthetic gene clusters (BGCs)
- `script_plantismash.sh` → Identifies biosynthetic gene clusters (BGCs) using plantiSMASH.
- `script_bigscape.sh` → Clusters and constructs similarity networks of BGCs using BiG-SCAPE.
- `script_clinker.sh` → Generates visualizations of synteny and similarity between gene clusters.

### Phylogeny
- `busco_script_prot.sh` → Runs BUSCO on protein sequences to assess genome completeness.
- `busco_phylogenomics.sh` → Builds a phylogenomic dataset based on BUSCO single-copy orthologs.
- `iqtree_script.sh` → Performs phylogenetic tree inference using IQ-TREE.
- `RESULTS_iqtree.treefile` → Final IQ-TREE phylogenetic tree.

#### R scripts
- `GO_enrichment_phyper.R` → GO enrichment analysis using hypergeometric test

#### Python scripts
- `plot_GO_enrichment_phyper.py` → Visualization of GO enrichment results
- `barplot_orthogroups.py` → Barplots of orthogroup distribution
- `barplot_platismash.py` → Visualization of BGC statistics
- `box_cluster_size.py` → Boxplot of BGC cluster sizes
- `box_top20_families.py` → Visualization of top gene families


### How to run the workflow

To run the scripts, you can:
- Clone this GitHub repository in a Linux environment:

```bash
git clone https://github.com/daisysotero/Coffea-analyses-2025.git

or download the repository as individual files directly from GitHub
or copy each script manually and save it as a .sh file using a text editor (e.g., Notepad++, VS Code).

Once the scripts are saved locally, navigate to the directory containing them and (optionally but recommended) give execution permission:

chmod +x *.sh
chmod +x *.py

Then run the scripts using:
bash script_name.sh
python script_name.py

