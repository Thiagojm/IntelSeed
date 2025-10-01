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
import platform

class CustomBuildPy(build_py):
    """Custom build command to compile the C library."""
    
    def run(self):
        """Build the C library and copy it to the package."""
        # Call parent build method first to create package structure
        super().run()
        
        # Compile the C library if source exists
        c_source = os.path.join('intel_seed', 'rdseed_bytes.c')
        if not os.path.exists(c_source):
            print(f"Warning: {c_source} not found. Cannot compile library.")
            return
        
        package_dir = os.path.join(self.build_lib, "intel_seed")
        os.makedirs(package_dir, exist_ok=True)
        
        system = platform.system()
        if system == "Windows":
            lib_name = "librdseed.dll"
            # Assume MinGW or MSVC; use gcc if available
            try:
                subprocess.check_call([
                    "gcc", "-shared", "-mrdseed", "-O2", "-Wall", 
                    "-o", os.path.join(package_dir, lib_name), c_source
                ], shell=True)
                print(f"Compiled {lib_name} for Windows.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to compile {lib_name}: {e}. Install MinGW-w64 and retry.")
        elif system == "Linux":
            lib_name = "librdseed.so"
            try:
                subprocess.check_call([
                    "gcc", "-shared", "-fPIC", "-mrdseed", "-O2", "-Wall", 
                    "-o", os.path.join(package_dir, lib_name), c_source
                ])
                print(f"Compiled {lib_name} for Linux.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to compile {lib_name}: {e}. Install gcc and retry.")
        else:
            print(f"Unsupported platform {system}. Compile {c_source} manually.")
        
        # Copy if already exists in source dir (fallback)
        for lib in ["librdseed.so", "librdseed.dll"]:
            src_lib = os.path.join("intel_seed", lib)
            if os.path.exists(src_lib):
                dst_lib = os.path.join(package_dir, lib)
                shutil.copy2(src_lib, dst_lib)
                print(f"Copied existing {lib}.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="intelseed",
    version="1.1.0",
    description="Python module for Intel RDSEED hardware random number generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Thiago Jung",
    author_email="tjm.plastica@gmail.com",
    packages=find_packages(),
    package_data={
        "intel_seed": ["*.so", "*.dll", "*.c"],
    },
    include_package_data=True,
    cmdclass={"build_py": CustomBuildPy},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=[],
)
