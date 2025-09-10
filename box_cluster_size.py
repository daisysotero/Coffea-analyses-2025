import os
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

import pandas as pd
import glob
import os

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import matplotlib as mpl
from __future__ import unicode_literals
from matplotlib.gridspec import GridSpec
#matplotlib.rcParams['text.usetex'] = True
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import AutoMinorLocator
from scipy.signal import find_peaks
import matplotlib.patches as patches
from statistics import mean, stdev
from math import sqrt
from scipy.stats import f_oneway
from scipy.stats import tukey_hsd
from scipy import stats
import matplotlib
import matplotlib.cm as cm
import matplotlib as mpl
from __future__ import unicode_literals
from matplotlib.gridspec import GridSpec
matplotlib.rcParams['text.usetex'] = True
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import AutoMinorLocator
import matplotlib.gridspec as gridspec

from scipy.stats import f_oneway
from scipy.stats import tukey_hsd
from scipy import stats
from statistics import mean, stdev
import statsmodels.api as sm
from math import sqrt

style = {'alpha': 0.75}
gridstyle = {'linewidth': 0.5, 'alpha': 0.5}
#plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx}')
plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica-Normal']})

# Base directory of gbk files
base_dir = "/path/input_bigscape"

# List to store extracted data
data = []

for species in os.listdir(base_dir):
    species_dir = os.path.join(base_dir, species)
    if os.path.isdir(species_dir):
        for filename in os.listdir(species_dir):
            if filename.endswith(".gbk"):
                filepath = os.path.join(species_dir, filename)
                with open(filepath, 'r') as f:
                    content = f.read()

                # Extract cluster size (LOCUS line)
                locus_match = re.search(r'^LOCUS\s+\S+\s+(\d+)\s+bp', content, re.MULTILINE)
                size = int(locus_match.group(1)) if locus_match else None

                # Extract cluster type (/product="...")
                product_match = re.search(r'/product="([^"]+)"', content)
                cluster_type = product_match.group(1).lower() if product_match else "unknown"

                # Add data if size exists
                if size is not None:
                    data.append({
                        'Species': species,
                        'Cluster_Size_bp': size,
                        'Cluster_Type': cluster_type,
                        'Cluster_Name': filename.replace('.gbk', '')
                    })

# Create DataFrame
df = pd.DataFrame(data)
df

# Dictionary of cluster type colors
color_map = {
    "alkaloid": "#FF1F20",  
    "lignan": "#4D91FF",  
    "polyketide": "#5CE657",  
    "saccharide": "#B957C8",  
    "putative": "#FF9900",  
    "terpene": "#FFFF66",  
    "lignan-alkaloid": "#003333",  
    "lignan-polyketide": "#004D4D",  
    "lignan-saccharide": "#006666",  
    "lignan-saccharide-terpene": "#008080",  
    "lignan-terpene": "#339999",  
    "saccharide-alkaloid": "#66B2B2",  
    "saccharide-polyketide": "#99CCCC",  
    "saccharide-terpene": "#BFE5E5",  
    "terpene-alkaloid": "#E5F5F5",  
    "polyketide-alkaloid": "#F5FFFF"
}

# Custom order list
type_cluster_order = [
    "alkaloid",  
    "lignan",  
    "polyketide",  
    "saccharide",  
    "putative",  
    "terpene",  
    "lignan-polyketide",  
    "lignan-saccharide",  
    "lignan-saccharide-terpene",  
    "lignan-terpene",  
    "saccharide-alkaloid",  
    "saccharide-polyketide",  
    "saccharide-terpene",  
    "terpene-alkaloid",  
    "polyketide-alkaloid"
]

# Set column as categorical with fixed order
df['Cluster_Type'] = pd.Categorical(df['Cluster_Type'], categories=order, ordered=True)

df

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create figure with two vertical panels
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 6), sharey=True)

# -------- PANEL A: By species --------
ax1 = axes[0]

sns.violinplot(
    x='Species',
    y='Cluster_Size_Mb',
    data=df,
    palette=custom_palette,
    linewidth=0.4,
    cut=0,
    inner='box',
    order=species_order,
    ax=ax1
)

