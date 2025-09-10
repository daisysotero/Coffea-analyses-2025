import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load enrichment results
df = pd.read_excel("result_phyper_subg_canephora.xlsx")

# Add useful columns
df['-log10(FDR)'] = -np.log10(df['fdr'])
df['GO_label'] = df['GO_name'] + ' (' + df['GO'] + ')'

# Sort by FDR and select top 35 terms
df_sorted = df.sort_values('fdr').head(35)

# Prepare data for plotting
x = df_sorted['-log10(FDR)']
y = df_sorted['GO_label']
colors = df_sorted['-log10(FDR)']
sizes = -np.log10(df_sorted['pvalue'])
sizes_scaled = sizes * 15

# Plot dotplot
plt.figure(figsize=(10, 7))
sc = plt.scatter(x=x, y=y, c=colors, s=sizes_scaled, cmap='viridis', alpha=0.8, edgecolor='k')

# Colorbar for FDR values
cbar = plt.colorbar(sc)
cbar.set_label('-log10(FDR)', fontsize=12)

# Manual size legend for p-value
for size in [2, 4, 6]:
    plt.scatter([], [], c='k', alpha=0.5, s=size*50, label=f'{size:.0f}')

plt.legend(scatterpoints=1, frameon=False, labelspacing=1,
           title='-log10(pvalue)', loc='lower right', bbox_to_anchor=(0.9, 0.05),
           borderaxespad=0)

# Titles and axis formatting
plt.title('GO enrichment - C. canephora subgenomes', fontsize=10)
plt.xlabel('-log10(FDR)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=11)
plt.gca().invert_yaxis()
plt.tight_layout()

# Save figure at high resolution
plt.savefig('dotplot_sub_canephora.png', dpi=800)
# plt.show()