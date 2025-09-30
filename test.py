import intel_seed
import csv
from datetime import datetime
from bitstring import BitArray
import time

duration = 3600
size = 2048
file_name = "random_data.bin"
ones_file_name = "ones_data.csv"

for i in range(duration):
    chunk = intel_seed.get_bits(size)
     # Count ones and write to CSV
    bit_array = BitArray(chunk)
    ones_count = bit_array.count(1)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    try:
        with open(ones_file_name, 'a', newline='') as f:
            csv.writer(f).writerow([timestamp, ones_count])
    except (OSError, IOError) as e:
        raise RuntimeError(f"Failed to write CSV count: {e}")
    with open(file_name, "ab") as f:
        f.write(chunk)
    print(f"Sample {i} - Number of ones: {ones_count}")
    time.sleep(1)
    
print(f"Random data saved to {file_name}")
print(f"Ones data saved to {ones_file_name}")