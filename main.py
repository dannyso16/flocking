import numpy as np
from boid import Boid
import pyxel

class FlockingAnim:
    def __init__(self):
        pyxel.init(200, 100, caption="Flocking Animation", fps=30)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)

FlockingAnim()
