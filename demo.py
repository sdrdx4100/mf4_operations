"""
Demo script showing programmatic usage of MF4 Operations
This demonstrates the core functionality without GUI
"""

import logging
import numpy as np
from pathlib import Path
from tempfile import gettempdir
from asammdf import MDF, Signal

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_sample_mf4_file(filepath: str) -> bool:
    """
    Create a sample MF4 file for testing
    
    Args:
        filepath: Path where to save the MF4 file
        
    Returns:
        True if successful
    """
    try:
        logger.info(f"Creating sample MF4 file: {filepath}")
        
        # Create time array (10 seconds at 100 Hz)
        time = np.arange(0, 10, 0.01)
        
        # Create sample signals
        signals = []
        
        # Signal 1: Sine wave
        sine_data = np.sin(2 * np.pi * 1 * time)
        signals.append(Signal(
            samples=sine_data,
            timestamps=time,
            name='SineWave_1Hz',
            unit='V'
        ))
        
        # Signal 2: Cosine wave
        cosine_data = np.cos(2 * np.pi * 2 * time)
        signals.append(Signal(
            samples=cosine_data,
            timestamps=time,
            name='CosineWave_2Hz',
            unit='V'
        ))
        
        # Signal 3: Linear ramp
        ramp_data = time * 10
        signals.append(Signal(
            samples=ramp_data,
            timestamps=time,
            name='LinearRamp',
            unit='m/s'
        ))
        
        # Signal 4: Square wave
        square_data = np.where(np.sin(2 * np.pi * 0.5 * time) > 0, 1, -1)
        signals.append(Signal(
            samples=square_data,
            timestamps=time,
            name='SquareWave_0.5Hz',
            unit='A'
        ))
        
        # Signal 5: Noisy signal
        noise_data = np.random.randn(len(time)) * 0.1 + time * 0.5
        signals.append(Signal(
            samples=noise_data,
            timestamps=time,
            name='NoisySignal',
            unit='°C'
        ))
        
        # Create MDF file
        mdf = MDF()
        mdf.append(signals)
        mdf.save(filepath, overwrite=True)
        
        logger.info(f"✓ Created sample MF4 file with {len(signals)} signals")
        return True
        
    except Exception as e:
        logger.error(f"✗ Error creating sample file: {e}")
        return False


def demo_file_operations():
    """Demonstrate file operations"""
    from mf4_operations.file_handler import FileHandler
    
    logger.info("\n" + "="*60)
    logger.info("Demo: File Operations")
    logger.info("="*60)
    
    # Create sample file (cross-platform temp directory)
    temp_dir = Path(gettempdir())
    sample_file = str(temp_dir / "sample_measurement.mf4")
    if not create_sample_mf4_file(sample_file):
        logger.error("Failed to create sample file")
        return False
    
    # Load file
    handler = FileHandler()
    logger.info(f"\nLoading file: {sample_file}")
    
    if not handler.load_file(sample_file):
        logger.error("Failed to load file")
        return False
    
    # Get channels
    channels = handler.get_channels()
    logger.info(f"\n✓ Found {len(channels)} channels:")
    for i, channel in enumerate(channels, 1):
        logger.info(f"  {i}. {channel}")
    
    # Get file info
    info = handler.get_file_info()
    logger.info(f"\n✓ File information:")
    for key, value in info.items():
        logger.info(f"  {key}: {value}")
    
    # Get data for some channels
    selected_channels = channels[:3]
    logger.info(f"\n✓ Getting data for channels: {selected_channels}")
    
    df = handler.get_channel_data(selected_channels)
    if df is not None:
        logger.info(f"  Data shape: {df.shape}")
        logger.info(f"  Columns: {list(df.columns)}")
        logger.info(f"\n  First few rows:")
        logger.info(df.head().to_string(index=False))
    
    # Export to CSV
    csv_file = str(temp_dir / "sample_export.csv")
    logger.info(f"\n✓ Exporting to CSV: {csv_file}")
    
    if handler.export_to_csv(csv_file, selected_channels):
        logger.info(f"  Export successful!")
        # Show file size
        size = Path(csv_file).stat().st_size
        logger.info(f"  File size: {size:,} bytes")
    else:
        logger.error("  Export failed")
    
    # Test resampling
    logger.info(f"\n✓ Testing resampling (0.1s intervals):")
    df_resampled = handler.get_channel_data(selected_channels, resample=0.1)
    if df_resampled is not None:
        logger.info(f"  Original data points: {len(df)}")
        logger.info(f"  Resampled data points: {len(df_resampled)}")
        logger.info(f"  Reduction: {100*(1-len(df_resampled)/len(df)):.1f}%")
    
    # Cleanup
    handler.close()
    logger.info("\n✓ File operations demo completed successfully")
    
    return True


def demo_settings():
    """Demonstrate settings management"""
    from mf4_operations.settings_manager import SettingsManager
    
    logger.info("\n" + "="*60)
    logger.info("Demo: Settings Management")
    logger.info("="*60)
    
    manager = SettingsManager()
    
    logger.info(f"\n✓ Settings directory: {manager.settings_dir}")
    
    # Set and get settings
    logger.info("\n✓ Testing settings operations:")
    manager.set_setting('demo_setting', 'demo_value')
    value = manager.get_setting('demo_setting')
    logger.info(f"  Set and retrieved: demo_setting = {value}")
    
    # Test history
    logger.info("\n✓ Testing history operations:")
    temp_dir = Path(gettempdir())
    manager.add_to_history(str(temp_dir / 'test1.mf4'), ['channel_A', 'channel_B'])
    manager.add_to_history(str(temp_dir / 'test2.mf4'), ['channel_C', 'channel_D', 'channel_E'])
    manager.add_to_history(str(temp_dir / 'test1.mf4'), ['channel_A', 'channel_F'])
    
    # Get recent labels
    recent = manager.get_recent_labels(limit=5)
    logger.info(f"  Recent labels: {recent}")
    
    # Get history for specific file
    history = manager.get_history_for_file(str(temp_dir / 'test1.mf4'))
    logger.info(f"  History entries for test1.mf4: {len(history)}")
    
    logger.info("\n✓ Settings management demo completed successfully")
    
    return True


def main():
    """Run all demos"""
    logger.info("="*60)
    logger.info("MF4 Operations - Functionality Demo")
    logger.info("="*60)
    
    success = True
    
    # Demo file operations
    if not demo_file_operations():
        success = False
    
    # Demo settings
    if not demo_settings():
        success = False
    
    # Summary
    logger.info("\n" + "="*60)
    if success:
        logger.info("✓ All demos completed successfully!")
        logger.info("\nTo run the GUI application, use:")
        logger.info("  python -m mf4_operations.main")
    else:
        logger.error("✗ Some demos failed")
    logger.info("="*60)
    
    return 0 if success else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
