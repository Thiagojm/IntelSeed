from intel_seed import random_int, RDSEEDError

# Basic call: Generate a random int from 0 to 100
num = random_int(0, 10000)
print(f"Random number (0-10000): {num}")

# From 0 to 4 (e.g., for a 5-sided die)
die_roll = random_int(0, 4)
print(f"Die roll (0-4): {die_roll}")

# Custom range: Negative numbers or large ranges work too
large_num = random_int(-50, 50)
print(f"Random in [-50, 50]: {large_num}")

# Defaults: 0 or 1 (like a coin flip)
coin = random_int()
print(f"Coin flip: {coin}")  # 0 (tails) or 1 (heads)