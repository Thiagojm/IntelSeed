# IntelSeed

A Python module for Intel RDSEED hardware random number generation.

## Overview

IntelSeed provides access to Intel's RDSEED instruction for generating cryptographically secure random numbers using hardware entropy. This is particularly useful for cryptographic applications that require high-quality entropy.

## Requirements

- Intel/AMD CPU with RDSEED support (Intel Broadwell 2014+ or AMD Zen 2017+)
- Linux x86_64 or Windows x86_64
- Python 3.8+
- For building: GCC (Linux) or MinGW-w64 (Windows/Linux cross-compile)

## Installation

### Building the Shared Library

#### On Linux (for Linux .so)
1. Compile the C library:
   ```bash
   gcc -shared -fPIC -mrdseed -o librdseed.so rdseed_bytes.c
   ```
   or optimized:
   ```bash
   gcc -fPIC -mrdseed -O2 -Wall -shared -o librdseed.so rdseed_bytes.c
   ```

#### Cross-Compiling for Windows on Linux (.dll)
1. Install MinGW-w64:
   ```bash
   sudo apt update
   sudo apt install mingw-w64
   ```
2. Compile:
   ```bash
   x86_64-w64-mingw32-gcc -fPIC -mrdseed -O2 -Wall -shared -o librdseed.dll rdseed_bytes.c -Wl,--out-implib,liblibrdseed.a
   ```

#### On Windows (native .dll)
1. Install MinGW-w64 (e.g., via MSYS2 or winget: `winget install mingw`).
2. Compile:
   ```bash
   gcc -fPIC -mrdseed -O2 -Wall -shared -o librdseed.dll rdseed_bytes.c
   ```

Place the built library (`librdseed.so` or `librdseed.dll`) in the same directory as the Python module or in your system's library path.

### Installing the Python Module
```bash
pip install -e .
```
or build a wheel:
```bash
python setup.py bdist_wheel
```

## Cross-Platform Support

The IntelSeed module now supports both Linux and Windows automatically:

- **OS Detection**: In `intel_seed.py`, the `IntelSeed` class uses `platform.system()` to detect the operating system. If no `library_path` is provided, it looks for `librdseed.so` on Linux/macOS or `librdseed.dll` on Windows in the module's directory.
- **Usage**: No changes needed in your Python code—the module handles library loading transparently.
- **Fallback**: If the appropriate library is not found, it raises `RDSEEDError`. Ensure the correct library is built and placed correctly.
- **Testing**: On Windows, verify RDSEED support with tools like CPU-Z. The module tests availability during initialization.

For other platforms (e.g., macOS), build a `librdseed.dylib` and extend the detection logic if needed.

## API Reference

### Functions

- `get_bytes(n_bytes: int) -> bytes`: Generate n_bytes of raw entropy
- `get_bits(n_bits: int) -> bytes`: Generate n_bits of raw entropy (may have extra bits)
- `get_exact_bits(n_bits: int) -> bytes`: Generate exactly n_bits of raw entropy
- `is_rdseed_available(library_path: str | None = None) -> bool`: Safely check if RDSEED is available on the current CPU and library loads successfully. Returns False for unsupported CPUs but re-raises other errors (e.g., missing library).
- `random_int(low: int = 0, high: int = 1) -> int`: Generate a cryptographically secure random integer in the range [low, high] using RDSEED with rejection sampling for uniform distribution.

### Classes

- `IntelSeed`: Main class for RDSEED operations
- `RDSEEDError`: Exception raised when RDSEED operations fail

### Methods

- `IntelSeed.get_bytes(n_bytes: int) -> bytes`: Generate n_bytes of raw entropy
- `IntelSeed.get_bits(n_bits: int) -> bytes`: Generate n_bits of raw entropy
- `IntelSeed.get_exact_bits(n_bits: int) -> bytes`: Generate exactly n_bits of raw entropy
- `IntelSeed.random_int(low: int = 0, high: int = 1) -> int`: Generate a cryptographically secure random integer in the range [low, high] using RDSEED.

## Usage

### Basic Usage

