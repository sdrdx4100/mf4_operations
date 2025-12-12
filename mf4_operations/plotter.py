"""
Plotting module for visualizing channel data
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from typing import List
import logging

logger = logging.getLogger(__name__)


class Plotter:
    """Handles plotting of channel data"""
    
    def __init__(self):
        self.figure = None
        self.canvas = None
    
    def plot_data(self, df: pd.DataFrame, channel_names: List[str]):
        """
        Plot channel data
        
        Args:
            df: DataFrame with channel data (must include 'time' column)
            channel_names: List of channel names to plot
        """
        try:
            if df is None or df.empty:
                logger.error("No data to plot")
                return
            
            # Check if time column exists
            if 'time' not in df.columns:
                logger.error("No time column in data")
                return
            
            # Create figure
            num_channels = len(channel_names)
            
            if num_channels == 0:
                logger.error("No channels specified")
                return
            
            # Determine subplot layout
            if num_channels == 1:
                rows, cols = 1, 1
            elif num_channels == 2:
                rows, cols = 2, 1
            elif num_channels <= 4:
                rows, cols = 2, 2
            elif num_channels <= 6:
                rows, cols = 3, 2
            elif num_channels <= 9:
                rows, cols = 3, 3
            else:
                rows, cols = 4, 3
            
            fig, axes = plt.subplots(rows, cols, figsize=(12, 8))
            fig.suptitle('Channel Data Plot', fontsize=14)
            
            # Flatten axes array for easy iteration
            if num_channels == 1:
                axes = [axes]
            else:
                axes = axes.flatten() if hasattr(axes, 'flatten') else axes
            
            # Plot each channel
            for idx, channel_name in enumerate(channel_names):
                if idx >= len(axes):
                    break
                
                ax = axes[idx]
                
                if channel_name in df.columns:
                    # Plot data
                    ax.plot(df['time'], df[channel_name], linewidth=0.8)
                    ax.set_xlabel('Time (s)', fontsize=9)
                    ax.set_ylabel('Value', fontsize=9)
                    ax.set_title(channel_name, fontsize=10)
                    ax.grid(True, alpha=0.3)
                    ax.tick_params(labelsize=8)
                else:
                    ax.text(0.5, 0.5, f'No data for\n{channel_name}',
                           ha='center', va='center', transform=ax.transAxes)
                    ax.set_xticks([])
                    ax.set_yticks([])
            
            # Hide unused subplots
            for idx in range(num_channels, len(axes)):
                axes[idx].set_visible(False)
            
            plt.tight_layout()
            plt.show()
            
            logger.info(f"Plotted {num_channels} channels")
            
        except Exception as e:
            logger.error(f"Error plotting data: {e}")
            raise
