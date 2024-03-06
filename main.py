# Link download code trên Github
# https://github.com/NMThanh123/Chicken-Invaders.git

import pygame
import os
import random
pygame.init()

WIDTH, HEIGHT = 1000, 950
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
start = True
pygame.display.set_caption("Checken Invaders")
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon-chicken.png")))
sound = pygame.mixer.Sound(os.path.join("sound.wav"))
sound1 = pygame.mixer.Sound(os.path.join("sound1.wav"))

# Load chicken
RED_SPACE_CHICKEN = pygame.image.load(os.path.join("assets","chicken-red.png"))
RED_SPACE_CHICKEN = pygame.transform.scale(RED_SPACE_CHICKEN, (60, 60))
GREEN_SPACE_CHICKEN = pygame.image.load(os.path.join("assets", "chicken-green.png"))
GREEN_SPACE_CHICKEN = pygame.transform.scale(GREEN_SPACE_CHICKEN, (60, 60))
BLUE_SPACE_CHICKEN = pygame.image.load(os.path.join("assets", "chicken-blue.png"))
BLUE_SPACE_CHICKEN = pygame.transform.scale(BLUE_SPACE_CHICKEN, (60, 60))
BIG_SPACE_CHICKEN = pygame.image.load(os.path.join("assets", "chicken-1.png"))
BIG_SPACE_CHICKEN = pygame.transform.scale(BIG_SPACE_CHICKEN, (60, 60))
POLICE_SPACE_CHICKEN = pygame.image.load(os.path.join("assets", "chicken-2.png"))
POLICE_SPACE_CHICKEN = pygame.transform.scale(POLICE_SPACE_CHICKEN, (70, 70))
W_SPACE_CHICKEN = pygame.image.load(os.path.join("assets", "chicken-3.png"))
W_SPACE_CHICKEN = pygame.transform.scale(W_SPACE_CHICKEN, (65, 80))
FLY_SPACE_CHICKEN = pygame.image.load(os.path.join("assets", "chicken-fly.png"))
FLY_SPACE_CHICKEN = pygame.transform.scale(FLY_SPACE_CHICKEN, (60, 95))

BOSS_CHICKEN =  pygame.image.load(os.path.join("assets", "boss.png"))
BOSS_CHICKEN = pygame.transform.scale(BOSS_CHICKEN, (500, 300))

# Load box bullet
BOX_RED = pygame.image.load(os.path.join("assets","box-bullet2.png"))
BOX_RED = pygame.transform.scale(BOX_RED, (35, 35))
BOX_GREEN = pygame.image.load(os.path.join("assets","box-bullet1.png"))
BOX_GREEN = pygame.transform.scale(BOX_GREEN, (35, 35))
BOX_PURPLE = pygame.image.load(os.path.join("assets","box-bullet3.png"))
BOX_PURPLE = pygame.transform.scale(BOX_PURPLE, (35, 35))
BOX_ORANGE = pygame.image.load(os.path.join("assets","box-bullet4.png"))
BOX_ORANGE = pygame.transform.scale(BOX_ORANGE, (35, 35))
BOX_BLUE = pygame.image.load(os.path.join("assets","box-bullet5.png"))
BOX_BLUE = pygame.transform.scale(BOX_BLUE, (35, 35))

# Player player
PLAN = pygame.image.load(os.path.join("assets", "plan.png"))
PLAN = pygame.transform.scale(PLAN, (150, 150))
GREEN_LASER = pygame.image.load(os.path.join("assets", "bullet1.png"))
GREEN_LASER = pygame.transform.scale(GREEN_LASER, (80, 68))
RED_LASER = pygame.image.load(os.path.join("assets", "bullet2.png"))
RED_LASER = pygame.transform.scale(RED_LASER, (80, 68))
PURPLE_LASER = pygame.image.load(os.path.join("assets", "bullet3.png"))
PURPLE_LASER = pygame.transform.scale(PURPLE_LASER, (80, 68))
ORANGE_LASER = pygame.image.load(os.path.join("assets", "bullet4.png"))
ORANGE_LASER = pygame.transform.scale(ORANGE_LASER, (90, 80))
BLUE_LASER = pygame.image.load(os.path.join("assets", "bullet5.png"))
BLUE_LASER = pygame.transform.scale(BLUE_LASER, (85, 60))
CHICKEN = pygame.image.load(os.path.join("assets", "chicken.png"))
CHICKEN = pygame.transform.scale(CHICKEN, (20, 40))
ROCKET = pygame.image.load(os.path.join("assets", "rocket.png"))
ROCKET = pygame.transform.scale(ROCKET, (40, 40))

