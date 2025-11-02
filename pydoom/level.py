import pygame
from enemy import Enemy

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.map = self.generate_map()
        self.enemies = self.generate_enemies()
        self.player_start_pos = self.find_player_start()
        self.items = []  # 可以添加血包、弹药等物品
        
    def generate_map(self):
        # 根据关卡号生成不同的地图
        if self.level_number == 1:
            return [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        elif self.level_number == 2:
            return [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        else:
            # 默认地图
            return [
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]
            ]
    
    def generate_enemies(self):
        enemies = []
        
        # 根据关卡号生成不同数量和类型的敌人
        if self.level_number == 1:
            enemies.append(Enemy(2.5, 2.5, 0))
            enemies.append(Enemy(5.5, 5.5, 0))
        elif self.level_number == 2:
            enemies.append(Enemy(2.5, 2.5, 0))
            enemies.append(Enemy(9.5, 2.5, 0))
            enemies.append(Enemy(2.5, 9.5, 1))  # 快速敌人
            enemies.append(Enemy(9.5, 9.5, 1))
        else:
            # 默认敌人
            enemies.append(Enemy(2.5, 2.5, 0))
            enemies.append(Enemy(5.5, 5.5, 0))
        
        return enemies
    
    def find_player_start(self):
        # 在地图上找到一个空位置作为玩家起始点
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == 0:
                    return (x + 0.5, y + 0.5)  # 返回格子中心
        return (1.5, 1.5)  # 默认起始点
    
    def is_completed(self):
        # 检查是否所有敌人都被消灭
        return all(not enemy.is_alive() for enemy in self.enemies)
    
    def update_enemies(self, player):
        for enemy in self.enemies[:]:
            if enemy.is_alive():
                enemy.update(player, self.map)
            else:
                self.enemies.remove(enemy)