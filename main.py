import pygame
import os
import time
import random
from game import Game
from constants import WIDTH, HEIGHT

pygame.font.init()

# Setting window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


# Background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
 

def main(mode='easy'):
    run = True
    FPS = 60

    main_font = pygame.font.SysFont("comicsans", 40) # Choose font
    lost_font = pygame.font.SysFont("comicsans", 50) # Choose font

    game = Game()
    game.create_game(mode)
    player = game.player
    player_velocity = game.player_velocity 
    clock = pygame.time.Clock()

    lost_count = 0


    def pause():
        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()


            paused_label = lost_font.render("Game is paused!", 1, (255, 0, 0))
            instruction_label = lost_font.render("Press c to continue or q to quit.", 1, (255, 0, 0))
            WIN.blit(paused_label, (int(WIDTH/2 - paused_label.get_width()/2), 350))
            WIN.blit(instruction_label, (int(WIDTH/2 - instruction_label.get_width()/2), 400))

            pygame.display.update()
            clock.tick(5)

    def redraw_window():

        enemies = game.enemies
        boss = game.boss
        lost = game.lost
        lives = game.lives
        level = game.level
        drop = game.drop


        WIN.blit(BACKGROUND, (0, 0))
        # draw text
        level_label = main_font.render(f"Level: {level}", 1, (255, 0, 0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 0, 0))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)
        
        if boss:
            boss.draw(WIN)
        
        if drop:
            drop.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 0, 0))
            WIN.blit(lost_label, (int(WIDTH/2 - lost_label.get_width()/2), 350))
        
        pygame.display.update()
        
    while run:
        clock.tick(FPS)
        redraw_window()

        game.check_player_health()

        game.check_player_lives()

        if game.lost:
            lost_count += 1
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        game.check_boss()

        game.create_enemies()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and ((player.x - player_velocity) > 0): # moving left
            player.x -= player_velocity
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and ((player.x + player_velocity + player.get_width()) < WIDTH): # moving right
            player.x += player_velocity
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and ((player.y + player_velocity + player.get_height() + 15) < HEIGHT): # moving down
            player.y += player_velocity
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and ((player.y - player_velocity) > 0): # moving up
            player.y -= player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_ESCAPE]:
            pause()
 
        game.move_enemies()
        game.move_boss()
        game.move_drop()
        game.move_laser_player()
        

class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (255,255,255))
            win.blit(text, (int(self.x + (self.width/2 - text.get_width()/2)), int(self.y + (self.height/2 - text.get_height()/2))))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    menu_font = pygame.font.SysFont("comicsans", 40)
    run = True 
    while run:
        WIN.blit(BACKGROUND, (0,0))
        title_label = title_font.render("Space Invaders", 1, (255,255,255))
        WIN.blit(title_label, (int(WIDTH/2 - title_label.get_width()/2), 150))

        menu_label = menu_font.render("Pick a mode", 1, (255,255,255))
        WIN.blit(menu_label, (int(WIDTH/2 - menu_label.get_width()/2), 250))

        easy_button = Button((0,0,255), int((WIDTH/2) - (80 / 2)), 300, 80, 70, text='Easy')
        medium_button = Button((0,0,255), int((WIDTH/2) - (80 / 2)), 390, 80, 75, text='Medium')
        hard_button = Button((0,0,255), int((WIDTH/2) - (80 / 2)), 480, 80, 75, text='Hard')

        easy_button.draw(WIN)
        medium_button.draw(WIN)
        hard_button.draw(WIN)

        pygame.display.update()

        for event in pygame.event.get(): 
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.isOver(pos):
                    main(easy_button.text)
                elif medium_button.isOver(pos):
                    main(medium_button.text)
                elif hard_button.isOver(pos):
                    main(hard_button.text)
    
    pygame.quit()

if __name__ == "__main__":
    main_menu()
