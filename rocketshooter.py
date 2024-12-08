import pgzero
import pygame
from pygame.locals import *
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Rocket Shooter")

BORDER = pygame.Rect(900/2, 0, 10, 500)

#Sounds
BULLET_HIT_SOUND = pygame.mixer.Sound("rocketshooter/bullet.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("rocketshooter/grenade.mp3")

#fonts
HEALTH_FONT = pygame.font.SysFont("Arial", (50))
WINNER_FONT = pygame.font.SysFont("Arial", (80))

#speed
FPS = 60
VEL = 5
BULLET_VEL = 7
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (55, 40)

#images
ROCKET1 = pygame.image.load("rocketshooter/player1.png")
ROCKET2 = pygame.image.load("rocketshooter/player2.png")
SKY = pygame.transform.scale(pygame.image.load("rocketshooter/sky.png"), (900, 500))

#health
rocket1_health = 10
rocket2_health = 10

#rocket 
class Rocket(pygame.sprite.Sprite):
    def __init__(self, image, angle, x, y):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale(image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), angle)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
    def move_horizontal(self, v, player):
        self.rect.x += v
        if player == 1:
            if self.rect.left <= 0 or self.rect.right >= BORDER.left:
                self.rect.move_ip(-v, 0)
        if player == 2:
            if self.rect.left <= BORDER.right or self.rect.right >= 900:
                self.rect.move_ip(-v, 0)
    def move_vertical(self, v):
        self.rect.move_ip(0, v)
        if self.rect.top <= 0 or self.rect.bottom >= 500:
            self.rect.move_ip(0, -v)

rocket1 = Rocket(ROCKET1, 270, 650, 200)
rocket2 = Rocket(ROCKET2, 90, 150, 200)

sprites = pygame.sprite.Group()
sprites.add(rocket1)
sprites.add(rocket2)