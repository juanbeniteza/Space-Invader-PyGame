import pygame
import os
from constants import HEIGHT, WIDTH
from laser import Laser

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Boss Ship
BOSS_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_boss.png"))

# Drop
LIFE_DROP = pygame.image.load(os.path.join("assets", "new_life.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

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
    def __init__(self, health=100):
        self.x = int(WIDTH/2 - BOSS_SPACE_SHIP.get_width()/2)
        self.y = 30
        super().__init__(self.x, self.y, health)
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


class Drop(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = LIFE_DROP
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel