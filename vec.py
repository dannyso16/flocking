import numpy as np

class Vec:
    """ Vector dim=3
    if use 2d vector, you can set like 'Vec(5, 6)'
    NOTE: <Vec> is always treated as dim=3, like 'Vec(5, 6, 0)'
    Vector calss implementation without numpy: http://www.shido.info/py/python9.html
    """
    def __init__(self, x, y, z=0):
        self.v = np.array([x,y,z])
        self.x = self.v[0]
        self.y = self.v[1]
        self.z = self.v[2]
        # print(self.v)

    def __add__(self, a):
        """a: int,float, Vector
        Vec(1,2,3) + Vec(1,2,3) = Vec(2,4,6)
        """
        if isinstance(a, int) or isinstance(a, float):
            return self.v + a
        elif isinstance(a, Vector):
            return self.v + a.v
        else:
            raise ValueError("(Vec + {}) cannot defined.".format(type(a)))

    __radd__ = __add__

    def __sub__(self, a):
        return self.__add__(-a)

    __rsub__ = __sub__


    def __mul__(self, a):
        """a: int,float, Vector
        Vec(1,2,3) * Vec(1,2,3) = Vec(1,4,9)
        """
        if isinstance(a, int) or isinstance(a, float):
            return self.v * a
        elif isinstance(a, Vector):
            return self.v * a.v
        else:
            raise ValueError("(Vec * {}) cannot defined.".format(type(a)))

    __rmul__ = __mul__

    def __neg__(self):
        return self.__mul__(-1)

    def __pos__(self):
        return copy.copy(self)

    def __abs__(self):
        return np.abs(self.v)

    def __len__(self):
        return len(self.v)


    def __repr__(self):
        """print(Vector object)-> show dim and elem"""
        return  "<class 'Vec'>: dim={}, {}".format(len(self.v), self.v)

    __str__ = __repr__
