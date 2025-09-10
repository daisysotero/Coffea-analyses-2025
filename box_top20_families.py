import os
from Bio import SeqIO
import pandas as pd

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
plt.style.use(os.path.join('/path/latex/Documentos', 'SinglePlot_2_axes.mplstyle'))

style = {'alpha': 0.75}
gridstyle = {'linewidth': 0.5, 'alpha': 0.5}
#plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx}')
plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica-Normal']})

# Base directory with family folders
base_dir = "path/to/directory/with/subdirectory/of/families/and/in/subdirectory/has/the/.gbk"

families = os.listdir(base_dir)  # list of 20 families (folder ids)
families

# List with IDs (folder names) of top 20 families
top20_families = [
     'FAM_00004',
     'FAM_00019',
     'FAM_00020',
     'FAM_00023',
     'FAM_00030',
     'FAM_00003',
     'FAM_00021',
     'FAM_00035',
     'FAM_00013',
     'FAM_00009',
     'FAM_00029',
     'FAM_00024',
     'FAM_00001',
     'FAM_00027',
     'FAM_00060',
     'FAM_00008',  
     'FAM_00044',
     'FAM_00050',
     'FAM_00031',
     'FAM_00017',
     
]

data = []

for family in top20_families:
    family_path = os.path.join(base_dir, family)
    
    # Check if directory exists to avoid errors
    if not os.path.isdir(family_path):
        print(f"Directory not found: {family_path}")
        continue
    
    for gbk_file in os.listdir(family_path):
        if not gbk_file.endswith(".gbk"):
            continue
        
        gbk_path = os.path.join(family_path, gbk_file)
        biosyn_gene_count = 0
        
        for record in SeqIO.parse(gbk_path, "genbank"):
            for feature in record.features:
                if feature.type == "CDS":
                    sec_met_vals = feature.qualifiers.get('sec_met', [])
                    if any("Kind: biosynthetic" in val for val in sec_met_vals):
                        biosyn_gene_count += 1
        
        data.append({"Family": family, "Cluster_size": biosyn_gene_count})

df = pd.DataFrame(data)
df

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Initial configuration
plt.figure(figsize=(5, 3))
order = df['Family'].unique()

fig = plt.figure(figsize=(5, 3))
gs = GridSpec(2, 1, height_ratios=[1, 10],hspace=0.02)  # ax1 will be 10x smaller than ax2
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])


# Base palette
base_color = '#1f77b4'
palette = {fam: base_color for fam in order}
# Plot boxplot on both axes
for ax in (ax1, ax2):
    sns.boxplot(
        x='Family',
        y='Cluster_size',
        data=df,
        order=order,
        palette=palette,
        linewidth=0.1,
        showfliers=False,
        width=0.5,
        ax=ax,
        
    )
    
    # Change transparency
    for patch in ax.patches:
        r, g, b, _ = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0.6))
    
    # Individual points
    sns.stripplot(
        x='Family',
        y='Cluster_size',
        data=df,
        order=order,
        color='black',
        size=2.5,
        jitter=True,
        alpha=0.3,
        ax=ax
    )

# Configure axis limits
ax1.set_ylim(22.5, 27)  # Top part
ax2.set_ylim(0, 18)   # Bottom part

# Hide spines (borders) between axes
ax1.spines.bottom.set_visible(False)
ax2.spines.top.set_visible(False)
ax1.xaxis.tick_top()
ax1.tick_params(labeltop=False)  # Don't show labels at top
ax2.xaxis.tick_bottom()
ax1.set_ylabel('')
# Add diagonal lines indicating the break
d = 0.5  # Size of diagonals
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=8,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)

# Common settings
# plt.ylabel('Number of biosynthetic genes per cluster', fontsize=8)
plt.ylabel('Number of biosynthetic genes per cluster', fontsize=8)
plt.xlabel('')
plt.xticks(rotation=90, fontsize=8)

# Adjust Y-axis ticks
ax2.set_yticks([3, 6, 9, 12, 15])
ax2.set_yticklabels([ '3', '6', '9', '12', '15'], fontsize=8)
ax1.set_yticks([24, 27])
ax1.set_yticklabels(['24', ''], fontsize=8)
ax2.set_ylim(2.5,16.5)

# Add texts with counts and totals
total_genes = df.groupby('Family')['Cluster_size'].sum()
num_clusters = df['Family'].value_counts()

for i, fam in enumerate(order):
    total = total_genes.get(fam, 0)
    count = num_clusters.get(fam, 0)
    max_y = df[df['Family'] == fam]['Cluster_size'].max()
    
    # Position text on appropriate axis
    if max_y > 18:
        ax = ax1
        y_pos = max_y + 0.2
    else:
        ax = ax2
        y_pos = max_y + 0.2
    
    ax.text(
        i, y_pos,
        f'{count} \n({total})',
        ha='center',
        va='bottom',
        fontsize=5,
        fontweight='bold',
        color='darkblue'
    )

# Add legend
ax1.text(
    12.5, 24.4,
    'Number of BCGs (number of genes)',
    fontsize=6,
    ha='left',
    va='bottom',
    color='black'
)

ax2.tick_params(
    bottom=False,         # Remove bottom ticks
    labelbottom=False    # Remove bottom labels
)

# 2. Activate ticks and labels at TOP of axis
ax1.tick_params(
    top=True,            # Show ticks at top
    labeltop=True,
    rotation=90# Show labels at top
)

plt.tight_layout()
plt.savefig('/path/boxplot/box.pdf',
            dpi=500, format='pdf', bbox_inches='tight', transparent=False)