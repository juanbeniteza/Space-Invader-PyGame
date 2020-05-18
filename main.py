import pygame
import os
import time
import random
pygame.font.init()

# Setting window
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Boss Ship
BOSS_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_boss.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, windows):
        windows.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collison(self, obj):
        return collide(obj, self)

class Ship:

    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
       window.blit(self.ship_img, (self.x, self.y))
       for laser in self.lasers:
           laser.draw(window)

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collison(obj):
                obj.health -= 10
                self.lasers.remove(laser)


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs, boss=None):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                if boss:
                     if laser.collison(boss):
                        boss.health -= 10
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                for obj in objs:
                    if laser.collison(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, int(self.y + self.ship_img.get_height() + 10), int(self.ship_img.get_width()), 5))
        pygame.draw.rect(window, (0,255,0), (self.x, int(self.y + self.ship_img.get_height() + 10), int(self.ship_img.get_width() * (self.health/self.max_health)), 5))


class Enemy(Ship):
    
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
    }
    
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Boss(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = BOSS_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    def move(self, vel):
        self.x += vel

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, int(self.y + self.ship_img.get_height() + 10), int(self.ship_img.get_width()), 5))
        pygame.draw.rect(window, (0,255,0), (self.x, int(self.y + self.ship_img.get_height() + 10), int(self.ship_img.get_width() * (self.health/self.max_health)), 5))


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    player_velocity = 5
    main_font = pygame.font.SysFont("comicsans", 40) # Choose font
    lost_font = pygame.font.SysFont("comicsans", 50) # Choose font

    enemies = []
    boss = None
    wave_length = 5
    enemy_velocity = 1
    laser_velocity = 5
    boss_velocity = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
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

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 0, 0))
            WIN.blit(lost_label, (int(WIDTH/2 - lost_label.get_width()/2), 350))
        
        pygame.display.update()
        
    while run:
        clock.tick(FPS)
        redraw_window()

        if player.health <= 0:
            lives -= 1
            player.health = player.max_health

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
            
        if boss:
            if boss.health <= 0:
                boss = None

        if len(enemies) == 0 and boss == None:
            if player.health < 90:
                player.health += 10
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

            if level % 2 == 0:
                boss = Boss(int(WIDTH/2 - BOSS_SPACE_SHIP.get_width()/2), 30, health=50*level)


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

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)
            
            if random.randrange(0, 4*60) == 1:
                enemy.shoot()
            
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        if boss:
            if boss_velocity > 0 and (boss.x + boss_velocity + boss.get_width() > WIDTH):
                boss_velocity = -boss_velocity
            if boss_velocity < 0 and ((boss.x + boss_velocity < 0)):
                boss_velocity = abs(boss_velocity)
            
            boss.move(boss_velocity)
            boss.move_lasers(laser_velocity, player)
            boss.shoot()

        player.move_lasers(-laser_velocity, enemies, boss)
        

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True 
    while run:
        WIN.blit(BACKGROUND, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (int(WIDTH/2 - title_label.get_width()/2), 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    
    pygame.quit()

if __name__ == "__main__":
    main_menu()
