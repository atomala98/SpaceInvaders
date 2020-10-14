from start_variables import *
import pygame

# loading all game graphics
bcg = pygame.image.load("bcg.jpg")
playerimage = pygame.image.load("player.png")
enemyimage = pygame.image.load("enemy.png")
enemyimage = pygame.transform.flip(enemyimage, 0, 1)
playerbullet = pygame.image.load("playerbullet.png")
enemybullet = pygame.image.load("enemybullet.png")


# ship class
class Ship:
    def __init__(self, x, y, velocity_x, velocity_y, cooldown, size, lives):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.cooldown = cooldown
        self.lives = lives
        self.bullets = []
        self.size = size
        self.name = ''


# player class, parenting from ship, with scores added
class Player(Ship):
    def __init__(self, x, y, velocity_x, velocity_y, cooldown, size, lives):
        Ship.__init__(self, x, y, velocity_x, velocity_y, cooldown, size, lives)
        self.score = 0

    def draw(self, win):
        win.blit(playerimage, (self.x - self.size[0] // 2, self.y - self.size[0] // 2))

    # adding bullet to player.bullets array
    def shot(self):
        self.bullets.insert(0, Bullet(self.x, self.y - self.size[1] // 2, BULLET_VELOCITY, BULLET_SIZE))
        self.cooldown = PLAYER_COOLDOWN

    # moving bullets with predefined velocity, deleting bullets that go off-screen
    def bullet_move(self):
        for bullet in self.bullets:
            bullet.y -= bullet.velocity
            if bullet.y < -30:
                del self.bullets[self.bullets.index(bullet)]


class Enemy(Ship):
    def draw(self, win):
        win.blit(enemyimage, (self.x - self.size[0] // 2, self.y - self.size[0] // 2))

    # nearly same as player.shot
    def shot(self):
        self.bullets.insert(0, Bullet(self.x, self.y + self.size[1] // 2,
                                      BULLET_VELOCITY, BULLET_SIZE))
        self.cooldown = ENEMY_COOLDOWN

    # nearly same as player.bullet_move
    def bullet_move(self):
        for bullet in self.bullets:
            bullet.y += bullet.velocity
            if bullet.y > HEIGHT:
                del self.bullets[self.bullets.index(bullet)]


class Bullet:
    def __init__(self, x, y, velocity, size):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.size = size
        self.lives = 1

    def draw(self, win, image):
        win.blit(image, (self.x - self.size[0] // 2, self.y - self.size[0] // 2))


# class defining menu buttons template
class Button:
    def __init__(self, size, x, y, text):
        self.size = size
        self.x = x
        self.y = y
        self.text = text

    def draw(self, win, color, font):
        pygame.draw.rect(win, color, (self.x - self.size[0]//2, self.y - self.size[1]//2, self.size[0], self.size[1]))
        text = font.render(self.text, 1, WHITE)
        win.blit(text, (self.x - text.get_width()//2, self.y - text.get_height()//2, self.size[0], self.size[1]))
