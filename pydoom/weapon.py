import pygame
from settings import *

class Weapon:
    def __init__(self):
        self.damage = WEAPON_DAMAGE
        self.range = WEAPON_RANGE
        self.cooldown = 0
        self.max_cooldown = WEAPON_COOLDOWN
        self.is_firing = False
        self.fire_frame = 0
        
        # 创建武器动画帧
        self.frames = []
        self.create_frames()
    
    def create_frames(self):
        # 创建简单的武器动画帧
        for i in range(5):
            frame = pygame.Surface((200, 200), pygame.SRCALPHA)
            # 绘制简单的武器图形
            pygame.draw.rect(frame, (150, 150, 150), (50, 100, 100, 50))
            pygame.draw.rect(frame, (100, 100, 100), (140, 110, 40, 30))
            
            # 根据帧数添加枪口闪光
            if i > 0 and i < 4:
                pygame.draw.rect(frame, (255, 255, 0), (180, 115, 10 + i*5, 20))
            
            self.frames.append(frame)
    
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        
        if self.is_firing:
            self.fire_frame += 1
            if self.fire_frame >= len(self.frames):
                self.fire_frame = 0
                self.is_firing = False
    
    def fire(self, player, enemies):
        if self.cooldown <= 0 and player.ammo > 0:
            self.cooldown = self.max_cooldown
            self.is_firing = True
            self.fire_frame = 0
            player.ammo -= 1
            
            # 检查是否击中敌人
            for enemy in enemies:
                if self.check_hit(player, enemy):
                    enemy.take_damage(self.damage)
                    if enemy.health <= 0:
                        player.add_score(100)
                    return True
            return False
    
    def check_hit(self, player, enemy):
        # 计算玩家到敌人的向量
        dx = enemy.x - player.x
        dy = enemy.y - player.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 检查距离
        if distance > self.range:
            return False
        
        # 计算角度差
        angle_to_enemy = math.atan2(dy, dx)
        angle_diff = abs(angle_to_enemy - player.angle)
        
        # 标准化角度差
        if angle_diff > math.pi:
            angle_diff = 2 * math.pi - angle_diff
        
        # 如果敌人在玩家视野内，则击中
        return angle_diff < player.fov / 2
    
    def draw(self, screen):
        if self.is_firing:
            frame = self.frames[self.fire_frame]
        else:
            frame = self.frames[0]
        
        # 将武器绘制在屏幕底部中央
        weapon_rect = frame.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        screen.blit(frame, weapon_rect)