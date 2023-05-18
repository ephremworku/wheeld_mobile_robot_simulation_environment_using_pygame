import pygame
import pygame
from pygame.locals import *
from sys import exit
# from gameobjects.vector2 import Vector2
from math import *
import numpy as np
import math
import random


def uncertainty_add(distance, angle, sigma):
    mean = np.array([distance, angle])
    covariance = np.diag(sigma ** 2)
    distance, angle = np.random.multivariate_normal(mean, covariance)
    distance = max(distance, 0)
    angle = max(angle, 0)
    return [distance, angle]

class Env:
    def __init__(self):

        # self.circlePos = []
        sprite_image_filename = 'Robot.PNG'
        pygame.init()

        self.screenWidth = 1000
        self.screenHeight = 620
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), 0, 32)
        self.sprite = pygame.image.load(sprite_image_filename).convert_alpha()
        self.clock = pygame.time.Clock()
        self.spriteRect = self.sprite.get_rect()
        self.obsDim = 50

        self.maph = 480
        self.mapw = 640
        self.gray = (70, 70, 70)
        self.white = (255, 255, 255)
        self.white2 = (200, 200, 200)
        self.blue = (0, 255, 0)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)

        self.sprite_pos = [self.screenWidth / 2, self.screenHeight]
        self.destination = (150, 10)
        self.startPosition = [self.screenWidth / 2, self.screenHeight - 20]
        self.sprite_speed = 300
        self.sprite_rotation = 0.
        self.sprite_rotation_speed = 100.
        self.rectangles = []
        self.wid, self.hei = (61, 70)
        self.rectangleFourCoordinates = []
        self.RectStartPos = (self.startPosition[0], self.startPosition[1])

        self.j = 0
        uncertanity = (0.5, 0.01)

        self.Range = 100
        self.speed = 4
        self.sigma = np.array([uncertanity[0], uncertanity[1]])
        self.position = (0, 0)
        self.count = 0
        self.W, self.H = pygame.display.get_surface().get_size()
        self.sensedObstacle = []

    # start and goal circles
    def circles(self, screen1, color, posision, radius, width):
        pygame.draw.circle(screen1, color, posision, radius, width)

    # draw obstacles
    def obstacles(self):
        # upperCornerx = int(random.uniform(0, mapw - obsDim))
        # upperCornery = int(random.uniform(0, maph - obsDim))
        upperCornerXY = ((50, 50), (30, 150), (550, 175), (100, 250), (250, 50), (250, 575), (350, 165),
                         (540, 150), (450, 50), (750, 650), (750, 350), (850, 550), (650, 50), (850, 666),
                         (503, 456))

        for i in upperCornerXY:
            upper = i
            rectangle = pygame.Rect(upper, (self.obsDim, self.obsDim))
            if self.j < 20:
                self.j += 1
                self.rectangleFourCoordinates.append((upper[0], upper[1]))
                self.rectangleFourCoordinates.append((upper[0] + self.obsDim, upper[1]))
                self.rectangleFourCoordinates.append((upper[0], upper[1] + self.obsDim))
                self.rectangleFourCoordinates.append((upper[0] + self.obsDim, upper[1] + self.obsDim))
            self.rectangles.append(rectangle)
            pygame.draw.rect(self.screen, self.gray, rectangle)
            # print(self.rectangleFourCoordinates)

            # goal and destination point
            self.circles(self.screen, self.blue, self.destination, 20, 2)
            self.circles(self.screen, self.blue, self.startPosition, 10, 0)
            self.circles(self.screen, self.red, self.destination, 10, 0)
            self.circles(self.screen, self.blue, self.startPosition, 20, 2)

    # collision detaction circles
    def collisionDetectorCircles(self):
        pygame.draw.circle(self.screen, self.blue, self.sprite_pos, 60, 1)
        for iter in self.rectangleFourCoordinates:
            # print(iter)
            if sqrt((iter[0] - self.sprite_pos[0]) ** 2 + (iter[1] - self.sprite_pos[1]) ** 2) < 60:
                print(iter)

                self.sprite_pos = [self.screenWidth / 2, self.screenHeight]

    # car motion including the tilting and heading motion
    def carMotion(self):
        # Car Motion
        pressed_keys = pygame.key.get_pressed()
        rotation_direction = 0.
        movement_direction = 0.
        if pressed_keys[K_LEFT]:
            rotation_direction = +1.0
        if pressed_keys[K_RIGHT]:
            rotation_direction = -1.0
        if pressed_keys[K_UP]:
            movement_direction = -1.0
        if pressed_keys[K_DOWN]:
            movement_direction = +1.0
        rotated_sprite = pygame.transform.rotate(self.sprite, self.sprite_rotation)
        # box_rotation = pygame.transform.rotate(box, sprite_rotation)

        rot = rotated_sprite.get_rect()
        # print(sprite_rotation)

        w, h = rotated_sprite.get_size()
        wid, hei = w, h
        # print(w, h)
        # print(int(self.sprite_pos[0]), int(self.sprite_pos[1]))
        sprite_draw_pos = (self.sprite_pos[0] - w / 2, self.sprite_pos[1] - h / 2)
        self.screen.blit(rotated_sprite, sprite_draw_pos)
        time_passed = self.clock.tick()
        time_passed_seconds = time_passed / 1000.0
        self.sprite_rotation += rotation_direction * self.sprite_rotation_speed * time_passed_seconds
        heading_x = sin(self.sprite_rotation * 2 * pi / 180.0)
        heading_y = cos(self.sprite_rotation * 2 * pi / 180.0)
        heading = [heading_x, heading_y]
        heading[0] *= movement_direction
        heading[1] *= movement_direction
        self.sprite_pos[0] += heading[0] * self.sprite_speed * time_passed_seconds
        self.sprite_pos[1] += heading[1] * self.sprite_speed * time_passed_seconds

    # obstacle distance measuring circle
    def obstacleDistanceMeasuringCircle(self):
        circlePos = []
        m = 0
        pygame.draw.circle(self.screen, self.blue, self.sprite_pos, 100, 1)
        # for iter in self.rectangleFourCoordinates:
        # print(iter)
        # if sqrt((iter[0] - self.sprite_pos[0]) ** 2 + (iter[1] - self.sprite_pos[1]) ** 2) < 100:
        # print(sqrt((iter[0] - self.sprite_pos[0]) ** 2 + (iter[1] - self.sprite_pos[1]) ** 2))

        for i in range(36):
            px = 100 * cos(i * (10 * pi / 180))
            py = 100 * sin(i * (10 * pi / 180))
            position = (self.sprite_pos[0] + px, self.sprite_pos[1] + py)
            circlePos.append(position)
            pygame.draw.circle(self.screen, self.white2, position, 2)
            if i == 33:
                pygame.draw.circle(self.screen, self.red, position, 5)
            else:
                pygame.draw.circle(self.screen, self.black, position, 2)

        # print(circlePos[5])

        detectPoint = []
        episoideDetectPoint = []
        quadrant = 0

        for iter in self.rectangleFourCoordinates:
            m = 0
            for j in circlePos:
                m += 1
                if  abs(iter[0] - j[0]) <= 5 and abs(iter[1] - j[1]) <= 5:
                    # m = circlePos.index(j)
                    if 0 <= m <= 9:
                        quadrant = 4
                        print("in quadrant 4 point: ", m, "collied")
                    if 9 <= m <= 18:
                        quadrant = 3
                        print("in quadrant 3 point: ", m, "collied")
                    if 18 <= m <= 27:
                        quadrant = 2
                        print("in quadrant 2 point: ", m, "collied")
                    if 27 <= m <= 36:
                        quadrant = 1
                        print("in quadrant 1 point: ", m, "collied")

                    detectPoint.append(m)


            episoideDetectPoint.append(detectPoint)
        return detectPoint

    def movement(self):
        pressed_keys = pygame.key.get_pressed()
        colliedPoints = None
        if pressed_keys[K_LEFT]:
            colliedPoints = self.obstacleDistanceMeasuringCircle()
            print(colliedPoints)
        if pressed_keys[K_RIGHT]:
            colliedPoints = self.obstacleDistanceMeasuringCircle()
            print(colliedPoints)
        if pressed_keys[K_UP]:
            colliedPoints = self.obstacleDistanceMeasuringCircle()
            print(colliedPoints)
        if pressed_keys[K_DOWN]:
            colliedPoints = self.obstacleDistanceMeasuringCircle()
            print(colliedPoints)

        # print(episoideDetectPoint)
        # print(iter)
        # if sqrt((iter[0] - self.sprite_pos[0]) ** 2 + (iter[1] - self.sprite_pos[1]) ** 2) < 60:
        #     print(iter)






    def distance(self, obstaclePosition):
        px = (obstaclePosition[0] - self.position[0]) ** 2
        py = (obstaclePosition[1] - self.position[1]) ** 2
        return math.sqrt(px + py)

    def sense_obstacles(self):
        self.count = 0
        index = []
        x, y = 0, 0
        new_distances = []
        scen = []
        data = []
        angles = []
        self.position = self.sprite_pos
        x1, y1 = self.position[0], self.position[1]
        for angle in np.linspace(0, 2 * math.pi, 60, False):
            counter = 0
            x2, y2 = (x1 + self.Range * math.cos(angle), y1 - self.Range * math.sin(angle))
            for i in range(0, 100):
                u = i / 100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                if 0 < x < self.W and 0 < y < self.H:
                    color = self.screen.get_at((x, y))
                    if (color[0], color[1], color[2]) == self.gray:
                        distance = self.distance((x, y))
                        angles.append(int(angle*180/math.pi))
                        # print(distance)
                        output = uncertainty_add(distance, angle, self.sigma)
                        new_distances.append(output[0])
                        index.append(self.count)
                        output.append(self.position)
                        # store the measurements
                        data.append(output)
                        break
            self.count += 1

        for x in range(60):
            for i in index:
                if x == i:
                    scen.append(new_distances)
                else:
                    scen.append(0)


        # print('distances: ', scen)
        # print('index: ', index)
        # print('angles: ', angles)
        if len(data) > 0:
            return scen, angles, index
        else:
            return False
