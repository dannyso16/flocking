from math import sin,cos

def Polar2(magnitude, degrees):
    x = magnitude * sin(radians(degrees))
    y = magnitude * cos(radians(degrees))
    return Vector2(x, y)
