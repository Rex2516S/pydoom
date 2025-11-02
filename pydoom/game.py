import pygame
import sys
from player import Player
from weapon import Weapon
from level import Level
from renderer import Renderer
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PyDoom")
        self.clock = pygame.time.Clock()
        
        self.current_level = 1
        self.level = Level(self.current_level)
        self.player = Player(*self.level.player_start_pos, 0)
        self.weapon = Weapon()
        self.renderer = Renderer(self.screen)
        
        self.running = True
        self.game_state = "playing"  # playing, game_over, level_complete
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.game_state == "playing":
                    self.weapon.fire(self.player, self.level.enemies)
                elif event.key == pygame.K_r and self.game_state != "playing":
                    self.restart_game()
        
        if self.game_state == "playing":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.move_forward(self.level.map)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.move_backward(self.level.map)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.rotate_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.rotate_right()
            if keys[pygame.K_q]:
                self.player.strafe_left(self.level.map)
            if keys[pygame.K_e]:
                self.player.strafe_right(self.level.map)
    
    def update(self):
        if self.game_state == "playing":
            self.weapon.update()
            self.level.update_enemies(self.player)
            
            # 检查游戏状态
            if self.player.health <= 0:
                self.game_state = "game_over"
            elif self.level.is_completed():
                if self.current_level < 2:  # 假设有2关
                    self.current_level += 1
                    self.level = Level(self.current_level)
                    self.player = Player(*self.level.player_start_pos, 0)
                else:
                    self.game_state = "level_complete"
    
    def render(self):
        if self.game_state == "playing":
            self.renderer.render(self.player, self.level)
            self.weapon.draw(self.screen)
        elif self.game_state == "game_over":
            self.screen.fill(BLACK)
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)
            
            font_small = pygame.font.SysFont(None, 36)
            score_text = font_small.render(f"Final Score: {self.player.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            self.screen.blit(score_text, score_rect)
            
            restart_text = font_small.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120))
            self.screen.blit(restart_text, restart_rect)
        elif self.game_state == "level_complete":
            self.screen.fill(BLACK)
            font = pygame.font.SysFont(None, 72)
            text = font.render("YOU WIN!", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)
            
            font_small = pygame.font.SysFont(None, 36)
            score_text = font_small.render(f"Final Score: {self.player.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            self.screen.blit(score_text, score_rect)
            
            restart_text = font_small.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def restart_game(self):
        self.current_level = 1
        self.level = Level(self.current_level)
        self.player = Player(*self.level.player_start_pos, 0)
        self.weapon = Weapon()
        self.game_state = "playing"
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()