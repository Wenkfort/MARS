import math as m
import random

import matplotlib.pyplot as plt

# в этом файле классы для работы с представлением геометрических фигур в виде двусвязного списка рёбер
class DcelVertex():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.half_edges = []

class DcelHalfEdge():
    def __init__(self, vert1):
        self.origin = vert1
        self.next = None
        self.twin = None
        self.prev = None
        self.face = None

# универсальный класс для грани
class DcelFace():
    def __init__(self):
        self.wedge = None
        self.half_edges = []

# более узкий класс для прямоугольника
class DcelRectangle():
    def __init__(self, min_size=3, max_size=9):
        self.half_edges = []
        self.height = None  
        self.width = None
        self.lchild = None
        self.rchild = None
        self.min_size = min_size
        self.max_size = max_size
        self.left_down_angle_x, self.left_down_angle_y = None, None

    # находим координаты левого нижнего угла прямоугольника
    def find_coordinates(self):
        min_x = float("inf")
        min_y = float("inf")
        for hedge in self.half_edges:
            if min_x > hedge.origin.x:
                min_x = hedge.origin.x
            if min_y > hedge.origin.y:
                min_y = hedge.origin.y

        self.left_down_angle_x = min_x
        self.left_down_angle_y = min_y

    

# в данном классе хранится список полуребер, вершин, прямоуголников
class Dcel():
    def __init__(self):
        self.half_edges = []
        self.vertices = []
        self.rectangles = []

    

    def visualize(self, field_width, field_height):
        fig = plt.figure()
        ax = plt.axes()

        plt.xlim(0, field_width)
        plt.ylim(0, field_height)

        for hedge in self.half_edges:
            plt.plot([hedge.origin.x, hedge.next.origin.x], [hedge.origin.y, hedge.next.origin.y])

        plt.grid(True)

        plt.show()
        print ("the end of visualizing!")