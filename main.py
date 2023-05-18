import pygame
from pygame.locals import *
from sys import exit
from math import *
import random
from Environment import Env

sprite_image_filename = 'Robot.PNG'
pygame.init()
screenWidth = 1000
screenHeight = 620
screen = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)
sprite = pygame.image.load(sprite_image_filename).convert_alpha()
clock = pygame.time.Clock()
spriteRect = sprite.get_rect()
obsDim = 50
maph = 480
mapw = 640
gray = (70, 70, 70)
white = (255, 255, 255)
blue = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

environment = Env()

while True:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # Obstacle creation
    environment.obstacles()
    # motion creation
    environment.carMotion()
    # using circles detect the collision
    environment.collisionDetectorCircles()
    # obstacle detecting circles
    environment.movement()
    # sensing the obstacle
    obstacles = environment.sense_obstacles()
    colors = screen.get_at((60, 60))
    print(obstacles)
    # updating the screen
    pygame.display.update()
