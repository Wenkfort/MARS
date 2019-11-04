from Leaf import Leaf
import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Tree():
    def __init__(self, n, m):
        self.list_leafs = []
        self.list_leafs.append(Leaf(n, m, 0, 0))

        did_split = True
        while did_split:
            did_split = False
            list_ = []
            for vert in self.list_leafs:
                if vert.width > vert.max_size or vert.height > vert.max_size or random.random() > 0.25:
                    if vert.split():
                        list_.append(vert.lchild)
                        list_.append(vert.rchild)
                        did_split = True
                    else:
                        list_.append(vert)
                else:
                    list_.append(vert)

            self.list_leafs = list_


    def visualize(self, field_width, field_height):
        fig = plt.figure()
        ax = fig.add_subplot(111)
    
        for vertex in self.list_leafs:
            ax.add_patch(patches.Rectangle((vertex.x, vertex.y), vertex.width, vertex.height, fill=False, color="red", alpha=1.0, lw=4.0))

        plt.xlim(0, field_width)
        plt.ylim(0, field_height)

        plt.grid(True)

        print ("the end!")
        plt.show()