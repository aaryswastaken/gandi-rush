import os

for i in range(6):
    for j in range(6):
        I = str(i) if i != 5 else "a"
        J = str(j) if j != 5 else "a"

        os.rename(f"sprite/2{I}{J}.png", f"sprite/temp_2{J}{I}.png")

for i in range(6):
    for j in range(6):
        I = str(i) if i != 5 else "a"
        J = str(j) if j != 5 else "a"

        os.rename(f"sprite/temp_2{I}{J}.png", f"sprite/2{I}{J}.png")