```python
import intel_seed

# Generate 32 bytes of entropy
data = intel_seed.get_bytes(32)
print(f"32 bytes: {data.hex()}")

# Generate 256 bits of entropy
data = intel_seed.get_bits(256)
print(f"256 bits: {data.hex()}")

# Generate exactly 200 bits of entropy
data = intel_seed.get_exact_bits(200)
print(f"200 bits: {data.hex()}")
```

### Advanced Usage

```python
from intel_seed import IntelSeed, RDSEEDError

try:
    # Create an instance
    rdseed = IntelSeed()
    
    # Generate various amounts of entropy
    data_1_bit = rdseed.get_exact_bits(1)
    data_7_bits = rdseed.get_exact_bits(7)
    data_128_bits = rdseed.get_exact_bits(128)
    
    print(f"1 bit: {data_1_bit.hex()}")
    print(f"7 bits: {data_7_bits.hex()}")
    print(f"128 bits: {data_128_bits.hex()}")
    
except RDSEEDError as e:
    print(f"RDSEED Error: {e}")
```

### Checking RDSEED Availability

```python
from intel_seed import is_rdseed_available, RDSEEDError

# Check if RDSEED is available (fast and safe)
available = is_rdseed_available()

if available:
    print("RDSEED is supported! You can now use hardware entropy.")
    # Proceed with RDSEED operations
    from intel_seed import get_bytes
    data = get_bytes(32)
else:
    print("RDSEED not available - falling back to software RNG.")
    # Use alternative like os.urandom
    import os
    data = os.urandom(32)

# For custom library path:
# available = is_rdseed_available("/path/to/custom/librdseed.dll")
```

### Generating Random Integers

```python
from intel_seed import random_int, RDSEEDError

# Random int from 0 to 100 (inclusive)
num = random_int(0, 100)
print(f"Random 0-100: {num}")

# From 0 to 4 (e.g., 5-sided die)
die_roll = random_int(0, 4)
print(f"Die roll 0-4: {die_roll}")

# With error handling
try:
    coin_flip = random_int()  # Defaults to 0-1
    print(f"Coin flip: {coin_flip}")
except RDSEEDError as e:
    print(f"RDSEED error: {e}")
```

### Generate random numbers in a range

```python
import os
from intel_seed import random_int, is_rdseed_available, RDSEEDError

def secure_random_int(low: int = 0, high: int = 1) -> int:
    """Generate a random int [low, high], using RDSEED if available, else os.urandom fallback."""
    if is_rdseed_available():
        try:
            return random_int(low, high)
        except RDSEEDError:
            print("RDSEED failed—using fallback.")
    # Fallback implementation using os.urandom
    import math
    range_size = high - low + 1
    bits_needed = math.ceil(math.log2(range_size))
    while True:
        data = os.urandom(math.ceil(bits_needed / 8))
        value = int.from_bytes(data, 'big') >> (len(data) * 8 - bits_needed)
        if value < range_size:
            return low + value

# Examples
num_100 = secure_random_int(0, 100)
num_4 = secure_random_int(0, 4)
print(f"Secure random 0-100: {num_100}")
print(f"Secure random 0-4: {num_4}")
```

### Conditional RDSEED Usage

```python
import os
from intel_seed import is_rdseed_available, get_bytes, RDSEEDError

def generate_secure_bytes(n_bytes: int) -> bytes:
    """Generate secure random bytes, preferring RDSEED if available."""
    available = is_rdseed_available()
    if available:
        try:
            return get_bytes(n_bytes)
        except RDSEEDError:
            print("RDSEED failed - using fallback.")
    # Fallback to system RNG
    return os.urandom(n_bytes)

# Usage
data = generate_secure_bytes(32)
print(f"Secure {len(data)} bytes: {data.hex()}")
```

## Error Handling

The module raises `RDSEEDError` when:
- The RDSEED library cannot be loaded
- The CPU doesn't support RDSEED
- RDSEED operations fail

```python
from intel_seed import RDSEEDError

try:
    data = intel_seed.get_bytes(32)
except RDSEEDError as e:
    print(f"RDSEED not available: {e}")
```

## License

MIT License
