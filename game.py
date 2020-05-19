from ship import Boss, Player, Enemy, Drop
from util import collide
import laser
import random
from constants import HEIGHT, WIDTH

class Game:

    GAME_MODE = {
        "Easy": {
            "wave_length_increase": 5,
            "enemy_velocity": 1,
            "boss_velocity": 4
        },
        "Medium": {
            "wave_length_increase": 7,
            "enemy_velocity": 2,
            "boss_velocity": 5
        },
        "Hard": {
            "wave_length_increase": 10,
            "enemy_velocity": 3,
            "boss_velocity": 6
        },
    }

    def __init__(self):
        self.wave_length = None
        self.enemy_velocity = None
        self.laser_velocity = 5
        self.boss_velocity = None
        self.player_velocity = 5
        self.enemies = []
        self.boss = None
        self.drop = None
        self.lost = False
        self.level = 0
        self.lives = 5
        self.player = None


    def create_game(self, mode):

        obj = self.GAME_MODE[mode]
        self.wave_length = obj['wave_length_increase']
        self.wave_length_increase = obj['wave_length_increase']
        self.enemy_velocity = obj['enemy_velocity']
        self.boss_velocity = obj['boss_velocity']
        self.player = Player(300, 630)

        return self

    
    def check_player_health(self):

        if self.player.health <= 0:
            self.lives -= 1
            self.player.health = self.player.max_health
    
    def check_player_lives(self):
        if self.lives <= 0 or self.player.health <= 0:
            self.lost = True

    def check_boss(self):
        if self.boss:
            if self.boss.health <= 0:
                self.boss = None

    def create_enemies(self):
        if len(self.enemies) == 0 and self.boss == None:
            if self.player.health < 90:
                self.player.health += 10
            self.level += 1
            self.wave_length += self.wave_length_increase
            for _ in range(self.wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                self.enemies.append(enemy)

            if self.level % 4 == 0:
                self.drop = Drop(random.randrange(50, WIDTH-100), random.randrange(-1500, -100))

            if self.level % 5 == 0:
                self.boss = Boss(health=50*self.level)
        
        if len(self.enemies) == 0 and self.boss:
            for _ in range(self.wave_length//2):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                self.enemies.append(enemy)

    def move_enemies(self):
        for enemy in self.enemies[:]:
            enemy.move(self.enemy_velocity)
            enemy.move_lasers(self.laser_velocity, self.player)
            
            if random.randrange(0, 4*60) == 1:
                enemy.shoot()
            
            if collide(enemy, self.player):
                self.player.health -= 20
                self.enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                self.lives -= 1
                self.enemies.remove(enemy)

    def move_boss(self):
        if self.boss:
            if self.boss_velocity > 0 and (self.boss.x + self.boss_velocity + self.boss.get_width() > WIDTH):
                self.boss_velocity = -self.boss_velocity
            if self.boss_velocity < 0 and ((self.boss.x + self.boss_velocity < 0)):
                self.boss_velocity = abs(self.boss_velocity)
            
            self.boss.move(self.boss_velocity)
            self.boss.move_lasers(self.laser_velocity, self.player)
            self.boss.shoot()
    
    def move_laser_player(self):
        self.player.move_lasers(-self.laser_velocity, self.enemies, self.boss)

    def move_drop(self):
        if self.drop:
            self.drop.move(self.enemy_velocity)

            if collide(self.drop, self.player):
                self.lives += 1
                self.drop = None
            
            elif self.drop.y + self.drop.get_height() > HEIGHT:
                self.drop = None
    

