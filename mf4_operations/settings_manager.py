"""
Settings manager for storing user preferences and label selection history
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SettingsManager:
    """Manages user settings and label selection history"""
    
    def __init__(self):
        # Settings directory in user home
        self.settings_dir = Path.home() / '.mf4_operations'
        self.settings_file = self.settings_dir / 'settings.json'
        self.history_file = self.settings_dir / 'label_history.json'
        
        # Ensure settings directory exists
        self.settings_dir.mkdir(parents=True, exist_ok=True)
        
        # Default settings
        self.settings = {
            'last_directory': str(Path.home()),
            'resample_rate': 0.0,
            'max_history': 50,
            'window_geometry': '1200x800',
            'theme': 'default',
        }
        
        # Label selection history
        self.label_history = []
        
        # Load existing settings
        self.load_settings()
        self.load_history()
    
    def load_settings(self) -> bool:
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
                logger.info("Settings loaded successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return False
    
    def save_settings(self) -> bool:
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            logger.info("Settings saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def load_history(self) -> bool:
        """Load label selection history"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.label_history = json.load(f)
                logger.info(f"Loaded {len(self.label_history)} history items")
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return False
    
    def save_history(self) -> bool:
        """Save label selection history"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.label_history, f, indent=2, ensure_ascii=False)
            logger.info("History saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving history: {e}")
            return False
    
    def add_to_history(self, file_path: str, selected_labels: List[str]):
        """
        Add label selection to history
        
        Args:
            file_path: Path to the file
            selected_labels: List of selected label names
        """
        try:
            # Create history entry
            entry = {
                'file_path': str(file_path),
                'file_name': Path(file_path).name,
                'labels': selected_labels.copy(),
                'timestamp': self._get_timestamp(),
            }
            
            # Add to history (newest first)
            self.label_history.insert(0, entry)
            
            # Limit history size
            max_history = self.settings.get('max_history', 50)
            if len(self.label_history) > max_history:
                self.label_history = self.label_history[:max_history]
            
            # Save history
            self.save_history()
            
        except Exception as e:
            logger.error(f"Error adding to history: {e}")
    
    def get_history_for_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Get history entries for a specific file
        
        Args:
            file_path: Path to the file
            
        Returns:
            List of history entries for the file
        """
        try:
            file_name = Path(file_path).name
            return [
                entry for entry in self.label_history
                if entry.get('file_name') == file_name
            ]
        except Exception as e:
            logger.error(f"Error getting file history: {e}")
            return []
    
    def get_recent_labels(self, limit: int = 10) -> List[str]:
        """
        Get recently used labels across all files
        
        Args:
            limit: Maximum number of labels to return
            
        Returns:
            List of recently used label names
        """
        try:
            # Collect all labels from history
            all_labels = []
            seen = set()
            
            for entry in self.label_history:
                for label in entry.get('labels', []):
                    if label not in seen:
                        all_labels.append(label)
                        seen.add(label)
                        if len(all_labels) >= limit:
                            return all_labels
            
            return all_labels
            
        except Exception as e:
            logger.error(f"Error getting recent labels: {e}")
            return []
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any):
        """Set a setting value and save"""
        self.settings[key] = value
        self.save_settings()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as string"""
        from datetime import datetime
        return datetime.now().isoformat()
