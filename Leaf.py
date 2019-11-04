import random

class Leaf():
    def __init__(self, width, height, x, y, min_size=3, max_size=6):
        # each space has a ccordinate of first point - (x, y)
        # and size of the field (n, m)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.centre_x_lf, self.centre_y_lf = self.get_centre()
        self.centre_x_wf, self.centre_y_wf = self.get_x_y_of_centre()

        self.min_size = min_size
        self.max_size = max_size

        self.was_splitted = False

    def split(self):
        # мы уже его разрезали! прекращаем!
        if self.was_splitted:
            return False

        #  определяем направление разрезания
            #  если ширина более чем на 25% больше высоты, то разрезаем вертикально
            #  если высота более чем на 25% больше ширины, то разрезаем горизонтально
            #  иначе выбираем направление разрезания случайным образом

        splitH = bool(random.getrandbits(1))
        if self.width > self.height and (self.width / self.height) >= 1.25:
            splitH = False
        elif self.height > self.width and (self.height / self.width) >= 1.25:
            splitH = True

        max_ = (self.height if splitH else self.width) - self.min_size
        if max_ <= 2*self.min_size:
            return False 

        split = random.randint(self.min_size, max_)

        if splitH:
            self.lchild, self.rchild = Leaf(self.width, split, self.x, self.y), Leaf(self.width, self.height - split, self.x, self.y + split)
            self.was_splitted = True
            return True
        else:
            self.lchild, self.rchild = Leaf(split, self.height, self.x, self.y), Leaf(self.width - split, self.height, self.x + split, self.y)
            self.was_splitted = True
            return True

    def get_centre(self):
        return self.width // 2, self.height // 2
  
    def get_x_y_of_centre(self):
        return self.x + self.width // 2, self.y + self.height // 2
