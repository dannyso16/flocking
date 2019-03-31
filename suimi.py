# %%
from vector2 import Vector2
from random import randint
import pyxel
import math

# %%
class Fishes:
    """
    This class manages a flock of 'fish' object.

    Attributes
    ----------
    flocking_size : int
    obstacle_size : int
    _boids : List[Boid]

    Methods
    -------
    update_vel_pos()
        update all boids position and velocities
    get_positions()
        return List[boid.pos]
    get_velocitys()
        return List[boid.vel]
    get_is_obstacle()
        return List[bool]
    """

    FPS = 30
    W,H = 200, 200

    def __init__(self, flock_size:int, obstacle_size:int):
        """flock_size: number of boids
        obstacle_size: number of obstacles
        only one leader you can control
        """
        self._boids = []
        # instantiate boid
        p = Vector2(self.W//2, self.H//2)
        v = Vector2(0, 0)
        leader = FishAgent(p, v, is_obstacle=False, is_leader=True)
        self._boids.append(leader)
        for i in range(flock_size-1):
            x,y = randint(0, self.W), randint(0, self.H)
            vx,vy = randint(-10,10), randint(-10,10)
            p = Vector2(x,y)
            v = Vector2(vx,vy)
            boid = FishAgent(p, v, is_obstacle=False, is_leader=False)
            self._boids.append(boid)

        # instantiate obstacles
        for i in range(obstacle_size):
            x = randint(self.W//4, self.W*3//4)
            y = randint(self.H//4, self.H*3//4)
            p = Vector2(x,y)
            v = Vector2(0,0)
            boid = FishAgent(p, v, is_obstacle=True)
            self._boids.append(boid)

    def __repr__(self):
        ret = ""
        for boid in self._boids:
            ret += boid.__repr__() + "\n"
        return ret

    def update_vel_pos(self):
        for boid in self._boids:
            boid.update_vel(self._boids)
            boid.update_pos()

    def get_positions(self):
        ps = []
        for boid in self._boids:
            ps.append(boid.pos)
        return ps

    def get_velocitys(self):
        vs = []
        for boid in self._boids:
            vs.append(boid.vel)
        return vs

    def get_is_obstacle(self):
        isObs = []
        for boid in self._boids:
            isObs.append(boid.is_obstacle)
        return isObs

    def get_is_leader(self):
        isLead = []
        for boid in self._boids:
            isLead.append(boid.is_leader)
        return isLead



# %%
class FishAgent:
    """
    This class manages each 'fish' instance.
    'boid.py' : you cannot control the flock
    'suimi.py': you can control the leader fish.(all fishes follow him.)

    Attributes
    ----------
    pos : Vector2
        position of object
    vel : Vector2
        velocity of object
    acc : Vector2
        acceleration of object
    is_obstacle : bool, default False
        if True, treated as static object(never update position and velocity)
    is_leader : bool, default False
        if True, you can control him.

    Methods
    -------
    update_vel(List[boid])
    update_pos(List[boid])
    """

    RULE_1_COEF = 0.01  # head center of flock
    RULE_2_COEF = 1.0   # avoid obstacles
    RULE_3_COEF = 0.2   # shooling and go same direction
    FOV = 10
    MAX_SPEED = 1.2
    MIN_W, MAX_W = 7, 192
    MIN_H, MAX_H = 7, 192

    def __init__(self, pos, vel, is_obstacle=False, is_leader=False):
        self.pos = pos
        self.vel = vel
        self.acc = Vector2(0,0)
        self.is_obstacle = is_obstacle
        self.is_leader = is_leader

    def __repr__(self):
        return "<BoidAgent>:pos=({},{}),vel=({},{})".format(
                self.pos.x, self.pos.y, self.vel.x, self.vel.y)

    def update_vel(self, boids):
        VEL = .9
        if self.is_obstacle: return
        if self.is_leader:
            self.acc = Vector2(0, 0)
            if pyxel.btn(pyxel.KEY_UP):    self.acc.y -= VEL
            if pyxel.btn(pyxel.KEY_DOWN):  self.acc.y += VEL
            if pyxel.btn(pyxel.KEY_RIGHT): self.acc.x += VEL
            if pyxel.btn(pyxel.KEY_LEFT):  self.acc.x -= VEL
        else:
            vec1 = self._rule1(boids)
            vec2 = self._rule2(boids)
            vec3 = self._rule3(boids)
            # print("1:{},2:{},3:{}".format(vec1,vec2,vec3))
            self.acc = vec1 + vec2 + vec3

    def update_pos(self):
        if self.is_obstacle: return
        self.vel += self.acc
        if self.vel.magnitude > self.MAX_SPEED:
            self.vel /= self.vel.magnitude/self.MAX_SPEED
        self.pos += self.vel
        self._bounce_wall() # limit positoni in game window

    def _bounce_wall(self):
        # left and right
        if self.pos.x < self.MIN_W:
            if self.vel.x<0: self.vel.x *= -1
        elif self.pos.x > self.MAX_W:
            if self.vel.x>0: self.vel.x *= -1
        # Upper and Lower
        if self.pos.y < self.MIN_H:
            if self.vel.y<0: self.vel.y *= -1
        elif self.pos.y > self.MAX_H:
            if self.vel.y>0: self.vel.y *= -1

    def _rule1(self, boids):
        """head to the leader"""
        for boid in boids:
            if boid.is_leader:
                return (boid.pos - self.pos) * self.RULE_1_COEF
        else:
            raise AttributeError("No leader in this flock")

    def _rule2(self, boids):
        """avoid obstacles"""
        vector = Vector2(0,0)
        for boid in boids:
            if boid is self: continue
            dist = (boid.pos - self.pos).magnitude
            if dist <= self.FOV:
                vector += (self.pos - boid.pos)/dist
        return vector * self.RULE_2_COEF

    def _rule3(self, boids):
        """schoolng and go same direction with the leader"""
        for boid in boids:
            if boid.is_leader:
                return (boid.vel - self.vel) * self.RULE_3_COEF
        else:
            raise AttributeError("No leader in this flock")


# %%
