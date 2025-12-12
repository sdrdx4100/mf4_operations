# Quick Start Guide - MF4 Operations

## Installation

### Option 1: Using Pre-built Executable (Recommended)

1. Download the latest release for your platform:
   - Windows: `MF4Operations.exe`
   - Linux: `MF4Operations`
   - macOS: `MF4Operations`

2. Run the executable directly (no installation required)

### Option 2: From Source

```bash
# Clone the repository
git clone https://github.com/sdrdx4100/mf4_operations.git
cd mf4_operations

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m mf4_operations.main
```

## Basic Usage

### 1. Open a File

- Click **File → Open File...** or use the "Open File..." button
- Select your MF4, MDF, or DAT file
- File information will be displayed in the left panel

### 2. Browse and Select Channels

- All available channels appear in the right panel
- Use the **Search** box to filter channels by name
- Click to select channels (Ctrl/Cmd+Click for multiple selections)
- Selected count is shown at the bottom

### 3. Export to CSV

1. Select the channels you want to export
2. (Optional) Set resample rate in seconds (0.0 = no resampling)
3. Click **Export Selected to CSV...**
4. Choose output location and filename
5. Done! Your CSV file is ready

### 4. Visualize Data

1. Select channels to plot (recommend ≤10 for performance)
2. (Optional) Set resample rate for downsampling
3. Click **Plot Selected Channels**
4. Interactive plot window appears with subplots for each channel

## Tips & Tricks

### Resampling

- Set to `0.01` for 100 Hz output
- Set to `0.1` for 10 Hz output
- Set to `0.0` to keep original sampling rate
- Resampling reduces file size and speeds up plotting

### History Feature

- The app remembers your channel selections per file
- When reopening a file, you'll be asked to restore previous selection
- This saves time on repetitive analysis tasks

### Search Function

- Type partial names to filter channels
- Search is case-insensitive
- Press Enter after typing to search

## Troubleshooting

### Issue: File won't open

**Solution**: Ensure the file is a valid MF4, MDF, or DAT file and not corrupted

### Issue: Channel names appear garbled

**Solution**: This is an encoding issue in the source file. The app handles this gracefully with fallback names

### Issue: Export fails

**Solution**: 
- Check you have write permissions to the output directory
- Ensure you have enough disk space
- Try selecting fewer channels

### Issue: Plot is slow

**Solution**:
- Use resampling to reduce data points
- Select fewer channels (≤10 recommended)
- Close the plot window before creating a new plot

## Settings Location

Your preferences and history are stored in:
- **Windows**: `C:\Users\<username>\.mf4_operations\`
- **Linux/Mac**: `~/.mf4_operations/`

You can delete these files to reset the application to defaults.

## Command Line Usage (Advanced)

For automation or batch processing, you can use the Python API:

```python
from mf4_operations.file_handler import FileHandler

# Load file
handler = FileHandler()
handler.load_file('path/to/file.mf4')

# Get channels
channels = handler.get_channels()
print(f"Found {len(channels)} channels")

# Export to CSV
handler.export_to_csv(
    'output.csv',
    ['Channel1', 'Channel2'],
    resample=0.01  # 100 Hz
)
```

See `demo.py` for more examples.

## Getting Help

- Check the full [README.md](README.md) for detailed documentation
- Report issues on [GitHub Issues](https://github.com/sdrdx4100/mf4_operations/issues)
- Run the demo: `python demo.py`

## Keyboard Shortcuts

- **Ctrl/Cmd+O**: Open file
- **Ctrl/Cmd+E**: Export to CSV
- **Ctrl/Cmd+Q**: Quit application
- **Ctrl/Cmd+A**: Select all channels (in listbox)
