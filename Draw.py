from operator import truediv
import pygame as pg
import time
import Boids
import random
import math
import numpy as np

# GLOBALS TO CHANGE

# THE SIZE OF THE BOID
BOID_SIZE = 20
# TIME STEP
TIME_STEP = 0.01

class PygameWindow():

    @staticmethod
    def draw_boid(boid : Boids.Boid, screen):
        pg.draw.circle(surface=screen,color=(255,0,0), center=(boid.x, boid.y), radius=BOID_SIZE)
        # draw a line in the direction it's looking
        scaler = BOID_SIZE * 1.25
        end_point_y = boid.y + (boid.vector[1] * scaler)
        end_point_x = boid.x + (boid.vector[0] * scaler)
        pg.draw.line(surface=screen, color=(0,0,255), start_pos=(boid.x, boid.y), end_pos=(end_point_x, end_point_y), width=5)

    @staticmethod
    def teleport_walls(boid : Boids.Boid, surface):

        if boid.x - BOID_SIZE > surface.get_size()[0]:
            boid.x = -BOID_SIZE
        elif boid.x + BOID_SIZE< 0:
            boid.x = surface.get_size()[0] + BOID_SIZE
        if boid.y - BOID_SIZE > surface.get_size()[1]:
            boid.y = -BOID_SIZE
        elif boid.y + BOID_SIZE< 0:
            boid.y = surface.get_size()[1] + BOID_SIZE

    def main_loop(self, boids):
        running = True
        while running:
            self.screen.fill((0,0,0))
            time.sleep(TIME_STEP)
            for boid in boids:
                boid.step(TIME_STEP)
                PygameWindow.teleport_walls(boid, self.screen)
                PygameWindow.draw_boid(boid, self.screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            pg.display.update()

    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption("boids")
        self.screen = pg.display.set_mode((680,800), pg.RESIZABLE)
        return 

if __name__ == "__main__":
    # setup the board
    pgWindow = PygameWindow()
    # create the boids
    boids = []
    for i in range(20):
        a = random.random()
        boids.append(Boids.Boid(f"Boid-{i}", random.randint(0,pgWindow.screen.get_size()[0]), random.randint(0,pgWindow.screen.get_size()[1]), vector=np.array([a, 1-a]), speed=175, range=200))
    # run the loop
    pgWindow.main_loop(boids);
    pass