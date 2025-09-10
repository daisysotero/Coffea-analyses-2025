library(dplyr)
library(tidyr)
library(readxl)
library(GO.db)
library(writexl)

# genes_universo: complete list of all genes in the study,
# regardless of whether they have GO annotation or not.
# This serves as the background for the statistical test.

# anotacoes: list of genes from the universe that have at least one GO annotation —
# i.e., a subset of the universe genes with associated GO terms.

# Genes of interest: the gene list you want to test for enrichment.

# -----------------------------------------------------------
# 1. Input data
# -----------------------------------------------------------
anotacoes <- read_excel("anotacoes_so_go.xlsx")
# Convert to standard data.frame (optional)
anotacoes <- as.data.frame(anotacoes, stringsAsFactors = FALSE)

# Split multiple GO terms separated by ";" into separate rows
anotacoes_expandida <- anotacoes %>%
  separate_rows(GO, sep = ";") %>%
  filter(GO != "", !is.na(GO))  # Remove rows with empty or NA GO terms

# -----------------------------------------------------------
# 2. Gene sets
# -----------------------------------------------------------
# Gene universe: all genes in the experiment (with or without GO)
genes_universo_df <- read_excel("gene_universo.xlsx")
genes_universo <- as.character(genes_universo_df$Query_ID)  # Extract gene IDs as character vector
# Total size of the gene universe
length(genes_universo)
length(unique(genes_universo))
total_genes <- length(unique(genes_universo))

# Genes of interest: genes to test for enrichment
# genes_interesse_df <- read_excel("genes_og_canephora.xlsx")
# genes_interesse_df <- read_excel("genes_og_subg_canephora.xlsx")
# genes_interesse_df <- read_excel("genes_og_eugenoides.xlsx")
genes_interesse_df <- read_excel("genes_og_subg_eugenoides.xlsx")
genes_interesse_df
genes_interesse <- as.character(genes_interesse_df$Genes)  # Extract genes of interest as character vector
length(genes_interesse)

genes_interseccao <- intersect(genes_interesse, genes_universo)
length(genes_interseccao)

# Number of genes of interest
k <- length(genes_interesse)

# -----------------------------------------------------------
# 3. (Optional) Check GO coverage in the gene universe
# -----------------------------------------------------------
# Proportion of universe genes with at least one GO annotation
length(unique(anotacoes_expandida$GeneID)) / length(genes_universo)

# -----------------------------------------------------------
# 4. GO enrichment analysis (hypergeometric test)
# -----------------------------------------------------------
go_counts <- anotacoes_expandida %>%
  filter(GeneID %in% genes_universo) %>%  # Keep only genes present in the universe
  group_by(GO) %>%
  summarise(
    m = n_distinct(GeneID),               # Number of universe genes annotated with the GO term
    q = sum(GeneID %in% genes_interesse) # Number of genes of interest annotated with the GO term
  ) %>%
  mutate(
    n = total_genes - m,                  # Number of universe genes NOT annotated with the GO term
    k = k,                               # Total number of genes of interest
    pvalue = phyper(q - 1, m, n, k, lower.tail = FALSE), # Hypergeometric p-value for enrichment (≥ q)
    M = m + n                            # Total number of genes in universe (redundant)
  ) %>%
  ungroup() %>%
  mutate(
    fdr = p.adjust(pvalue, method = "BH"),  # Multiple testing correction using Benjamini-Hochberg (FDR)
    GO_name = Term(GO)                        # Retrieve GO term descriptions (using GO.db package)
  ) %>%
  filter(fdr < 0.05) %>%                      # Retain only significantly enriched GO terms (FDR < 0.05)
  arrange(fdr)                                # Sort by ascending FDR (most significant first)

print(go_counts)

# Export results to Excel
# write_xlsx(go_counts, "result_phyper_canephora.xlsx")
# write_xlsx(go_counts, "result_phyper_subg_canephora.xlsx")
# write_xlsx(go_counts, "result_phyper_eugenioides.xlsx")
write_xlsx(go_counts, "result_phyper_subg_eugenioides.xlsx")



# Explanation of variables:
# q: number of genes of interest annotated with the GO term
# m: number of universe genes annotated with the GO term
# n: number of universe genes NOT annotated with the GO term
# k: total number of genes of interest
# M = m + n: total number of genes in the universe
