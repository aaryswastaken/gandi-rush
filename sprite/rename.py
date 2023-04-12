"""
    This module is to rename all of this ...
"""

import os

# Rename 0x00A
for i in range(1, 6):
    os.rename(f"00{i}.png", f"00{i-1}.png")


# Rename 0x10A
for i in range(1, 6):
    os.rename(f"10{i}.png", f"10{i-1}.png")

# Rename 0x2AB
for i in range(0, 6):
    for j in range(0, 6):
        I = str(i-1) if i != 0 else "a"
        J = str(j-1) if j != 0 else "a"

        os.rename(f"2{i}{j}.png", f"2{I}{J}.png")
