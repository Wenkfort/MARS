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
    def __init__(self, vert1, vert2):
        self.origin = vert1
        self.next = None
        self.twin = None
        self.prev = None
        self.face = None
        self.length = m.sqrt((vert2.x-vert1.x)**2 + (vert2.y-vert1.y)**2)

# универсальный класс для грани
class DcelFace():
    def __init__(self):
        self.wedge = None
        self.half_edges = []

# более узкий класс для прямоугольника
class DcelRectangle():
    def __init__(self, min_size=3, max_size=9):
        self.wedge = None
        self.half_edges = []
        self.height = None  
        self.width = None
        self.lchild = None
        self.rchild = None
        self.was_splitted = False
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

    # В этом методе будет прописана логика деления прямоугольника
    # Если прямоугольник удастся разделить, добавляется новая вершина, полуребро делится на два полуребра
    # Полуребра соседних прямогольников (полуребра-близнецы) так же делятся на два полуребра 
    def split_rectangle(self, rectangle):
        if not self.rectangles.__contains__(rectangle):
            print ("This class doesn't contain this rectangle")
            return False
        
        print("This class contain rectangle. All is Ok!")

        if rectangle.was_splitted:
            return False
        
        # выбирать направление разрезания на основе размеров
        # Если ширина больше чем в 1.25 раз больше высоты, режем вертикально
        # Если высота больше чем в 1.25 раз больше ширины, режем горизонтально
        # В остальных случаях направление разрезания случайным образом
        splitH = bool(random.getrandbits(1))
        if rectangle.width / rectangle.height > 1.25:
            splitH = True
        elif rectangle.height / rectangle.width > 1.25:
            splitH = False

        max_ = (rectangle.height if splitH else rectangle.width) - rectangle.min_size
        
        # Лист слишком маленький, чтобы его резать
        if max_ <= 2 * rectangle.min_size:
            return False 

        # линия реза исходя из размеров прямоугольника
        split = random.randint(rectangle.min_size, max_)

        splitH = True   # TODO: remove it. it`s for debugging
        if splitH:
            print ("split horizontaly")
            self.split_horizontaly(rectangle, split)
        else:
            print ("split verticaly")
            self.split_verticaly(rectangle, split)

        return False

    # TODO: удалить?
    def split_hedge_on_two(self):
        print("this method splitted hedge on two")

    def split_horizontaly(self, rectangle, split):
            # Нужно удалить 2 полуребра у разрезаемого прямоугольника и 2 полуребра близнеца, итого: 4 полуребра из списка ребер. 
            # Добивить 2 точки
            # Добавить 3 полуребра разрезаемому прямоугольнику и 4* полуребра для 2х соседних прямоугольников. 
            # Для каждого соседнего прямоуг 1 ребро заменяется на 2.
            # *ПОДУМАТЬ: если линия реза точно попала на один уровень с вершиной соседнего прямоугольника
            
            # Ищем нужные полуребра, которое необходимо разрезать
            left_hedge = None
            right_hedge = None 
            for hedge in rectangle.half_edges:
                if hedge.origin.x == hedge.next.origin.x and hedge.origin.y <= rectangle.left_down_angle_y + split <= hedge.next.origin.y:
                    # found first hedge
                    right_hedge = hedge
                if hedge.origin.x == hedge.next.origin.x and hedge.next.origin.y <= rectangle.left_down_angle_y + split <= hedge.origin.y:
                    # found second hedge
                    left_hedge = hedge
            print("hedged are founded")
            
            
            # добавляем вершины, если необходимо
            left_vert, right_vert = None, None
            # координаты вершины слева
            left_x, left_y = rectangle.left_down_angle_x, rectangle.left_down_angle_y + split
            # координаты вершины справа
            right_x, right_y = rectangle.left_down_angle_x + rectangle.width, rectangle.left_down_angle_y + split

            # проверяем, возможно, такие вершины уже существуют
            for vertex in self.vertices:
                if vertex.x == left_x and vertex.y == left_y:
                    left_vert = vertex
                if vertex.x == right_x and vertex.y == right_y:
                    right_vert = vertex

            # Добавляем, если вершины еще не существуют
            if left_vert == None:
                left_vert = DcelVertex(left_x, left_y)
                self.vertices.append(left_vert)
            
            if right_vert == None:
                right_vert = DcelVertex(right_x, right_y)
                self.vertices.append(right_vert)

            # TODO: не все зависимости прописал
            # укорачиваем левое полуребро
            # создаем новое укороченное полуребро слева, ктр будет принадлежать верхнему прямоугольнику
            hedgeV_left = DcelHalfEdge(left_hedge.origin, left_vert)
            hedgeV_left.prev = left_hedge.prev
            hedgeV_left.next = left_hedge
            left_hedge.prev = hedgeV_left
            # точка начала полуребра больше не ссылается на старое левое полуребро
            left_hedge.origin.half_edges.remove(left_hedge)
            # новой точкой начала для вершины становится left_vert
            left_hedge.origin = left_vert
            # соответственно left_vert теперь ссылается на это ребро
            left_vert.half_edges.append(left_hedge)
            self.half_edges.append(hedgeV_left)


            # укорачиваем правое полуребро
            # создаем новое укороченное полуребро справа, ктр будет принадлежать верхнему прямоугольнику
            hedgeV_right = DcelHalfEdge(right_vert, right_hedge.next.origin)
            hedgeV_right.prev = right_hedge
            hedgeV_right.next = right_hedge.next
            right_hedge.next = hedgeV_right
            # промежуточная точка теперь ссылается на новое полуребро
            right_vert.half_edges.append(hedgeV_right)
            self.half_edges.append(hedgeV_right)

            
            
            # создаем горизонтальные полуребра и делаем их близнецами
            hedgeH_down = DcelHalfEdge(right_vert, left_vert)
            hedgeH_up = DcelHalfEdge(left_vert, right_vert)
            hedgeH_down.twin = hedgeH_up
            hedgeH_up.twin = hedgeH_down

            # создаем левое и правое полуребра для верхнего прямоугольника



    def split_verticaly(self, rectangle, split):
        print("split verticaly")
        # Нужно удалить 2 полуребра у разрезаемого прямоугольника и 2 полуребра близнеца, итого: 4 полуребра из списка ребер. 
        # Добивить 2 точки
        # Добавить 4 полуребра разрезаемому прямоугольнику и 4* полуребра для 2х соседних прямоугольников. 
        # Для каждого соседнего прямоуг 1 ребро заменяется на 2.
        # *ПОДУМАТЬ: если линия реза точно попала на один уровень с вершиной соседнего прямоугольника


    def add_first_face(self, width, height):
        # добавляем 4 вершины
        vertices_ = []
        vertices_.append(DcelVertex(0, 0))
        vertices_.append(DcelVertex(width, 0))
        vertices_.append(DcelVertex(width, height))    
        vertices_.append(DcelVertex(0, height))

        # добавляем 4 полуребра
        half_edges_list = []
        half_edges_list.append(DcelHalfEdge(vertices_[0], vertices_[1]))
        half_edges_list.append(DcelHalfEdge(vertices_[1], vertices_[2]))
        half_edges_list.append(DcelHalfEdge(vertices_[2], vertices_[3]))
        half_edges_list.append(DcelHalfEdge(vertices_[3], vertices_[0]))

        # добавляем вершинам ссылки на ребра, которые выходят из этой вершины
        vertices_[0].half_edges.append(half_edges_list[0])
        vertices_[1].half_edges.append(half_edges_list[1])
        vertices_[2].half_edges.append(half_edges_list[2])
        vertices_[3].half_edges.append(half_edges_list[3])

        # добавляем каждому полуребру ссылки на следующие полуребра
        half_edges_list[0].next = half_edges_list[1]
        half_edges_list[1].next = half_edges_list[2]
        half_edges_list[2].next = half_edges_list[3]
        half_edges_list[3].next = half_edges_list[0]

        # добавляем каждому полуребру ссылки на предыдущие полуребра
        half_edges_list[0].prev = half_edges_list[3]
        half_edges_list[1].prev = half_edges_list[0]
        half_edges_list[2].prev = half_edges_list[1]
        half_edges_list[3].prev = half_edges_list[2]

        # создаем грань
        rectangle = DcelRectangle()

        # грани добавляем ссылки на полуребра
        rectangle.half_edges = half_edges_list
        # добавляем размеры прямоугольника
        rectangle.width = width
        rectangle.height = height

        # добавляем каждому ребру ссылку на грань
        half_edges_list[0].face = rectangle
        half_edges_list[1].face = rectangle
        half_edges_list[2].face = rectangle
        half_edges_list[3].face = rectangle

        rectangle.find_coordinates()

        # заносим всё это добро в основные списки
        self.vertices += vertices_
        self.half_edges += half_edges_list
        self.rectangles.append(rectangle)

        print ("stop")

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