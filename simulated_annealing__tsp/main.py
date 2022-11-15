from anneal import simulate
from functions import read_file

def main():
    coords = read_file("coord_1.txt") 
    simulate(coords, stopping_iter=5000)

if __name__ == "__main__":
    main()