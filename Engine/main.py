import math
from game import Game
import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 120

# L'interface
pygame.display.set_caption("Shooter")
pygame.display.set_icon(pygame.image.load("./Engine/assets/banner.png"))
screen = pygame.display.set_mode((1080, 720))

# Images / Assets
background = pygame.image.load("./Engine/assets/bg.jpg")

#Logo menu
banner = pygame.image.load("./Engine/assets/banner.png")
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

#Play button
play_button = pygame.image.load("./Engine/assets/button.png")
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)

#Exit Button
exit_button = pygame.image.load("./Engine/assets/exit_button.png")
exit_button = pygame.transform.scale(exit_button, (100, 100))
exit_button_rect = exit_button.get_rect()
exit_button_rect.x = math.ceil(490)
exit_button_rect.y = 600

#Load the player
game = Game()

running = True

while running :

    #Set Background Image
    screen.blit(background, (-1280, -200))
    
    if game.is_playing:
        game.update(screen)
    else:
        screen.blit(play_button, play_button_rect)
        screen.blit(exit_button, exit_button_rect)
        screen.blit(banner, banner_rect)
        game.update_screen_score(screen)

    #Update assets
    pygame.display.flip()

    for event in pygame.event.get():
        
        #Game stops
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Game closed !")
        #Player movements
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_SPACE:
                if game.is_playing:
                    game.player.launch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game.start()
                game.sound_manager.play('click')
            elif exit_button_rect.collidepoint(event.pos):
                running = False
                pygame.quit()
    
    clock.tick(FPS)