from player import Player
from monster import Monster
from monster import Mummy
from monster import Alien
from sounds import SoundManager
from comet_event import CometFallEvent
from projectile import Projectile
import pygame

class Game:
    def __init__(self):
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.comet_event = CometFallEvent(self)
        self.pressed = {}
        self.score = 0
        self.screen_score = 0
        self.highest_score = 0
        self.all_monsters = pygame.sprite.Group()
        self.sound_manager = SoundManager()
        self.font = pygame.font.Font("./Engine/assets/custom_font.ttf", 25)

    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)
        self.player.rect.x = 0
        self.score = 0

    def add_score(self, points=10):
        self.score += points

    def game_over(self):
       self.all_monsters = pygame.sprite.Group()
       self.player.health = self.player.max_health
       self.is_playing = False
       self.comet_event.reset_percent()
       self.comet_event.all_comets = pygame.sprite.Group()
       self.sound_manager.play('game_over')
       self.screen_score = self.score
       self.player.all_projectiles.remove(self.player.all_projectiles)
       if self.screen_score > self.highest_score:
           self.highest_score = self.screen_score

    def update(self, screen):
    
        #Show score
        score_text = self.font.render(f"Score : {self.score}", 1, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        screen.blit(self.player.image, self.player.rect)

        #Update player health bar
        self.player.update_health_bar(screen)

        self.comet_event.update_bar(screen)

        self.player.update_animation()

        #Get player projectiles
        for projectile in self.player.all_projectiles:
            projectile.move()

        #Get monsters
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()

        #Get Comets
        for comet in self.comet_event.all_comets:
            comet.fall()

        #Set Projectiles Image
        self.player.all_projectiles.draw(screen)

        #Monstre
        self.all_monsters.draw(screen)

        self.comet_event.all_comets.draw(screen)

        #Players movements with keys

        #Right
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()

        if self.pressed.get(pygame.K_d) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
    
        #Left
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()

        elif self.pressed.get(pygame.K_a) and self.player.rect.x > 0:
            self.player.move_left()

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self, monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))

    def update_screen_score(self, screen):
        #Score Menu
        score_text = self.font.render(f"Score : {self.screen_score}", 1, (255, 255, 255))
        screen.blit(score_text, (475, 500))

        #Highest Score
        score_text = self.font.render(f"Highest Score : {self.highest_score}", 1, (255, 255, 255))
        screen.blit(score_text, (425, 535))