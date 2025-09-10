#data (df_transposed) > Species in rown and variables (number orthogrups, number unassigned genes...) in columns 


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


df2 = df_transposed[['Species','Number of genes in orthogroups',
                    'Number of unassigned genes']].iloc[::-1]

df3 = df_transposed[['Species','Number of orthogroups containing species']].iloc[::-1]


xlabel = ['BGC [$\\%$]']
ylabel = []

def bar_empilhada_plot(ax, df, cores, direcao_barra, coluna_desejada, rotacao, xlabel, ylabel, xlim,fontsize):
    
    
    
    df.plot(kind=direcao_barra, stacked=True, ax=ax, edgecolor='black', color=cores,
                             lw=0.5,legend=False, width=0.7)

    handles, labels = None, None
    handles, labels = ax.get_legend_handles_labels()
    ax.set_yticks(range(len(df[coluna_desejada]))) # Define as posições dos rótulos
    ax.set_yticklabels(df[coluna_desejada], rotation=rotacao,fontsize=fontsize)

    ax.set_xlim(None,xlim)
        
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


cores = ["C0",
"C3"
]  

################## GRAPH 1 ##################
################## GRAPH 1 ##################
################## GRAPH 1 ##################

xlabel = []
ylabel = ['Genes number']
xlim=30000
fontsize = 9
handles1, labels1 = bar_empilhada_plot(axs[0], df2,
                                     cores, direcao_barra, 
                                     coluna_desejada, rotacao, xlabel,ylabel, xlim,fontsize)


####################################

fig.legend(handles1, labels1, loc='right',  
           bbox_to_anchor=(1.259, 0.766),
           ncol=1, frameon=False)



grupos = {
    'Low-altitude West and Central Africa': [
    'C. canephora','C. arabica sgC_ET39','C. arabica sgCC_bourbon',
    'C. arabica sgCC_catura','C. arabica sgC_geisha'
    ],

    'High-Altitude East and Central Africa': [
    'C. eugenioides_BUA','C. eugenioides_CCC68of','C. arabica sgE_ET39',
    'C. arabica sgEE_bourbon','C. arabica sgEE_catura','C. arabica sgE_geisha'
    ]
}


cores_grupos = {
    'Low-altitude West and Central Africa': '#99249eff', 
    'High-Altitude East and Central Africa': '#9B870C',  
}

    
cores_rotulos = []
for especie in df2['Species']:
    for grupo, especies in grupos.items():
        if especie in especies:
            cores_rotulos.append(cores_grupos[grupo])
            break  


for i, label in enumerate(axs[0].get_yticklabels()):
    label.set_color(cores_rotulos[i]) 

    

axs[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}'))
axs[0].set_xlabel(r"Genes number ($ \times 10^3$)", fontsize=8)  # Ajuste o nome e o tamanho da fonte


for i, (total, valor) in enumerate(zip(df2.iloc[:, 1:].sum(axis=1),  
                                       df_transposed["Number of genes in species-specific orthogroups"].iloc[::-1])):  
    axs[0].text(total + (xlim * 0.01), i-0.12, f"{int(valor)}",  
             color="green", fontsize=8, va="center", ha="left", fontweight="bold")
    

fig.text(1.11 + deslocamento, 0.6, 'Number of genes in species-specific orthogroups', 
         ha='center', va='bottom', fontsize=8, color='green')


for i, valor in enumerate(df2['Number of genes in orthogroups']):
    axs[0].text(valor - (xlim * 0.02), i, f"{int(valor)}", 
                color="white", fontsize=8, va="center", ha="right", fontweight="bold")

################## GRAPH 2 ##################
################## GRAPH 2 ##################
################## GRAPH 2 ##################

cores = ["#11833bfc"]  

xlabel = []
ylabel = ['Genes number']
xlim=23000
handles1, labels1 = bar_empilhada_plot(axs[1], df3,
                                     cores, direcao_barra, 
                                     coluna_desejada, rotacao, xlabel,ylabel, xlim,fontsize)

####################################

fig.legend(handles1, labels1, loc='right',  
           bbox_to_anchor=(1.32, 0.7),
           ncol=1, frameon=False)


grupos = {
    'Low-altitude West and Central Africa': [
    'C. canephora','C. arabica sgC_ET39','C. arabica sgCC_bourbon',
    'C. arabica sgCC_catura','C. arabica sgC_geisha'
    ],

    'High-Altitude East and Central Africa': [
    'C. eugenioides_BUA','C. eugenioides_CCC68of','C. arabica sgE_ET39',
    'C. arabica sgEE_bourbon','C. arabica sgEE_catura','C. arabica sgE_geisha'
    ]

}



cores_grupos = {
    'Low-altitude West and Central Africa': '#99249eff',  
    'High-Altitude East and Central Africa': '#9B870C',  

}

    

cores_rotulos = []
for especie in df3['Species']:
    for grupo, especies in grupos.items():
        if especie in especies:
            cores_rotulos.append(cores_grupos[grupo])
            break 


for i, label in enumerate(axs[1].get_yticklabels()):
    label.set_color(cores_rotulos[i]) 
    

for i, valor in enumerate(df3['Number of orthogroups containing species']):
    axs[1].text(valor - (xlim * 0.02), i, f"{int(valor)}", 
                color="white", fontsize=8, va="center", ha="right", fontweight="bold")

    

axs[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}'))
axs[1].set_xlabel(r"Orthogroups number ($ \times 10^3$)", fontsize=8)  # Ajuste o nome e o tamanho da fonte


for i, (total, valor) in enumerate(zip(df3.iloc[:, 1:].sum(axis=1),   
                                       df_transposed["Number of species-specific orthogroups"].iloc[::-1])):  
    axs[1].text(total + (xlim * 0.01), i-0.12, f"{int(valor)}",  # Posição exata no final da barra
             color="#3b321ffc", fontsize=8, va="center", ha="left", fontweight="bold")
    
fig.text(1.082 + deslocamento, 0.55, 'Number of species-specific orthogroups', 
          ha='center', va='bottom', fontsize=8, color='#3b321ffc')



x_values = [1.07, 0.38, 1.07, 0.80, 0.90]

# Deslocamento desejado para a direita
deslocamento = 0.05 

##Adicionando o texto com o deslocamento
fig.text(x_values[0] + deslocamento, 0.45, 'Low-altitude West and Central Africa', 
         ha='center', va='bottom', fontsize=8, color='#99249eff')
fig.text(x_values[2] + deslocamento, 0.41, 'High-Altitude East and Central Africa', 
         ha='center', va='bottom', fontsize=8, color='goldenrod')




plt.tight_layout()
plt.savefig(r'path/statistic_per_species.pdf',
            bbox_inches='tight',pad_inches=0.02, transparent=True, dpi=700)