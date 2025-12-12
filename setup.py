from setuptools import setup, find_packages

setup(
    name="mf4_operations",
    version="1.0.0",
    description="Fast and lightweight MF4/MDF/DAT file converter and viewer",
    author="MF4 Operations Team",
    packages=find_packages(),
    install_requires=[
        "asammdf>=7.3.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "mf4-operations=mf4_operations.main:main",
        ],
    },
    python_requires=">=3.8",
)
