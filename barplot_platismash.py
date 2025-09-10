import pandas as pd
import matplotlib.patches as patches
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
import os
import ezodf
from Bio import SeqIO
import xlrd
import re
import matplotlib
import matplotlib.cm as cm
import matplotlib as mpl
from __future__ import unicode_literals
from matplotlib.gridspec import GridSpec
matplotlib.rcParams['text.usetex'] = True
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import AutoMinorLocator

#2 figures, and 2 datafrme
#df 1-> df_pivot_specie -> Species in rows, and cluter type (alkaloids, terpenes, putative...) in columns
#df 2-> df_pivot_chr -> Species in rows, and chromossomes (Chr01, Chr02, Chr03...) in columns

xlabel = ['BGC [$\\%$]']
ylabel = []

def bar_empilhada_plot(ax, df, cores, direcao_barra, 
                       coluna_desejada, rotacao, xlabel, ylabel, xlim):
    
    
    
    df.plot(kind=direcao_barra, stacked=True, ax=ax, edgecolor='black', color=cores,
                             lw=0.5,legend=False, width=0.7)

    handles, labels = None, None
    handles, labels = ax.get_legend_handles_labels()
    ax.set_yticks(range(len(df[coluna_desejada]))) # Define as posições dos rótulos
    ax.set_yticklabels(df[coluna_desejada], rotation=rotacao, fontsize=8.5)
    ax.invert_yaxis() 
    ax.set_xlim(None,xlim)
    
    if len(xlabel) > 0:
        ax.set_xlabel(xlabel[0])
    if len(ylabel) > 0:
        ax.set_ylabel(ylabel[0])
        
    return handles, labels


label_size=8
plots_em_x=2
plots_em_y=1

h_size     = 4
v_size     = 4

fig, axs = plt.subplots(plots_em_y,plots_em_x, figsize=(h_size*plots_em_x, v_size*plots_em_y),layout='constrained')

direcao_barra='barh'
coluna_desejada='Species'
rotacao=0

cores = [
"#FF1F20",  # Vermelho mais vibrante
"#4D91FF",  # Azul mais brilhante
"#5CE657",  # Verde mais intenso
"#B957C8",  # Roxo mais vivo
"#FF9900",  # Laranja mais destacado
"#FFFF66" ,  # Amarelo mais brilhante
"#003333",  # Teal muito escuro
"#004D4D",  # Teal escuro
"#006666",  # Teal médio escuro
"#008080",  # Teal médio
"#339999",  # Teal claro
"#66B2B2",  # Teal mais claro
"#99CCCC",  # Teal suave
"#BFE5E5",  # Teal pastel
"#E5F5F5",  # Teal muito suave
]


################## graph 1 ##################
xlabel = ['Total number of clusters']
ylabel = []
xlim=63
handles1, labels1 = bar_empilhada_plot(axs[0], df_pivot_specie, cores, direcao_barra, 
                                     coluna_desejada, rotacao, xlabel,ylabel, xlim)


### colcoar numero ao fim da barra
for i, total in enumerate(df_pivot_specie.iloc[:, 1:].sum(axis=1)):
    axs[0].text(total+0.5, i, f'{total:.0f}', 
                va='center', ha='left', 
                fontsize=9, color='black')
    

################## graph 2 ##################
cores2 = [
    '#035201ff', '#12b302ff', '#48fb2aff', '#9fab03ff', '#ebb503ff', '#f6f602ff', '#04001fff', '#130290ff',
    '#2408fbff', '#7361fcff', '#aba0fdff',
     '#ffebee', '#ffcdd2', '#ef9a9a', '#e57373', '#f44336', '#e53935', '#d32f2f', '#c62828',
    '#b71c1c', '#ff8a80', '#ff5252'] 
    
xlabel = ['Total number of cluters']
xlim=63

handles3, labels3 = bar_empilhada_plot(axs[1], df_pivot_chr, cores2, direcao_barra, 
                                     coluna_desejada, rotacao, xlabel,ylabel, xlim)

### colcoar numero ao fim da barra
for i, total in enumerate(df_pivot_chr.iloc[:, 1:].sum(axis=1)):
    axs[1].text(total+0.5, i, f'{total:.0f}', 
                va='center', ha='left', 
                fontsize=9, color='black')
    

####################################

fig.legend(handles1, labels1, loc='center',  
           bbox_to_anchor=(0.6, 1.10),
           ncol=5, frameon=False,fontsize=9)


fig.legend(handles3, labels3, loc='center',  
           bbox_to_anchor=(1.07, 0.53),
           ncol=1, frameon=False,fontsize=8)



grupos = {
    'Low-altitude West and Central Africa': [
    'C. canephora','C. arabica sgC_ET39','C. arabica sgCC_bourbon',
    'C. arabica sgCC_catura','C. arabica sgC_geisha'
    ],
    'High-Altitude East and Central Africa': [
    'C. eugenioides_BUA','C. eugenioides_CCC68of','C. arabica sgE_ET39',
    'C. arabica sgEE_bourbon','C. arabica sgEE_catura','C. arabica sgE_geisha']}


# Defina as cores para cada grupo
cores_grupos = {
    'Low-altitude West and Central Africa': '#99249eff',  # cor para este grupo
    'High-Altitude East and Central Africa': '#9B870C',  # cor para este grupo

}

    
cores_rotulos = []
for especie in df_pivot_specie['Species']:
    for grupo, especies in grupos.items():
        if especie in especies:
            cores_rotulos.append(cores_grupos[grupo])
            break  


for i, label in enumerate(axs[0].get_yticklabels()):
    label.set_color(cores_rotulos[i]) 
    

cores_rotulos = []
for especie in df_pivot_chr['Species']:
    for grupo, especies in grupos.items():
        if especie in especies:
            cores_rotulos.append(cores_grupos[grupo])
            break  

for i, label in enumerate(axs[1].get_yticklabels()):
    label.set_color(cores_rotulos[i]) 


handles = [Line2D([0], [0], marker='s', color='w', label=group, 
                  markerfacecolor=cores_grupos[group], markersize=10, 
                  markeredgewidth=1, markeredgecolor='black') for group in cores_grupos]




x_values = [0.3, 0.38, 0.61, 0.80, 0.90]

# Deslocamento desejado para a direita
deslocamento = 0.1  #

fig.text(x_values[0] + deslocamento, 0.98, 'Low-altitude West and Central Africa', 
         ha='center', va='bottom', fontsize=9, color='#99249eff')
fig.text(x_values[2] + deslocamento, 0.98, 'High-Altitude East and Central Africa', 
         ha='center', va='bottom', fontsize=9, color='goldenrod')


plt.tight_layout()
plt.savefig(r'/path/cluster_species_cromoss.pdf',bbox_inches='tight',pad_inches=0.02, transparent=True, dpi=700)