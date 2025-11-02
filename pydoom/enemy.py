import math
import random
from settings import *
import pygame

class Enemy:
    def __init__(self, x, y, enemy_type=0):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.health = ENEMY_HEALTH
        self.speed = ENEMY_SPEED
        self.damage = ENEMY_DAMAGE
        self.attack_range = ENEMY_ATTACK_RANGE
        self.attack_cooldown = 0
        self.max_attack_cooldown = ENEMY_ATTACK_COOLDOWN
        self.state = "idle"  # idle, chase, attack
        self.detection_range = 5
        self.last_player_x = 0
        self.last_player_y = 0
        
        # 初始化游荡方向
        self.wander_direction = random.uniform(0, 2 * math.pi)
        
        # 创建敌人纹理
        self.texture = self.create_texture()
    
    def create_texture(self):
        texture = pygame.Surface((64, 64), pygame.SRCALPHA)
        
        if self.type == 0:  # 普通敌人
            color = (255, 0, 0)
        elif self.type == 1:  # 快速敌人
            color = (255, 100, 100)
            self.speed *= 1.5
        else:  # 强力敌人
            color = (150, 0, 0)
            self.health *= 1.5
            self.damage *= 1.5
        
        # 绘制敌人
        pygame.draw.circle(texture, color, (32, 32), 25)
        pygame.draw.circle(texture, (255, 255, 255), (20, 20), 8)
        pygame.draw.circle(texture, (255, 255, 255), (44, 20), 8)
        pygame.draw.circle(texture, (0, 0, 0), (20, 20), 4)
        pygame.draw.circle(texture, (0, 0, 0), (44, 20), 4)
        
        return texture
    
    def update(self, player, map_grid):
        # 更新攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # 计算到玩家的距离
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 状态机
        if distance <= self.attack_range:
            self.state = "attack"
            self.attack(player)
        elif distance <= self.detection_range and self.has_line_of_sight(player, map_grid):
            self.state = "chase"
            self.chase_player(player, map_grid)
            self.last_player_x = player.x
            self.last_player_y = player.y
        else:
            self.state = "idle"
            self.wander(map_grid)
    
    def has_line_of_sight(self, player, map_grid):
        # 简单的视线检查 - 使用DDA算法
        ray_x, ray_y = self.x, self.y
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return True
            
        step_x = dx / distance * 0.1
        step_y = dy / distance * 0.1
        
        steps = int(distance / 0.1)
        
        for _ in range(steps):
            ray_x += step_x
            ray_y += step_y
            
            # 检查是否击中墙壁
            if (0 <= int(ray_y) < len(map_grid) and 
                0 <= int(ray_x) < len(map_grid[0]) and 
                map_grid[int(ray_y)][int(ray_x)] == 1):
                return False
        
        return True
    
    def chase_player(self, player, map_grid):
        # 计算到玩家的方向
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # 归一化方向向量
            dx /= distance
            dy /= distance
            
            # 尝试移动
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            
            # 碰撞检测
            if (0 <= int(new_y) < len(map_grid) and 
                0 <= int(new_x) < len(map_grid[0]) and 
                map_grid[int(new_y)][int(new_x)] == 0):
                self.x = new_x
                self.y = new_y
    
    def wander(self, map_grid):
        # 随机游荡
        if random.random() < 0.02:  # 2%的几率改变方向
            self.wander_direction = random.uniform(0, 2 * math.pi)
        
        new_x = self.x + math.cos(self.wander_direction) * self.speed * 0.5
        new_y = self.y + math.sin(self.wander_direction) * self.speed * 0.5
        
        # 碰撞检测
        if (0 <= int(new_y) < len(map_grid) and 
            0 <= int(new_x) < len(map_grid[0]) and 
            map_grid[int(new_y)][int(new_x)] == 0):
            self.x = new_x
            self.y = new_y
        else:
            # 如果撞墙，改变方向
            self.wander_direction = random.uniform(0, 2 * math.pi)
    
    def attack(self, player):
        if self.attack_cooldown <= 0:
            player.take_damage(self.damage)
            self.attack_cooldown = self.max_attack_cooldown
    
    def take_damage(self, amount):
        self.health -= amount
    
    def is_alive(self):
        return self.health > 0