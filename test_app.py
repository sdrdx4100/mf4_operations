"""
Simple test script to verify the application components
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_imports():
    """Test that all modules can be imported"""
    try:
        from mf4_operations import __version__
        from mf4_operations.file_handler import FileHandler
        from mf4_operations.settings_manager import SettingsManager
        from mf4_operations.plotter import Plotter
        from mf4_operations.gui import MF4OperationsGUI
        
        logger.info("✓ All modules imported successfully")
        logger.info(f"✓ Version: {__version__}")
        return True
    except ImportError as e:
        logger.error(f"✗ Import error: {e}")
        return False


def test_file_handler():
    """Test FileHandler basic functionality"""
    try:
        from mf4_operations.file_handler import FileHandler
        
        handler = FileHandler()
        logger.info("✓ FileHandler instantiated")
        
        # Test methods exist
        assert hasattr(handler, 'load_file')
        assert hasattr(handler, 'get_channels')
        assert hasattr(handler, 'get_channel_data')
        assert hasattr(handler, 'export_to_csv')
        assert hasattr(handler, 'get_file_info')
        
        logger.info("✓ FileHandler has all required methods")
        return True
    except Exception as e:
        logger.error(f"✗ FileHandler test failed: {e}")
        return False


def test_settings_manager():
    """Test SettingsManager basic functionality"""
    try:
        from mf4_operations.settings_manager import SettingsManager
        
        manager = SettingsManager()
        logger.info("✓ SettingsManager instantiated")
        
        # Test settings directory creation
        assert manager.settings_dir.exists()
        logger.info(f"✓ Settings directory: {manager.settings_dir}")
        
        # Test settings operations
        manager.set_setting('test_key', 'test_value')
        value = manager.get_setting('test_key')
        assert value == 'test_value'
        logger.info("✓ Settings read/write works")
        
        # Test history
        manager.add_to_history('test.mf4', ['channel1', 'channel2'])
        logger.info("✓ History functionality works")
        
        return True
    except Exception as e:
        logger.error(f"✗ SettingsManager test failed: {e}")
        return False


def test_plotter():
    """Test Plotter basic functionality"""
    try:
        from mf4_operations.plotter import Plotter
        
        plotter = Plotter()
        logger.info("✓ Plotter instantiated")
        
        # Test methods exist
        assert hasattr(plotter, 'plot_data')
        logger.info("✓ Plotter has all required methods")
        
        return True
    except Exception as e:
        logger.error(f"✗ Plotter test failed: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("="*50)
    logger.info("MF4 Operations - Component Tests")
    logger.info("="*50)
    
    tests = [
        ("Import Test", test_imports),
        ("FileHandler Test", test_file_handler),
        ("SettingsManager Test", test_settings_manager),
        ("Plotter Test", test_plotter),
    ]
    
    results = []
    for name, test_func in tests:
        logger.info(f"\nRunning: {name}")
        logger.info("-"*50)
        result = test_func()
        results.append((name, result))
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("Test Summary")
    logger.info("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{name}: {status}")
    
    logger.info("-"*50)
    logger.info(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n✓ All tests passed!")
        return 0
    else:
        logger.error(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