# Lasers enemy
EGG_1 = pygame.image.load(os.path.join("assets", "egg.png"))
EGG_1 = pygame.transform.scale(EGG_1, (20, 20))
EGG_2 = pygame.image.load(os.path.join("assets", "egg1.png"))
EGG_2 = pygame.transform.scale(EGG_2, (35,38))
EGG_3 = pygame.image.load(os.path.join("assets", "egg3.png"))
EGG_3 = pygame.transform.scale(EGG_3, (20,25))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))
BG1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg1.jpg")), (WIDTH, HEIGHT))

class Egg: 
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height  and self.y >= -10)

    def collision(self, obj):
        return collide(self, obj)


class Plan:
    COOLDOWN = 30

    def __init__(self, x, y, health=200):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Egg(self.x+32, self.y-25, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()


class Player(Plan):
    def __init__(self, x, y, health=200):
        super().__init__(x, y, health)
        self.img = PLAN
        self.laser_img = BLUE_LASER
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health
        self.chicken = []

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                if type(objs) is list:
                    for obj in objs:
                        if laser.collision(obj):
                            x = obj.x
                            y = obj.y
                            chicken_thighs = Egg(x+20,y+10, CHICKEN)
                            objs.remove(obj)
                            self.chicken.append(chicken_thighs)
            
                            if laser in self.lasers:
                                self.lasers.remove(laser)
                else:
                    if laser.collision(objs):
                        objs.health -= 10    
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (50, 60, (self.img.get_width()-40), 10))
        pygame.draw.rect(window, (0,255,0), (50, 60, (self.img.get_width()-40) * (self.health/self.max_health), 10))


class Chicken(Plan):
    COLOR_MAP = {
                "red": (RED_SPACE_CHICKEN, EGG_1),
                "green": (GREEN_SPACE_CHICKEN, EGG_1),
                "blue": (BLUE_SPACE_CHICKEN, EGG_1),
                "white": (W_SPACE_CHICKEN, EGG_3),
                "brown": (BIG_SPACE_CHICKEN, EGG_3),
                "police": (POLICE_SPACE_CHICKEN, EGG_2),
                "fly" :(FLY_SPACE_CHICKEN, EGG_1),
                }

    def __init__(self, x, y, color, health=200):
        super().__init__(x, y, health)
        self.img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Egg(self.x+20, self.y+30, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


class Boss(Plan):   
    def __init__(self, x, y, vel_boss_x, vel_boss_y, health=1000):
        super().__init__(x, y, health)
        self.img = BOSS_CHICKEN
        self.mask = pygame.mask.from_surface(self.img)
        self.vel_boss_x = vel_boss_x
        self.vel_boss_y = vel_boss_y
        self.max_health = health
        self.egg = EGG_1

    def move(self):
        if self.x <= 0 or self.x + self.img.get_width() >= WIDTH:
            self.vel_boss_x = - self.vel_boss_x
        self.x += self.vel_boss_x
            
        if self.y <= 40 or self.y + self.img.get_height() >= HEIGHT-200:    
            self.vel_boss_y = -self.vel_boss_y
        self.y += self.vel_boss_y

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Egg(self.x + random.randrange(50, 400), self.y+250, self.egg)
            self.lasers.append(laser)
            self.cool_down_counter = 1    
        
    def draw(self, window):
        super().draw(window)   
        self.healthbar(window)   

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (270, 30, (self.img.get_width()-40), 10))
        pygame.draw.rect(window, (0,255, 0), (270, 30, (self.img.get_width()-40) * (self.health/self.max_health), 10))


class Drop_box():
    COLOR = {
                "red": (BOX_RED, RED_LASER),
                "green": (BOX_GREEN, GREEN_LASER),
                "blue": (BOX_BLUE, BLUE_LASER),
                "purple": (BOX_PURPLE, PURPLE_LASER),
                "orange": (BOX_ORANGE, ORANGE_LASER)
            }

    def __init__(self, x, y , color):
        self.x = x
        self.y = y
        self.color = color
        self.img, self.laser = self.COLOR[color]
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y)) 

    def drop(self, vel):
        self.y += vel   
        if self.y >= HEIGHT:
            self.img, self.laser = self.COLOR[random.choice(["red", "green","blue", "purple", "orange"])]
            self.x = random.randint(100, WIDTH-150)
            self.y = -700

    def creat_box_new(self):
        self.img, self.laser = self.COLOR[random.choice(["red", "green","blue", "purple", "orange"])]
        self.x = random.randrange(100, WIDTH-150)
        self.y = -700        


