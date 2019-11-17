import random
from shapely.geometry import Polygon, Point


# Данный клас реализует бинарное разбиение пространства
class BinarySplitter():
    def __init__(self, width, height):
        self.polygons = []

        # polygon_1 = Polygon([(0, 0), (width // 2, 0), (width // 2, height), (0, height)])
        # polygon_2 = Polygon([(width // 2, 0), (width, 0), (width, height // 2), (width // 2, height // 2)])
        # polygon_3 = Polygon([(width // 2, height // 2), (width, height // 2), (width, height), (width // 2, height)])

        

    def add_first_polygon(self, width, height):
        self.polygons.append(Polygon([(0, 0), (width, 0), (width, height), (0, height)]))
    
    def make_bigger(self, polygon):
        points = list(polygon.exterior.coords)

        points[0] = list(points[0])
        points[1] = list(points[1])
        points[2] = list(points[2])
        points[3] = list(points[3])


        points[0][0] += -0.5
        points[0][1] += -0.5
        points[1][0] += 0.5
        points[1][1] += -0.5
        points[2][0] += 0.5
        points[2][1] += 0.5
        points[3][0] += -0.5
        points[3][1] += 0.5

        points[0] = tuple(points[0])
        points[1] = tuple(points[1])
        points[2] = tuple(points[2])
        points[3] = tuple(points[3])

        points.remove(points[-1])

        return Polygon(points)



