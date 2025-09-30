"""
IntelSeed: Python module for Intel RDSEED hardware random number generation.

This module provides access to Intel's RDSEED instruction for generating
cryptographically secure random numbers using hardware entropy.
"""

from .intel_seed import (
    IntelSeed,
    RDSEEDError,
    get_rdseed,
    get_bytes,
    get_bits,
    get_exact_bits,
    is_rdseed_available,
    random_int,
)

__version__ = "1.0.0"
__author__ = "Thiago Jung"
__email__ = "thiagojm1984@hotmail.com"

__all__ = [
    "IntelSeed",
    "RDSEEDError", 
    "get_rdseed",
    "get_bytes",
    "get_bits",
    "get_exact_bits",
    "is_rdseed_available",
    "random_int",
]
