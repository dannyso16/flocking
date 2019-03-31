# %%
from vector2 import Vector2
from random import randint
import pyxel
import math
from boid import FlockingBoid
from boid import BoidAgent

# %%
class App:
    FLOCK_SIZE    = 10
    OBSTACLE_SIZE = 1
    FPS = 30
    W,H = 200, 110

    def __init__(self):
        pyxel.init(self.W, self.H, caption="Flocking", fps=self.FPS)
        pyxel.load("asset/slime.pyxel")
        self.flock = FlockingBoid(self.FLOCK_SIZE, self.OBSTACLE_SIZE)
        # pyxel.mouse(visible=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.flock.update_vel_pos()

    def draw(self):
        pyxel.cls(3)
        self._window_frame_anim()
        poss = self.flock.get_positions()
        vels = self.flock.get_velocitys()
        isObs = self.flock.get_is_obstacle()

        # print(poss)
        for pos,vel,is_obs in zip(poss, vels, isObs):
            if is_obs: self._obstacle_anim(int(pos.x), int(pos.y))
            else:      self._slime_anim(int(pos.x), int(pos.y), vel.x)

    def _slime_anim(self, x, y, vx):
        # 4 pictures, period=6, each state durate 3 frames
        x,y = x-8,y-8
        state_duration = 3
        states = {0:0, 1:1, 2:2, 3:3, 4:2, 5:1} # transition of state
        cur = (pyxel.frame_count//state_duration) % 6
        u = states[cur]*16
        sign = -1 if vx>=0 else 1
        pyxel.blt(x=x, y=y, img=0,
                  u=u,v=0, w=sign*16, h=16, colkey=12)

    def _obstacle_anim(self, x, y):
        x,y = x-8,y-8
        state_duration = 3
        cur = (pyxel.frame_count//state_duration) % 6
        col = 7 if cur==3 else 11
        pyxel.rectb(x, y, x+16, y+16, col)
        if cur==3: pyxel.rectb(x+1, y+1, x+15, y+15, col)

    def _window_frame_anim(self):
        state_duration = 3
        offset = 0
        x1, y1 = offset, offset
        x2, y2 = self.W-1 - offset, self.H-1 - offset
        cur = (pyxel.frame_count//state_duration) % 6
        col = 7 if cur==3 else 11
        pyxel.rectb(x1, y1, x2, y2, col)
        if cur==3: pyxel.rectb(x1+1, y1+1, x2-1, y2-1, col)

# %%
App()
