import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Add this before other matplotlib imports

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def create_heatmap_seaborn(df, output_file=None, figsize=(12, 8)):
    # Invert the DataFrame rows
    df_inverted = df.iloc[::-1]
    
    # Create figure with white background
    plt.figure(figsize=figsize, facecolor='white')
    
    # Create custom colormap from blue to white to red
    colors = ['#000080', '#0000FF', '#00FFFF', '#00FF00', '#FFFF00', '#FF0000', '#FFFFFF']
    n_bins = 100
    custom_cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)
    
    # Set values above threshold to nan (will be shown as white)
    threshold = 6e4
    df_masked = df_inverted.copy()
    df_masked[df_masked > threshold] = np.nan

    # Create heatmap
    ax = sns.heatmap(df_inverted,
                     annot=False,
                     cmap=custom_cmap,
                     cbar=True,
                     square=False,
                     xticklabels=20,  # Show fewer x ticks
                     yticklabels=20,  # Show fewer y ticks
                     vmin=df_masked.min().min(),  # Set minimum value
                     vmax=threshold)   
    
    # Customize colorbar
    cbar = ax.collections[0].colorbar
    cbar.set_label('Intensity', fontsize=12, labelpad=15)
    cbar.ax.set_yticklabels([f'{x:.3E}' for x in np.linspace(0, 5e4, 6)])
    
    # Set labels with larger font
    plt.xlabel('Emission (nm)', fontsize=12, labelpad=10)
    plt.ylabel('Excitation (nm)', fontsize=12, labelpad=10)
    
    # Set axis ranges
    plt.xlim(0, len(df.columns))
    plt.ylim(len(df), 0)
    
    # Set custom tick labels
    x_ticks = np.linspace(0, len(df.columns)-1, 7)
    x_labels = np.linspace(400, 700, 7)
    plt.xticks(x_ticks, [int(x) for x in x_labels], rotation=0)
    
    y_ticks = np.linspace(0, len(df)-1, 6)
    y_labels = np.linspace(600, 350, 6)
    plt.yticks(y_ticks, [int(y) for y in y_labels])
    
    # Add contour lines
    plt.contour(df_masked, colors='black', alpha=0.3, levels=5)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
    else:
        plt.show()
    
    plt.close()