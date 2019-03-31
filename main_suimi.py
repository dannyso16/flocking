# %%
from vector2 import Vector2
from random import randint
import pyxel
import math
from suimi import Fishes
from suimi import FishAgent

# %%
class App:
    FLOCK_SIZE = 30
    FPS = 30
    W,H = 200, 110

    def __init__(self):
        pyxel.init(self.W, self.H, caption="Suimi-", fps=self.FPS)
        pyxel.load("asset/fish.pyxel")
        self.flock = Fishes(self.FLOCK_SIZE, obstacle_size=0)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.flock.update_vel_pos()

    def draw(self):
        pyxel.cls(12)
        # self._window_frame_anim()
        poss = self.flock.get_positions()
        vels = self.flock.get_velocitys()
        isLead = self.flock.get_is_leader()

        # print(poss)
        self._backgnd_anim()
        for pos,vel,is_leader in zip(poss, vels, isLead):
            self._fish_anim(int(pos.x), int(pos.y), vel.x, is_leader)

    def _fish_anim(self, x, y, vx, is_leader=False):
        # 4 pictures, period=6, each state durate 3 frames
        # x,y = x-8,y-8
        # state_duration = 3
        # states = {0:0, 1:1, 2:2, 3:3, 4:2, 5:1} # transition of state
        # cur = (pyxel.frame_count//state_duration) % 6
        # u = states[cur]*16
        f = (pyxel.frame_count//10)%2
        sign = -1 if vx>=0 else 1
        if is_leader:
            pyxel.blt(x=x, y=y, img=0,
                      u=f*16,v=8, w=sign*12, h=6, colkey=12)
        else:
            pyxel.blt(x=x, y=y, img=0,
                      u=f*16,v=0, w=sign*12, h=6, colkey=12)

    def _backgnd_anim(self):
        # ground
        for i in range(5):
            pyxel.blt(x=i*48, y=self.H-8, img=0,
                          u=0,v=16, w=48, h=8, colkey=12)

        # wakame
        f = (pyxel.frame_count//10)%2
        for xi in [0, 30, 60, 90, 120, 150, 180]:
            pyxel.blt(x=xi, y=self.H-16, img=0,
                    u=f*8, v=24, w=8, h=16, colkey=12)

        # bubble
        init_pos = [(100, 100), (50, 200),(160, 10)]
        for xi,yi in init_pos:
            yi = self.H - (yi+pyxel.frame_count//9)%self.H
            pyxel.blt(x=xi, y=yi, img=0,
                    u=32+f*8, v=0, w=8, h=8, colkey=12)

# %%
App()
