"""
File handler module for reading MF4/MDF/DAT files
Handles encoding errors and provides unified interface
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import pandas as pd
from asammdf import MDF
import logging

logger = logging.getLogger(__name__)


class FileHandler:
    """Handles MF4/MDF/DAT file operations with encoding error handling"""
    
    def __init__(self):
        self.mdf = None
        self.file_path = None
        self.channels = []
        
    def load_file(self, file_path: str) -> bool:
        """
        Load MF4/MDF/DAT file
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False
                
            # Check file extension
            ext = file_path.suffix.lower()
            if ext not in ['.mf4', '.mdf', '.dat']:
                logger.warning(f"Unsupported file extension: {ext}")
                # Try to load anyway
                
            # Load file with asammdf
            self.mdf = MDF(str(file_path))
            self.file_path = file_path
            
            # Get channel list
            self.channels = []
            for group_index, group in enumerate(self.mdf.groups):
                for channel_index, channel in enumerate(group.channels):
                    try:
                        # Handle encoding errors when reading channel names
                        if hasattr(channel, 'name'):
                            name = str(channel.name)
                        else:
                            name = f"Channel_{group_index}_{channel_index}"
                        self.channels.append(name)
                    except (UnicodeDecodeError, AttributeError) as e:
                        logger.warning(f"Error reading channel name: {e}")
                        self.channels.append(f"Channel_{group_index}_{channel_index}")
            
            logger.info(f"Loaded file: {file_path} with {len(self.channels)} channels")
            return True
            
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            return False
    
    def get_channels(self) -> List[str]:
        """Get list of available channels"""
        return self.channels.copy()
    
    def get_channel_data(self, channel_names: List[str], 
                        resample: Optional[float] = None) -> Optional[pd.DataFrame]:
        """
        Get data for selected channels
        
        Args:
            channel_names: List of channel names to extract
            resample: Optional resampling rate in seconds
            
        Returns:
            DataFrame with channel data or None if error
        """
        if not self.mdf:
            logger.error("No file loaded")
            return None
            
        try:
            # Extract channels
            data_dict = {}
            
            for channel_name in channel_names:
                try:
                    # Get signal
                    signal = self.mdf.get(channel_name)
                    
                    # Handle resampling
                    if resample and resample > 0:
                        # Resample signal
                        timestamps = signal.timestamps
                        if len(timestamps) > 1:
                            start = timestamps[0]
                            end = timestamps[-1]
                            # Use numpy.arange for precise floating-point resampling
                            import numpy as np
                            new_timestamps = np.arange(start, end, resample)
                            # Simple interpolation
                            resampled = pd.Series(signal.samples, index=timestamps)
                            resampled = resampled.reindex(
                                new_timestamps, method='nearest'
                            )
                            data_dict[channel_name] = resampled.values
                            if 'time' not in data_dict:
                                data_dict['time'] = new_timestamps
                        else:
                            data_dict[channel_name] = signal.samples
                            if 'time' not in data_dict:
                                data_dict['time'] = signal.timestamps
                    else:
                        data_dict[channel_name] = signal.samples
                        if 'time' not in data_dict:
                            data_dict['time'] = signal.timestamps
                            
                except Exception as e:
                    logger.error(f"Error extracting channel {channel_name}: {e}")
                    continue
            
            if not data_dict:
                return None
                
            # Create DataFrame
            # Ensure all arrays have the same length (use shortest)
            min_len = min(len(v) for v in data_dict.values())
            for key in data_dict:
                data_dict[key] = data_dict[key][:min_len]
                
            df = pd.DataFrame(data_dict)
            return df
            
        except Exception as e:
            logger.error(f"Error getting channel data: {e}")
            return None
    
    def export_to_csv(self, output_path: str, channel_names: List[str],
                     resample: Optional[float] = None) -> bool:
        """
        Export selected channels to CSV
        
        Args:
            output_path: Path for output CSV file
            channel_names: List of channels to export
            resample: Optional resampling rate
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df = self.get_channel_data(channel_names, resample)
            if df is None:
                return False
                
            # Export to CSV with proper encoding
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            logger.info(f"Exported to CSV: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return False
    
    def get_file_info(self) -> Dict[str, Any]:
        """Get information about loaded file"""
        if not self.mdf:
            return {}
            
        try:
            info = {
                'file_path': str(self.file_path),
                'version': str(self.mdf.version),
                'channel_count': len(self.channels),
            }
            
            # Try to get additional info
            try:
                if hasattr(self.mdf, 'header'):
                    header = self.mdf.header
                    if hasattr(header, 'start_time'):
                        info['start_time'] = str(header.start_time)
                    if hasattr(header, 'author'):
                        info['author'] = str(header.author)
                    if hasattr(header, 'comment'):
                        info['comment'] = str(header.comment)
            except Exception as e:
                logger.debug(f"Could not extract additional info: {e}")
                
            return info
            
        except Exception as e:
            logger.error(f"Error getting file info: {e}")
            return {}
    
    def close(self):
        """Close the file"""
        if self.mdf:
            try:
                self.mdf.close()
            except:
                pass
            self.mdf = None
            self.file_path = None
            self.channels = []
