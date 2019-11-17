import numpy as np

from BinarySpltter import BinarySplitter


field_width = 30
field_height = 30

def createMap(n, m):
    binary_splitting = BinarySplitter(n, m)
    array = np.zeros((n, m), dtype=bool)
    return array


def main():
    # size of field n x m
    createMap(field_width, field_height)
    

if __name__ == '__main__':
  main()