class Back_ground_shoot:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.img = BG1
        self.heigt = self.img.get_height()

    def draw(self):
        WIN.blit(self.img, (self.x, self.y))
        WIN.blit(self.img, (self.x, self.y-self.heigt))
        
    def uppdate(self):
        self.y += self.speed
        if self.y == self.heigt:
            self.y = 0        
    
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    rocket = 0
    chicken_thigh_nums = 0
    main_font = pygame.font.SysFont("comicsans", 25)
    lost_font = pygame.font.SysFont("comicsans", 60)
    win_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 7
    enemy_vel = 1
    laser_vel_enemy = 2.5

    vel_boss_x = 1.2
    vel_boss_y = 1.2
    laser_vel_boss = 1.5
    
    player_vel = 5
    laser_vel_player = 4

    vel_box = 2
    speed_bg = 1
    
    player = Player(400, 800)

    clock = pygame.time.Clock()
    lost = False
    lost_count = 0

    bg1 = Back_ground_shoot(0, 0, speed_bg)
    box_bullet = Drop_box(random.randrange(100, WIDTH-150), random.randrange(-900, -100), random.choice(["red", "green", "blue", "purple","orange"]))
    
    boss = Boss(50, 50, vel_boss_x, vel_boss_y)
    
    def redraw_window():
        bg1.draw()
        bg1.uppdate()  
            
        box_bullet.drop(vel_box)
        box_bullet.draw(WIN)

        player.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)
        
        for chicken_thigh in player.chicken:
            chicken_thigh.draw(WIN)
    
        if collide(box_bullet, player):
            player.laser_img = box_bullet.laser
            box_bullet.creat_box_new()
        
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        text_hp = main_font.render(f"HP: ", 1, (255,255,255))
        rocket_label = main_font.render(f": {rocket}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(text_hp, (10, 45))
        WIN.blit(ROCKET, (10, 80))
        WIN.blit(rocket_label, (60, 80))

        if level == 4:
            boss.move()        
            boss.draw(WIN)  
            boss.shoot()
            boss.move_lasers(laser_vel_boss, player)
            player.move_lasers(-laser_vel_player, boss) 
            if boss.health == 0:
                win_label = win_font.render("You win!!", 1, (255,255,255))
                WIN.blit(win_label, (WIDTH/2 - win_label.get_width()/2, 400))
                boss.y = -1000
                boss.lasers = []
        
        if level < 4:
            player.move_lasers(-laser_vel_player, enemies)      

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 400))
            bg1.speed = 0  
            pygame.mixer.Sound.stop(sound)
        
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        for chicken_thigh in player.chicken:
            if collide(chicken_thigh, player):
                player.chicken.remove(chicken_thigh)
                chicken_thigh_nums += 1  

        if chicken_thigh_nums == 10:
            rocket += 1   
            chicken_thigh_nums = 0

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 7
            for i in range(wave_length):
                enemy = Chicken(random.randrange(60, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green", "white", "brown", "police", "fly"]))
                enemies.append(enemy) 

        if level == 4:
            bg1.speed = 0     
            enemy_vel = 0           
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.mixer.Sound.stop(sound)
            if event.type == pygame.MOUSEBUTTONDOWN:	
                if event.button == 1: 
                    enemy_vel = 1
                    laser_vel_enemy = 2.5
                    laser_vel_player = 4
                    player_vel = 5
                    vel_box = 2
                    bg1.speed = 1
                if event.button == 1 and start:
                    player.shoot()
           
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > -50: # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH+50: # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 5 < HEIGHT+50: # down
            player.y += player_vel
        if keys[pygame.K_SPACE] :
            player.shoot()
        if keys[pygame.K_ESCAPE] :
            enemy_vel = 0
            laser_vel_enemy = 0
            player_vel = 0
            laser_vel_player = 0
            vel_box = 0
            bg1.speed = 0
                
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel_enemy, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy) 

        for chicken_thigh in player.chicken:
            chicken_thigh.move(3)  

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 60)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 650))
        pygame.mixer.Sound.play(sound1)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.stop(sound1)
                pygame.mixer.Sound.play(sound)
                main()
    pygame.quit()

if __name__ == "__main__":
    main_menu()

