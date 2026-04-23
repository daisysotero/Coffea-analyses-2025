## Repository structure

### Annotation and preprocessing
- `script_agat_allsteps.sh` → Performs gene model processing using AGAT, retaining longest isoforms in a GFF3 file and extracting corresponding CDS and protein sequences from the genome FASTA.
- `script_interpro.sh` → Protein domain annotation using InterProScan.
- `script_kofamscan.sh` → KEGG Orthology assignment using KofamScan.
- `script_tesorter.sh` → Transposable element detection and classification using TEsorter.

### Orthology analysis
- `script_orthofinder3.1.sh` → Orthogroup inference using OrthoFinder

### Biosynthetic gene clusters (BGCs)
- `script_plantismash.sh` → Detection of BGCs using plantiSMASH
- `script_bigscape.sh` → Clustering and networking of BGCs using BiG-SCAPE
- `script_clinker.sh` → Visualization of gene cluster similarity

### Phylogeny
- `busco_script_prot.sh` → BUSCO analysis on protein sequences.
- `busco_phylogenomics.sh` → Phylogenomic dataset construction using BUSCO single-copy orthologs.
- `iqtree_script.sh` → Phylogenetic inference using IQ-TREE.
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

