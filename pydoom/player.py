import math
import pygame
from settings import *

class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.fov = PLAYER_FOV
        self.speed = PLAYER_SPEED
        self.rotation_speed = PLAYER_ROTATION_SPEED
        self.health = 100
        self.score = 0
        self.ammo = 50
        
    def move_forward(self, map_grid):
        new_x = self.x + math.cos(self.angle) * self.speed
        new_y = self.y + math.sin(self.angle) * self.speed
        
        # 碰撞检测
        if 0 <= int(new_y) < len(map_grid) and 0 <= int(new_x) < len(map_grid[0]):
            if map_grid[int(new_y)][int(new_x)] == 0:
                self.x = new_x
                self.y = new_y
    
    def move_backward(self, map_grid):
        new_x = self.x - math.cos(self.angle) * self.speed
        new_y = self.y - math.sin(self.angle) * self.speed
        
        # 碰撞检测
        if 0 <= int(new_y) < len(map_grid) and 0 <= int(new_x) < len(map_grid[0]):
            if map_grid[int(new_y)][int(new_x)] == 0:
                self.x = new_x
                self.y = new_y
    
    def strafe_left(self, map_grid):
        new_x = self.x + math.cos(self.angle - math.pi/2) * self.speed
        new_y = self.y + math.sin(self.angle - math.pi/2) * self.speed
        
        # 碰撞检测
        if 0 <= int(new_y) < len(map_grid) and 0 <= int(new_x) < len(map_grid[0]):
            if map_grid[int(new_y)][int(new_x)] == 0:
                self.x = new_x
                self.y = new_y
    
    def strafe_right(self, map_grid):
        new_x = self.x + math.cos(self.angle + math.pi/2) * self.speed
        new_y = self.y + math.sin(self.angle + math.pi/2) * self.speed
        
        # 碰撞检测
        if 0 <= int(new_y) < len(map_grid) and 0 <= int(new_x) < len(map_grid[0]):
            if map_grid[int(new_y)][int(new_x)] == 0:
                self.x = new_x
                self.y = new_y
    
    def rotate_left(self):
        self.angle -= self.rotation_speed
    
    def rotate_right(self):
        self.angle += self.rotation_speed
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
    
    def add_ammo(self, amount):
        self.ammo += amount
    
    def add_score(self, points):
        self.score += points