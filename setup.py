#!/usr/bin/env python3
"""
Setup script for IntelSeed Python module.
"""

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import os
import subprocess
import sys
import shutil

class CustomBuildPy(build_py):
    """Custom build command to compile the C library."""
    
    def run(self):
        """Build the C library and copy it to the package."""
        # Call parent build method first to create package structure
        super().run()
        
        # The C library should already be compiled and in the package directory
        # Just verify it exists
        package_dir = "intel_seed"
        library_path = os.path.join(package_dir, "librdseed.so")
        
        if not os.path.exists(library_path):
            print(f"Warning: {library_path} not found. Make sure to compile it manually.")
        else:
            print(f"Found compiled library at {library_path}")

setup(
    name="intel-seed",
    version="1.0.0",
    description="Python module for Intel RDSEED hardware random number generation",
    author="Thiago Jung",
    author_email="thiagojm1984@hotmail.com",
    packages=find_packages(),
    package_data={
        "intel_seed": ["librdseed.so"],
    },
    include_package_data=True,
    cmdclass={"build_py": CustomBuildPy},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
    },
)
