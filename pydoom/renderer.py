import pygame
import math
import random
from settings import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 24)
        
        # 创建纹理
        self.wall_textures = self.create_wall_textures()
        self.sky_texture = self.create_sky_texture()
        self.floor_texture = self.create_floor_texture()
    
    def create_wall_textures(self):
        textures = []
        
        # 创建几种不同的墙壁纹理
        for i in range(4):
            texture = pygame.Surface((64, 64))
            
            if i == 0:  # 石墙
                color = (150, 150, 150)
                for y in range(0, 64, 8):
                    for x in range(0, 64, 8):
                        shade = 20 if (x//8 + y//8) % 2 == 0 else 0
                        pygame.draw.rect(texture, 
                                        (color[0]-shade, color[1]-shade, color[2]-shade), 
                                        (x, y, 8, 8))
            
            elif i == 1:  # 砖墙
                color = (180, 100, 80)
                for y in range(0, 64, 16):
                    for x in range(0, 64, 32):
                        pygame.draw.rect(texture, color, (x, y, 30, 14))
                        pygame.draw.line(texture, (100, 50, 40), (x, y+14), (x+30, y+14), 2)
            
            elif i == 2:  # 金属墙
                color = (120, 120, 140)
                for y in range(0, 64, 16):
                    for x in range(0, 64, 16):
                        pygame.draw.rect(texture, color, (x, y, 14, 14))
                        pygame.draw.rect(texture, (80, 80, 100), (x, y, 14, 14), 1)
            
            else:  # 木墙
                color = (150, 120, 90)
                for y in range(0, 64, 16):
                    pygame.draw.rect(texture, color, (0, y, 64, 14))
                    pygame.draw.line(texture, (100, 80, 60), (0, y+14), (64, y+14), 2)
            
            textures.append(texture)
        
        return textures
    
    def create_sky_texture(self):
        texture = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        
        # 创建渐变天空
        for y in range(SCREEN_HEIGHT // 2):
            # 从深蓝到浅蓝的渐变
            blue = 100 + int(155 * y / (SCREEN_HEIGHT // 2))
            pygame.draw.line(texture, (50, 50, blue), (0, y), (SCREEN_WIDTH, y))
        
        # 添加一些星星
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 4)
            pygame.draw.circle(texture, (255, 255, 255), (x, y), 1)
        
        return texture
    
    def create_floor_texture(self):
        texture = pygame.Surface((64, 64))
        
        # 创建地板纹理
        color = (80, 80, 80)
        for y in range(0, 64, 8):
            for x in range(0, 64, 8):
                shade = 10 if (x//8 + y//8) % 2 == 0 else 0
                pygame.draw.rect(texture, 
                                (color[0]-shade, color[1]-shade, color[2]-shade), 
                                (x, y, 8, 8))
        
        return texture
    
    def render(self, player, level):
        # 绘制天空
        self.screen.blit(self.sky_texture, (0, 0))
        
        # 绘制地板
        floor_rect = pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        self.screen.fill(GRAY, floor_rect)
        
        # 使用射线投射绘制墙壁
        self.raycast(player, level.map)
        
        # 绘制敌人
        self.draw_enemies(player, level.enemies, level.map)
        
        # 绘制HUD
        self.draw_hud(player)
    
    def raycast(self, player, map_grid):
        # 对屏幕上的每一列进行射线投射
        for x in range(SCREEN_WIDTH):
            # 计算射线方向
            camera_x = 2 * x / SCREEN_WIDTH - 1  # -1到1
            ray_dir_x = math.cos(player.angle) + math.cos(player.angle - player.fov/2) * camera_x
            ray_dir_y = math.sin(player.angle) + math.sin(player.angle - player.fov/2) * camera_x
            
            # 玩家当前位置
            map_x, map_y = int(player.x), int(player.y)
            
            # 射线步进长度
            delta_dist_x = abs(1 / ray_dir_x) if ray_dir_x != 0 else float('inf')
            delta_dist_y = abs(1 / ray_dir_y) if ray_dir_y != 0 else float('inf')
            
            # 初始步进方向和距离
            if ray_dir_x < 0:
                step_x = -1
                side_dist_x = (player.x - map_x) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x + 1.0 - player.x) * delta_dist_x
                
            if ray_dir_y < 0:
                step_y = -1
                side_dist_y = (player.y - map_y) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y + 1.0 - player.y) * delta_dist_y
            
            # DDA算法
            hit = False
            side = 0  # 0=x方向, 1=y方向
            
            while not hit:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1
                
                # 检查是否击中墙壁
                if (0 <= map_y < len(map_grid) and 
                    0 <= map_x < len(map_grid[0]) and 
                    map_grid[map_y][map_x] > 0):
                    hit = True
            
            # 计算距离并校正鱼眼效果
            if side == 0:
                perp_wall_dist = (map_x - player.x + (1 - step_x) / 2) / ray_dir_x
            else:
                perp_wall_dist = (map_y - player.y + (1 - step_y) / 2) / ray_dir_y
            
            # 计算墙的高度
            line_height = int(SCREEN_HEIGHT / perp_wall_dist)
            
            # 计算墙的顶部和底部位置
            draw_start = max(-line_height // 2 + SCREEN_HEIGHT // 2, 0)
            draw_end = min(line_height // 2 + SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
            
            # 选择墙壁纹理
            wall_type = map_grid[map_y][map_x] - 1
            if wall_type < 0 or wall_type >= len(self.wall_textures):
                wall_type = 0
            
            texture = self.wall_textures[wall_type]
            
            # 计算纹理坐标
            if side == 0:
                wall_x = player.y + perp_wall_dist * ray_dir_y
            else:
                wall_x = player.x + perp_wall_dist * ray_dir_x
            wall_x -= math.floor(wall_x)
            
            # 纹理x坐标
            tex_x = int(wall_x * 64)
            if (side == 0 and ray_dir_x > 0) or (side == 1 and ray_dir_y < 0):
                tex_x = 64 - tex_x - 1
            
            # 绘制纹理列
            for y in range(draw_start, draw_end):
                tex_y = int((y - draw_start) * 64 / (draw_end - draw_start))
                color = texture.get_at((tex_x, tex_y))
                
                # 根据距离调整亮度
                brightness = max(0, 255 - int(perp_wall_dist * 20))
                if side == 1:
                    brightness = brightness // 1.5  # y方向的墙更暗
                
                color = (min(color[0], brightness), 
                        min(color[1], brightness), 
                        min(color[2], brightness))
                
                self.screen.set_at((x, y), color)
    
    def draw_enemies(self, player, enemies, map_grid):
        # 按距离排序（从远到近）
        sorted_enemies = sorted(enemies, key=lambda e: 
                               (e.x - player.x)**2 + (e.y - player.y)**2, 
                               reverse=True)
        
        # 绘制每个敌人
        for enemy in sorted_enemies:
            if enemy.is_alive():
                self.draw_sprite(player, enemy, map_grid)
    
    def draw_sprite(self, player, sprite, map_grid):
        # 计算精灵相对于玩家的位置和距离
        dx = sprite.x - player.x
        dy = sprite.y - player.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 计算精灵相对于玩家的角度
        sprite_angle = math.atan2(dy, dx) - player.angle
        
        # 标准化角度到[-π, π]范围内
        while sprite_angle > math.pi:
            sprite_angle -= 2 * math.pi
        while sprite_angle < -math.pi:
            sprite_angle += 2 * math.pi
        
        # 如果精灵在玩家视野内
        if abs(sprite_angle) < player.fov / 2 + 0.2:  # 稍微扩大视野范围
            # 计算精灵在屏幕上的水平位置
            sprite_screen_x = int((sprite_angle / player.fov + 0.5) * SCREEN_WIDTH)
            
            # 计算精灵大小（基于距离）
            sprite_height = int(SCREEN_HEIGHT / distance * 2)
            sprite_width = sprite_height
            
            # 计算精灵在屏幕上的垂直位置（居中）
            sprite_screen_y = SCREEN_HEIGHT // 2
            
            # 绘制精灵
            draw_start_x = max(0, sprite_screen_x - sprite_width // 2)
            draw_end_x = min(SCREEN_WIDTH, sprite_screen_x + sprite_width // 2)
            draw_start_y = max(0, sprite_screen_y - sprite_height // 2)
            draw_end_y = min(SCREEN_HEIGHT, sprite_screen_y + sprite_height // 2)
            
            # 缩放纹理并绘制
            if draw_start_x < draw_end_x and draw_start_y < draw_end_y:
                scaled_sprite = pygame.transform.scale(sprite.texture, 
                                                     (sprite_width, sprite_height))
                self.screen.blit(scaled_sprite, (draw_start_x, draw_start_y))
    
    def draw_hud(self, player):
        # 绘制生命值条
        health_width = 200
        health_height = 20
        health_x = 10
        health_y = SCREEN_HEIGHT - 40
        
        # 背景
        pygame.draw.rect(self.screen, (100, 0, 0), 
                        (health_x, health_y, health_width, health_height))
        # 当前生命值
        pygame.draw.rect(self.screen, (0, 200, 0), 
                        (health_x, health_y, health_width * player.health / 100, health_height))
        # 边框
        pygame.draw.rect(self.screen, WHITE, 
                        (health_x, health_y, health_width, health_height), 2)
        
        # 生命值文本
        health_text = self.font.render(f"Health: {player.health}", True, WHITE)
        self.screen.blit(health_text, (health_x, health_y - 25))
        
        # 弹药和分数
        ammo_text = self.font.render(f"Ammo: {player.ammo}", True, WHITE)
        score_text = self.font.render(f"Score: {player.score}", True, WHITE)
        
        self.screen.blit(ammo_text, (SCREEN_WIDTH - 150, 10))
        self.screen.blit(score_text, (SCREEN_WIDTH - 150, 40))
        
        # 十字准星
        pygame.draw.line(self.screen, WHITE, 
                        (SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2),
                        (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2), 2)
        pygame.draw.line(self.screen, WHITE, 
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10),
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10), 2)