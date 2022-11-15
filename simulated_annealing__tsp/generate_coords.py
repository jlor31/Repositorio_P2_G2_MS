# Generate random coordinates
import numpy as np

RANGE = (-100, 100)
N = 100

coords = np.random.randint(RANGE[0], RANGE[1], size=(N, 2))

with open("coord_1.txt", "w") as f:
    for coord in coords:
        f.write(f"{coord[0]} {coord[1]}\n")


