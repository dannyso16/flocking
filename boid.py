from vec import Vec
import numpy as np
import pyxel

class Boid:
    def __init__(self):
        r1,r2,r3 = set(np.random.randint(0,100) for _ in range(3))
        self.pos = Vec(r1,r2,r3)




#====== main =======
birds = [Boid() for _ in range(10)]
np.random.randint(0,100)
for b in birds:
    print(b.pos)