# Add n
group_counts_species = df['Species'].value_counts()
for i, species in enumerate(species_order):
    if species in group_counts_species.index:
        count = group_counts_species[species]
        max_y = df[df['Species'] == species]['Cluster_Size_Mb'].max()
        ax1.text(i, max_y + 0.035, f'n = {count}', ha='center', va='bottom', fontsize=6, fontweight='bold')

# Add mean as star
sns.pointplot(
    x='Species',
    y='Cluster_Size_Mb',
    data=df,
    estimator='mean',
    color='white',
    markers='*',
    scale=0.4,
    errwidth=0,
    linestyles='',
    order=species_order,
    ax=ax1,
    zorder=7
)

# Add median and outliers
for i, (group, dados) in enumerate(df.groupby('Species')['Cluster_Size_Mb']):
    q1 = np.percentile(dados, 25)
    q3 = np.percentile(dados, 75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mediana = np.median(dados)
    ax1.plot(i, mediana, 'o', color='white', markersize=2,
             markeredgewidth=0.7, markeredgecolor='black', zorder=3)
    outliers = dados[(dados < lower) | (dados > upper)]
    ax1.plot([i]*len(outliers), outliers, 'o', color='white', mew=0.1, mec='k', markersize=1.5, alpha=0.75)

ax1.set_ylabel('Cluster Size (Mb)', fontsize=10)
ax1.set_xlabel('')
ax1.set_xticks(range(len(species_order)))
ax1.set_xticklabels(species_order, rotation=25, ha='center', fontsize=8)
ax1.tick_params(axis='y', labelsize=8)
ax1.set_ylim(0, 2.65)
ax1.set_xlim(-0.5, len(species_order) - 0.5)
ax1.set_title('A', loc='left', fontsize=12, weight='bold')


# -------- PANEL B: By cluster type --------
ax2 = axes[1]

sns.violinplot(
    x='Cluster_Type',
    y='Cluster_Size_Mb',
    data=df,
    palette=color_map,
    linewidth=0.4,
    cut=0,
    inner='box',
    order=type_cluster_order,
    ax=ax2
)

group_counts_type = df['Cluster_Type'].value_counts()
for i, ctype in enumerate(type_cluster_order):
    if ctype in df['Cluster_Type'].values:
        max_y = df[df['Cluster_Type'] == ctype]['Cluster_Size_Mb'].max()
        count = group_counts_type.get(ctype, 0)
        ax2.text(i, max_y + 0.035, f'n = {count}', ha='center', va='bottom', fontsize=6, fontweight='bold')

sns.pointplot(
    x='Cluster_Type',
    y='Cluster_Size_Mb',
    data=df,
    estimator='mean',
    color='white',
    markers='*',
    scale=0.4,
    errwidth=0,
    linestyles='',
    order=type_cluster_order,
    ax=ax2,
    zorder=7
)

for i, (group, dados) in enumerate(df.groupby('Cluster_Type')['Cluster_Size_Mb']):
    q1 = np.percentile(dados, 25)
    q3 = np.percentile(dados, 75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mediana = np.median(dados)
    ax2.plot(i, mediana, 'o', color='white', markersize=2,
             markeredgewidth=0.7, markeredgecolor='black', zorder=3)
    outliers = dados[(dados < lower) | (dados > upper)]
    ax2.plot([i]*len(outliers), outliers, 'o', color='white', mew=0.1, mec='k', markersize=1.5, alpha=0.75)

ax2.set_ylabel('Cluster Size (Mb)', fontsize=10)
ax2.set_xlabel('')
ax2.set_xticks(range(len(type_cluster_order)))
ax2.set_xticklabels(type_cluster_order, rotation=25, ha='center', fontsize=8)
ax2.tick_params(axis='y', labelsize=8)
ax2.set_ylim(0, 2.65)
ax2.set_xlim(-0.5, len(type_cluster_order) - 0.5)
ax2.set_title('B', loc='left', fontsize=12, weight='bold')

# Final layout
plt.tight_layout(h_pad=1)
plt.savefig('/path/cluster_size_combined.pdf',
            dpi=500, format='pdf', bbox_inches='tight', transparent=False)