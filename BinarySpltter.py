import random

from DCEL import Dcel

# Данный клас реализует бинарное разбиение пространства
class BinarySplitter():
    def __init__(self, width, height):
        dcel = Dcel()
        dcel.add_first_face(width, height)

        did_split = True
        while did_split:
            did_split = False

            rectanles_copy = list(dcel.rectangles)
            # пробежать по каждому прямоугольнику в пространстве и попробовать разрезать
            # если хотя бы раз разрезали, ещё раз
            for rectangle in rectanles_copy:
                if rectangle.width > rectangle.max_size or rectangle.height > rectangle.max_size or random.random() > 0.25:
                    if dcel.split_rectangle(rectangle):
                        did_split = True
                

        print ("stop")


