"""
GUI application for MF4 Operations
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import logging
from pathlib import Path
from typing import List, Optional
import threading

from .file_handler import FileHandler
from .settings_manager import SettingsManager
from .plotter import Plotter

logger = logging.getLogger(__name__)


class MF4OperationsGUI:
    """Main GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MF4 Operations - File Converter & Viewer")
        
        # Initialize components
        self.file_handler = FileHandler()
        self.settings_manager = SettingsManager()
        self.plotter = None
        
        # Variables
        self.current_file = None
        self.selected_channels = []
        
        # Setup GUI
        self._setup_ui()
        
        # Restore window geometry
        geometry = self.settings_manager.get_setting('window_geometry', '1200x800')
        self.root.geometry(geometry)
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File...", command=self._open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Export to CSV...",
                              command=lambda: self._export_data('csv'))
        file_menu.add_command(label="Export to Parquet...",
                              command=lambda: self._export_data('parquet'))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)

        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Plot Selected Channels", command=self._plot_channels)
        tools_menu.add_separator()
        tools_menu.add_command(label="Select All (filtered)", command=self._select_all)
        tools_menu.add_command(label="Clear Selection", command=self._clear_selection)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
        
        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - File info and controls
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=1)
        
        # File info section
        file_frame = ttk.LabelFrame(left_panel, text="File Information", padding=10)
        file_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 5))
        
        ttk.Button(file_frame, text="Open File...", 
                  command=self._open_file).pack(fill=tk.X, pady=(0, 5))
        
        self.file_info_text = scrolledtext.ScrolledText(
            file_frame, height=8, width=40, state=tk.DISABLED
        )
        self.file_info_text.pack(fill=tk.BOTH, expand=True)
        
        # Resample settings
        resample_frame = ttk.LabelFrame(left_panel, text="Resample Settings", padding=10)
        resample_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(resample_frame, text="Resample Rate (seconds):").pack(anchor=tk.W)
        self.resample_var = tk.DoubleVar(
            value=self.settings_manager.get_setting('resample_rate', 0.0)
        )
        resample_spinbox = ttk.Spinbox(
            resample_frame, from_=0.0, to=10.0, increment=0.01,
            textvariable=self.resample_var, width=20
        )
        resample_spinbox.pack(fill=tk.X, pady=5)
        ttk.Label(
            resample_frame, 
            text="(0.0 = no resampling)", 
            font=('', 8, 'italic')
        ).pack(anchor=tk.W)
        
        # Export section
        export_frame = ttk.LabelFrame(left_panel, text="Export", padding=10)
        export_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            export_frame, text="Export to CSV...",
            command=lambda: self._export_data('csv')
        ).pack(fill=tk.X, pady=(0, 5))

        ttk.Button(
            export_frame, text="Export to Parquet...",
            command=lambda: self._export_data('parquet')
        ).pack(fill=tk.X)

        ttk.Label(
            export_frame,
            text="Parquet: compact & fast for large data",
            font=('', 8, 'italic')
        ).pack(anchor=tk.W, pady=(5, 0))

        # Plot button
        ttk.Button(
            left_panel, text="Plot Selected Channels",
            command=self._plot_channels
        ).pack(fill=tk.X, pady=5)
        
        # Right panel - Channel list and preview
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=2)
        
        # Channel selection section
        channel_frame = ttk.LabelFrame(right_panel, text="Channel Selection", padding=10)
        channel_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search box
        search_frame = ttk.Frame(channel_frame)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Selection helper buttons
        button_frame = ttk.Frame(channel_frame)
        button_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(
            button_frame, text="Select All",
            command=self._select_all
        ).pack(side=tk.LEFT)
        ttk.Button(
            button_frame, text="Clear",
            command=self._clear_selection
        ).pack(side=tk.LEFT, padx=5)
        
        # Channel listbox with scrollbar
        list_frame = ttk.Frame(channel_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.channel_listbox = tk.Listbox(
            list_frame, selectmode=tk.EXTENDED,
            yscrollcommand=scrollbar.set
        )
        self.channel_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.channel_listbox.yview)
        
        # Selection info
        self.selection_label = ttk.Label(
            channel_frame, text="Selected: 0 channels"
        )
        self.selection_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Bind selection change
        self.channel_listbox.bind('<<ListboxSelect>>', self._on_channel_select)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root, textvariable=self.status_var,
            relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _open_file(self):
        """Open file dialog and load file"""
        last_dir = self.settings_manager.get_setting(
            'last_directory', str(Path.home())
        )
        
        file_path = filedialog.askopenfilename(
            title="Select MF4/MDF/DAT file",
            initialdir=last_dir,
            filetypes=[
                ("Measurement files", "*.mf4 *.mdf *.dat"),
                ("MF4 files", "*.mf4"),
                ("MDF files", "*.mdf"),
                ("DAT files", "*.dat"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        # Save last directory
        self.settings_manager.set_setting('last_directory', str(Path(file_path).parent))
        
        # Load file in background
        self.status_var.set("Loading file...")
        self.root.update()
        
        def load_thread():
            success = self.file_handler.load_file(file_path)
            self.root.after(0, lambda: self._on_file_loaded(success, file_path))
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def _on_file_loaded(self, success: bool, file_path: str):
        """Callback when file is loaded"""
        if not success:
            messagebox.showerror("Error", f"Failed to load file:\n{file_path}")
            self.status_var.set("Ready")
            return
        
        self.current_file = file_path
        
        # Update file info
        self._update_file_info()
        
        # Update channel list
        self._update_channel_list()
        
        # Load history for this file
        self._load_history_for_file()
        
        self.status_var.set(f"Loaded: {Path(file_path).name}")
    
    def _update_file_info(self):
        """Update file information display"""
        info = self.file_handler.get_file_info()
        
        self.file_info_text.config(state=tk.NORMAL)
        self.file_info_text.delete(1.0, tk.END)
        
        if info:
            for key, value in info.items():
                self.file_info_text.insert(tk.END, f"{key}: {value}\n")
        
        self.file_info_text.config(state=tk.DISABLED)
    
    def _update_channel_list(self, filter_text: str = ""):
        """Update channel listbox"""
        channels = self.file_handler.get_channels()
        
        self.channel_listbox.delete(0, tk.END)
        
        # Filter channels
        if filter_text:
            filter_lower = filter_text.lower()
            channels = [ch for ch in channels if filter_lower in ch.lower()]
        
        # Add to listbox
        for channel in channels:
            self.channel_listbox.insert(tk.END, channel)
        
        self.status_var.set(f"Showing {len(channels)} channels")
    
    def _on_search(self, *args):
        """Handle search text change"""
        search_text = self.search_var.get()
        self._update_channel_list(search_text)
    
    def _on_channel_select(self, event):
        """Handle channel selection change"""
        selection = self.channel_listbox.curselection()
        self.selected_channels = [
            self.channel_listbox.get(i) for i in selection
        ]
        
        self.selection_label.config(
            text=f"Selected: {len(self.selected_channels)} channels"
        )
    
    def _clear_selection(self):
        """Clear channel selection"""
        self.channel_listbox.selection_clear(0, tk.END)
        self.selected_channels = []
        self.selection_label.config(text="Selected: 0 channels")

    def _select_all(self):
        """Select all channels currently shown in the listbox"""
        count = self.channel_listbox.size()
        if count == 0:
            return
        self.channel_listbox.selection_set(0, tk.END)
        self.selected_channels = [
            self.channel_listbox.get(i) for i in range(count)
        ]
        self.selection_label.config(
            text=f"Selected: {len(self.selected_channels)} channels"
        )
    
    def _load_history_for_file(self):
        """Load and apply label selection history for current file"""
        if not self.current_file:
            return
        
        history = self.settings_manager.get_history_for_file(self.current_file)
        
        if history:
            # Get most recent entry
            recent = history[0]
            labels = recent.get('labels', [])
            
            if labels:
                # Ask user if they want to load previous selection
                response = messagebox.askyesno(
                    "History Found",
                    f"Found previous selection with {len(labels)} channels.\n"
                    "Load previous selection?"
                )
                
                if response:
                    self._select_channels_by_name(labels)
    
    def _select_channels_by_name(self, channel_names: List[str]):
        """Select channels by name"""
        self.channel_listbox.selection_clear(0, tk.END)
        
        for i in range(self.channel_listbox.size()):
            channel = self.channel_listbox.get(i)
            if channel in channel_names:
                self.channel_listbox.selection_set(i)
        
        # Update selected channels
        selection = self.channel_listbox.curselection()
        self.selected_channels = [
            self.channel_listbox.get(i) for i in selection
        ]
        self.selection_label.config(
            text=f"Selected: {len(self.selected_channels)} channels"
        )
    
    # Per-format save dialog configuration
    _EXPORT_FORMATS = {
        'csv': {
            'title': "Export to CSV",
            'extension': ".csv",
            'filetypes': [("CSV files", "*.csv"), ("All files", "*.*")],
        },
        'parquet': {
            'title': "Export to Parquet",
            'extension': ".parquet",
            'filetypes': [("Parquet files", "*.parquet"), ("All files", "*.*")],
        },
    }

    def _export_data(self, fmt: str):
        """Export selected channels in the given format ('csv' or 'parquet')"""
        if not self.current_file:
            messagebox.showwarning("Warning", "No file loaded")
            return

        if not self.selected_channels:
            messagebox.showwarning("Warning", "No channels selected")
            return

        config = self._EXPORT_FORMATS.get(fmt, self._EXPORT_FORMATS['csv'])

        # Get output file path
        output_path = filedialog.asksaveasfilename(
            title=config['title'],
            defaultextension=config['extension'],
            filetypes=config['filetypes'],
            initialfile=Path(self.current_file).stem + config['extension']
        )

        if not output_path:
            return

        # Get resample rate
        resample_rate = self.resample_var.get()
        if resample_rate <= 0:
            resample_rate = None

        # Export in background
        self.status_var.set(f"Exporting to {fmt.upper()}...")
        self.root.update()

        def export_thread():
            success = self.file_handler.export_data(
                output_path, self.selected_channels, resample_rate, fmt=fmt
            )
            self.root.after(0, lambda: self._on_export_complete(success, output_path))

        threading.Thread(target=export_thread, daemon=True).start()
    
    def _on_export_complete(self, success: bool, output_path: str):
        """Callback when export is complete"""
        if success:
            messagebox.showinfo("Success", f"Exported to:\n{output_path}")
            self.status_var.set("Export complete")
            
            # Save to history
            self.settings_manager.add_to_history(
                self.current_file, self.selected_channels
            )
        else:
            messagebox.showerror("Error", "Export failed")
            self.status_var.set("Export failed")
    
    def _plot_channels(self):
        """Plot selected channels"""
        if not self.selected_channels:
            messagebox.showwarning("Warning", "No channels selected")
            return
        
        # Limit number of channels for plotting
        if len(self.selected_channels) > 10:
            response = messagebox.askyesno(
                "Warning",
                f"You selected {len(self.selected_channels)} channels.\n"
                "Plotting many channels may be slow.\n"
                "Continue?"
            )
            if not response:
                return
        
        # Get data
        self.status_var.set("Loading data for plotting...")
        self.root.update()
        
        resample_rate = self.resample_var.get()
        if resample_rate <= 0:
            resample_rate = None
        
        def plot_thread():
            df = self.file_handler.get_channel_data(
                self.selected_channels, resample_rate
            )
            self.root.after(0, lambda: self._on_data_ready_for_plot(df))
        
        threading.Thread(target=plot_thread, daemon=True).start()
    
    def _on_data_ready_for_plot(self, df):
        """Callback when data is ready for plotting"""
        if df is None:
            messagebox.showerror("Error", "Failed to load channel data")
            self.status_var.set("Plot failed")
            return
        
        try:
            # Create plotter
            self.plotter = Plotter()
            self.plotter.plot_data(df, self.selected_channels)
            
            self.status_var.set("Plot displayed")
            
            # Save to history
            self.settings_manager.add_to_history(
                self.current_file, self.selected_channels
            )
            
        except Exception as e:
            logger.error(f"Error plotting data: {e}")
            messagebox.showerror("Error", f"Failed to plot data:\n{e}")
            self.status_var.set("Plot failed")
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """MF4 Operations v1.1.0

A fast and lightweight application for handling
MF4/MDF/DAT measurement files.

Features:
• Load MF4/MDF/DAT files
• Preview and select channels
• Export to CSV or Parquet with optional resampling
• Plot channel data
• Save label selection history

Developed for automotive engineers."""
        
        messagebox.showinfo("About MF4 Operations", about_text)
    
    def _on_close(self):
        """Handle window close"""
        # Save window geometry
        geometry = self.root.geometry()
        self.settings_manager.set_setting('window_geometry', geometry)
        
        # Save resample rate
        self.settings_manager.set_setting('resample_rate', self.resample_var.get())
        
        # Close file handler
        self.file_handler.close()
        
        # Close window
        self.root.destroy()


def run_gui():
    """Run the GUI application"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run GUI
    root = tk.Tk()
    app = MF4OperationsGUI(root)
    root.mainloop()
