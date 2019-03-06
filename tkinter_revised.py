# http://code.activestate.com/recipes/576959/
from tkinter import *
from random import randint, choice
from time import clock, sleep

# Here are various program settings.

USE_WINDOW = False  # Display program in window.
FULLSCREEN = True   # Go fullscreen when executed.

SCR_SAVER = False   # Turn screensaver mode on or off.
COME_BACK = -1      # The program can automatically "restart."
                    # if < 0: Exit program immediately
                    # if = 0: Disable exiting program
                    # if > 0: Come back after X seconds

TITLE = 'BOIDs'     # Title to show in windowed mode.
WIDTH = 800         # Width for window to display in.
HEIGHT = 600        # Height to display in window mode.

BACKGROUND = '#000' # Background color for the screen.
BOIDS = 10          # Number of boids to show in a group.

# BoidGUI and BoidAgent have settings too.

class BoidGUI(Canvas):

    # Drawing Options
    BAL_NOT_VEC = True      # Draw balls (True) or vectors (False).
    RANDOM_BACK = False     # Replace background with flashing colors?
    RANDOM_BALL = False     # Replace balls with flashing colors?
    DRAW_TARGET = True      # Show line from groups to their targets?
    # Wall Settings
    WALL_BOUNCE = False     # Bouncy wall if true; force wall if false.
    WALL_MARGIN = 50        # Pixels from edge of screen for boundary.
    WALL_FORCE = 100        # Force applied to balls outside boundary.
    # Random Parameters
    MAX_FPS = 100           # Maximum frame per second for display.
    GROUPS = 2              # Number of groups to have displayed on the GUI.
    # Target Settings
    TARGET_FORCE = 500      # Force exerted by the targets on the boid groups.
    TRIG_DIST = 100         # Distance to target where target gets changed.
    MINI_DIST = 200         # Target must be this far away when recreated.
    # Boid Settings
    MAX_SPEED = 400         # Maximum speed for boids (pixels per second).
    MAX_SIZE = 15           # Largest radius a boid is allowed to have.
    MIN_SIZE = 10           # Smallest radius a boid may be built with.
    # Color Variables
    PALETTE_MODE = True     # Palette mode if true; random mode if false.
    COLORS = '#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#FF00FF'
    PALETTE = []
    for x in range(16):
        for y in range(16):
            for z in range(16):
                color = '#{:X}{:X}{:X}'.format(x, y, z)
                PALETTE.append(color)
    # Check the settings up above for errors.
    assert MINI_DIST > TRIG_DIST, 'Targets must be set beyond trigger point.'
    assert MAX_SIZE > MIN_SIZE, 'A minimum may not be larger than maximum.'
    assert len(COLORS) > GROUPS, 'There must be more colors than groups.'

    def __init__(self, master, width, height, background, boids):
        # Initialize the Canvas object.
        cursor = 'none' if SCR_SAVER else ''
        super().__init__(master, width=width, height=height, cursor=cursor,
                         background=background, highlightthickness=0)
        self.width = width
        self.height = height
        self.background = background
        # Create colors for the balls.
        self.create_ball_palette(boids)
        # Build the boid control system.
        self.build_boids(boids)
        # Build loop for frame updating.
        self.last_time = clock()
        self.time_diff = 1 / self.MAX_FPS
        self.after(1000 // self.MAX_FPS, self.update_screen)

    def create_ball_palette(self, size):
        # The last color is not used.
        size += 1
        # Turn the colors into (R, G, B) tuples.
        colors = list(map(parse_color, self.COLORS))
        self.BALL_PALETTE = []
        for index in range(len(colors)):
            # Extract color bounds.
            lower = colors[index]
            upper = colors[(index + 1) % len(colors)]
            palette = []
            # Interpolate colors between the bounds.
            for bias in range(size):
                R, G, B = interpolate(lower, upper, bias / size)
                palette.append('#{0:02X}{1:02X}{2:02X}'.format(R, G, B))
            # Add the new palette to the choice list.
            self.BALL_PALETTE.append(palette)

    def build_boids(self, boids):
        # Build various boid simulation groups.
        self.groups = []
        for group in range(self.GROUPS):
            group = BoidGroup()
            group.palette = choice(self.BALL_PALETTE)
            self.BALL_PALETTE.remove(group.palette)
            # Create a new boid for current group.
            for boid, color in zip(range(boids), group.palette):
                # Place the boid somewhere on screen.
                x = randint(0, self.width)
                y = randint(0, self.height)
                position = Vector2(x, y)
                # Give it a random velocity (within 400).
                velocity = Polar2(randint(1, self.MAX_SPEED), randint(1, 360))
                # Create a random size for the ball.
                size = randint(self.MIN_SIZE, self.MAX_SIZE)
                assert size != 2, 'This is an oddly shaped ball.'
                # Create a boid (with a maximum speed of 400).
                boid = BoidAgent(position, velocity, size, self.MAX_SPEED)
                # Add a color attribute from COLORS list.
                if self.PALETTE_MODE:
                    boid.color = color
                else:
                    boid.color = choice(self.COLORS)
                group.add_boid(boid)
            # Add some mutators to this group.
            if self.WALL_BOUNCE:
                group.add_control(self.bounce_wall)
            else:
                group.add_control(self.force_wall)
            group.add_control(self.motivate)
            # Add a random target attribute to the group.
            x = randint(self.WALL_MARGIN, self.width - self.WALL_MARGIN)
            y = randint(self.WALL_MARGIN, self.height - self.WALL_MARGIN)
            group.target = Vector2(x, y)
            self.groups.append(group)

    def motivate(self, group, boid, seconds):
        # What direction should this boid move in?
        vector = (group.target - boid.position).unit()
        # Adjust velocity according to force and scale.
        boid.velocity += vector * self.TARGET_FORCE * seconds

    def check_target(self):
        for group in self.groups:
            # Is the center of the group within (100) pixels of target?
            if (group.center - group.target).magnitude <= self.TRIG_DIST:
                # Adjust target to be over (200) pixels away.
                while (group.center - group.target).magnitude <= self.MINI_DIST:
                    minimum = self.WALL_MARGIN
                    width = self.width - minimum
                    height = self.height - minimum
                    x = randint(minimum, width)
                    y = randint(minimum, height)
                    group.target = Vector2(x, y)
                # Change the ball colors if they are not random.
                if not self.RANDOM_BALL:
                    if self.PALETTE_MODE:
                        palette = choice(self.BALL_PALETTE)
                        self.BALL_PALETTE.remove(palette)
                        self.BALL_PALETTE.append(group.palette)
                        # Assign colors from new palette.
                        for boid, color in zip(group.boids, palette):
                            boid.color = color
                        group.palette = palette
                    else:
                        # Assign a random color from palette.
                        for boid in group.boids:
                            boid.color = choice(self.COLORS)


    def force_wall(self, group, boid, seconds):
        # Left and Right walls.
        if boid.position.x < self.WALL_MARGIN:
            boid.velocity.x += self.WALL_FORCE * seconds
        elif boid.position.x > self.width - self.WALL_FORCE:
            boid.velocity.x -= self.WALL_FORCE * seconds
        # Upper and Lower walls.
        if boid.position.y < self.WALL_MARGIN:
            boid.velocity.y += self.WALL_FORCE * seconds
        elif boid.position.y > self.height - self.WALL_FORCE:
            boid.velocity.y -= self.WALL_FORCE * seconds

        # Left and Right walls.
        if boid.position.x < self.WALL_MARGIN:
            if boid.velocity.x < 0:
                boid.velocity.x *= -1
        elif boid.position.x > self.width - self.WALL_MARGIN:
            if boid.velocity.x > 0:
                boid.velocity.x *= -1
        # Upper and Lower walls.
        if boid.position.y < self.WALL_MARGIN:
            if boid.velocity.y < 0:
                boid.velocity.y *= -1
        elif boid.position.y > self.height - self.WALL_MARGIN:
            if boid.velocity.y > 0:
                boid.velocity.y *= -1

    def update_screen(self):
        # Clear the screen.
        self.delete(ALL)
        for group in self.groups:
            # Draw the group's target if enabled.
            if self.DRAW_TARGET:
                center = group.center
                target = group.target
                self.create_line(center.x, center.y, target.x, target.y,
                                 fill=choice(self.PALETTE), width=3)
            # Draw all boids in the current group.
            for boid in group.boids:
                # Select correct fill color for drawing.
                fill = choice(self.PALETTE) if self.RANDOM_BALL else boid.color
                if self.BAL_NOT_VEC:
                    # Draw a ball (oval).
                    x1 = boid.position.x - boid.radius
                    y1 = boid.position.y - boid.radius
                    x2 = boid.position.x + boid.radius
                    y2 = boid.position.y + boid.radius
                    self.create_oval((x1, y1, x2, y2), fill=fill)
                else:
                    # Draw a direction pointer.
                    start = boid.position
                    end = boid.velocity.unit() * (boid.radius * 3) + start
                    self.create_line(start.x, start.y, end.x, end.y,
                                     fill=fill, width=3)
        # Randomize the background color if enabled.
        if self.RANDOM_BACK:
            self['background'] = choice(self.PALETTE)
        # Update all group targets as needed.
        self.check_target()
        # Run through the updating routines on the groups.
        time = clock()
        delta = time - self.last_time
        for group in self.groups:
            group.run_controls(delta)
            group.update_velocity()
            group.update_position(delta)
        self.last_time = time
        # Schedule for the next run of this method.
        plus = time + self.time_diff
        over = plus % self.time_diff
        diff = plus - time - over
        self.after(round(diff * 1000), self.update_screen)

import _tkinter # Properly set the GUI's update rate.
_tkinter.setbusywaitinterval(1000 // BoidGUI.MAX_FPS)


class BoidGroup:

    # Simple collection for managing boid agents.

    def __init__(self):
        self.__boids = []
        self.__flag = False
        self.__controls = []
        self.__good_center = False
        self.__prop_center = Vector2(0, 0)
        self.__good_vector = False
        self.__prop_vector = Vector2(0, 0)

    def add_boid(self, boid):
        self.__boids.append(boid)

    def update_velocity(self):
        assert not self.__flag, 'Position must be updated first.'
        self.__flag = True
        for boid in self.__boids:
            boid.update_velocity(self, self.__boids)
        self.__good_vector = False

    def update_position(self, seconds):
        assert self.__flag, 'Velocity must be updated first.'
        self.__flag = False
        for boid in self.__boids:
            boid.update_position(seconds)
        self.__good_center = False

    def add_control(self, control):
        self.__controls.append(control)

    def run_controls(self, seconds):
        for control in self.__controls:
            for boid in self.__boids:
                control(self, boid, seconds)

    @property
    def boids(self):
        for boid in self.__boids:
            yield boid

    @property
    def center(self):
        if self.__good_center == False:
            self.__prop_center = Vector2(0, 0)
            for boid in self.__boids:
                self.__prop_center += boid.position
            self.__prop_center /= len(self.__boids)
            self.__good_center = True
        return self.__prop_center

    @property
    def vector(self):
        if self.__good_vector == False:
            self.__prop_vector = Vector2(0, 0)
            for boid in self.__boids:
                self.__prop_vector += boid.velocity
            self.__prop_vector /= len(self.__boids)
            self.__good_vector = True
        return self.__prop_vector

################################################################################

class BoidAgent:

    # Implements all three boid rules.

    RULE_1_SCALE = 100  # Scale the clumping factor.
    RULE_2_SCALE = 3    # Scale the avoiding factor.
    RULE_2_SPACE = 1    # Avoid when inside of space.
    RULE_3_SCALE = 100  # Scale the schooling factor.

    def __init__(self, position, velocity, radius, max_speed):
        self.position = position
        self.velocity = velocity
        self.__update = Vector2(0, 0)
        self.radius = radius
        self.max_speed = max_speed

    def update_velocity(self, group, boids):
        # Filter self out of boids.
        others = [boid for boid in boids if boid is not self]
        # Run through the boid rules.
        vector_1 = self.__rule_1(others)
        # vector_1 = (group.center - self.position) / 100
        vector_2 = self.__rule_2(others)
        vector_3 = self.__rule_3(others)
        # vector_3 = (group.vector - self.velocity) / 100
        # Save the results.
        self.__update = vector_1 + vector_2 + vector_3

    def update_position(self, seconds):
        # Update to new velocity.
        self.velocity += self.__update
        # Limit the velocity as needed.
        if self.velocity.magnitude > self.max_speed:
            self.velocity /= self.velocity.magnitude / self.max_speed
        # Update our position variable.
        self.position += self.velocity * seconds

    def __rule_1(self, boids):
        # Simulate the clumping factor.
        vector = Vector2(0, 0)
        for boid in boids:
            vector += boid.position
        vector /= len(boids)
        return (vector - self.position) / self.RULE_1_SCALE

    def __rule_2(self, boids):
        # Simulate the avoiding factor.
        vector = Vector2(0, 0)
        for boid in boids:
            delta = (boid.position - self.position).magnitude
            space = (boid.radius + self.radius) * (self.RULE_2_SPACE + 1)
            if delta < space:
                vector += (self.position - boid.position)
        return vector / self.RULE_2_SCALE

    def __rule_3(self, boids):
        # Simulate the schooling factor.
        vector = Vector2(0, 0)
        weight = 0
        for boid in boids:
            r2 = boid.radius ** 2
            vector += boid.velocity * r2
            weight += r2
        vector /= len(boids) * weight
        return (vector - self.velocity) / self.RULE_3_SCALE

################################################################################

# If this code is run directly,
# run the program's entry point.
if __name__ == '__main__':
    main()
