from Leaf import Leaf
from Tree import Tree

import numpy as np

field_width = 30
field_height = 30

def createMap(n, m):
    tree = Tree(n, m)
    tree.visualize(field_width, field_height)
    array = np.zeros((n, m), dtype=bool)
    return array


def main():
    # size of field n x m
    createMap(field_width, field_height)


if __name__ == '__main__':
  main()