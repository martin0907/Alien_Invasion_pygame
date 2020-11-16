import pygame
import random
import time
import os

pygame.font.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Alien invasion")
ship = pygame.image.load(os.path.join("images", "ship.png"))
alien = pygame.image.load(os.path.join("images", "alien.png"))
red_bullet = pygame.image.load(os.path.join("images", "red.png"))
green_bullet = pygame.image.load(os.path.join("images", "green.png"))
background = pygame.transform.scale(pygame.image.load(os.path.join("images","space.jpg")), (width, height))
bullet_speed = 3
ship_speed = 5
enemy_speed = 1

class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = ship
        self.bullets = []

    def show(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.show(window)

    def move_bullets(self, speed, obj):
        for bullet in self.bullets:
            bullet.move(speed)
            if bullet.screen_edge(height):
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                obj.health -= 25
                self.bullets.remove(bullet)
    
    def fire(self):
            bullet = Bullet(self.x+28, self.y-7, self.bullets_img)
            self.bullets.append(bullet)
           
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def show(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, speed):
        self.y += speed
    
    def screen_edge(self, height):
        return not(self.y <= height and self.y >= 0)
        
    def collision(self, obj):
        return collide(self, obj)

class Player(Ship):
    def __init__(self, x, y, health = 100, score = 0):
        super().__init__(x, y, health)
        self.ship_img = ship
        self.bullets_img = green_bullet
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = score
        self.moving_right = False
        self.moving_left = False
        self.moving_UP = False
        self.moving_DOWN = False

    def move_bullets(self, speed, objs):
        for bullet in self.bullets:
            bullet.move(speed)
            if bullet.screen_edge(height):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        objs.remove(obj)
                    if bullet.collision(obj):
                        self.score += 1
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

    def move(self, ship):
        if self.moving_left and ship.x - ship_speed > 0:
            ship.x -= ship_speed
        if self.moving_right and ship.x + ship_speed + ship.get_width() < width:
            ship.x += ship_speed
        if self.moving_UP and ship.y - ship_speed > 0:
            ship.y -= ship_speed
        if self.moving_DOWN and ship.y + ship_speed + ship.get_height() < height:
            ship.y += ship_speed

    def show(self, window):
        super().show(window)
        self.healthbar(window)
    
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 5, self.ship_img.get_width(), 5))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 5, self.ship_img.get_width() * (self.health/self.max_health), 5))

class Alien(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = alien
        self.bullet_img = red_bullet
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, speed):
        self.y += speed

    def fire(self):
            bullet = Bullet(self.x+24, self.y+42, self.bullet_img)
            self.bullets.append(bullet)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return (obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None)

def key_down(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_UP = True
    elif event.key == pygame.K_DOWN:
        ship.moving_DOWN = True
    elif event.key == pygame.K_SPACE:
        ship.fire()
    
def key_up(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_UP = False
    elif event.key == pygame.K_DOWN:
        ship.moving_DOWN = False

def moving(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            key_down(event, ship)
        elif event.type == pygame.KEYUP:
            key_up(event, ship)

def game():
    run = True
    fps = 60
    level = 0
    lives = 5
    lives_title = pygame.font.SysFont("comicsans", 40)
    level_title = pygame.font.SysFont("comicsans", 40)
    score_title = pygame.font.SysFont("comicsans", 40)
    enemies = []
    wave_length = 5
    lost = False
    clock = pygame.time.Clock()
    ship = Player(50,500)
    score = ship.score

    def update_screen():
        screen.blit(background, (0,0))
        lives_tittle = lives_title.render(f"Lives: {lives}", 1, (255,255,255))
        level_tittle = level_title.render(f"Level: {level}", 1, (255,255,255))
        score_tittle = score_title.render(f"Score: {ship.score}", 1, (255,255,255))
        screen.blit(lives_tittle, (10, 10))
        screen.blit(level_tittle, (width - level_tittle.get_width() - 10, 10))
        screen.blit(score_tittle, (450, 10))

        for enemy in enemies:
            enemy.show(screen)

        ship.show(screen)
        pygame.display.update()

    while run:
        clock.tick(fps)
        update_screen()
        ship.move(ship)
        moving(ship)

        if lives <= 0 or ship.health <= 0:
            lost = True
            run = False
        
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Alien(random.randrange(50, 950), random.randrange(-1700, 100))
                enemies.append(enemy)
        
        for enemy in enemies[:]:
            enemy.move(enemy_speed)
            enemy.move_bullets(bullet_speed, ship)

            if random.randrange(0, 2*60) == 1:
                enemy.fire()

            if collide(enemy, ship):
                ship.health -= 20
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)

        ship.move_bullets(-bullet_speed, enemies)
  
game()