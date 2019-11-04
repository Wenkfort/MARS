class DcelHalfEdge():
    def __init__(self, vert1, vert2):
        self.vert1 = vert1
        self.vert2 = vert2
        self.next = -1
        self.twin = -1
        self.prev = -1
        self.face = -1
