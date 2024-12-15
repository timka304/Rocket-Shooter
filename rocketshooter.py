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


def draw_window():
    screen.blit(SKY, (0,0))
    pygame.draw.rect(screen, "white", BORDER)
    rocket1_health_text = HEALTH_FONT.render("health: " + str(rocket1_health), 1 , "red")
    rocket2_health_text = HEALTH_FONT.render("health: " + str(rocket2_health), 1, "red")
    screen.blit(rocket1_health_text, (900-rocket1_health_text.get_width()-10, 10))
    screen.blit(rocket2_health_text, (20, 20))

def draw_bullets():
    for bullet in rocket1_bullets:
        pygame.draw.rect(screen, "red", bullet)
        bullet.x -= BULLET_VEL
    for bullet in rocket2_bullets:
        pygame.draw.rect(screen, "blue", bullet)
        bullet.x += BULLET_VEL

rocket1_hit = pygame.USEREVENT + 1
rocket2_hit = pygame.USEREVENT + 1

def handle_bullets():
    global rocket1_health, rocket2_health
    for bullet in rocket2_bullets:
        if rocket1.rect.colliderect(bullet):
            rocket1_health -= 1
            pygame.event.post(pygame.event.Event(rocket1_hit))
            rocket2_bullets.remove(bullet)
        elif bullet.x > 900:
            rocket2_bullets.remove(bullet)
    for bullet in rocket1_bullets:
        if rocket2.rect.colliderect(bullet):
            rocket2_health -= 1
            pygame.event.post(pygame.event.Event(rocket2_hit))
            rocket1_bullets.remove(bullet)
        elif bullet.x < 0:
            rocket1_bullets.remove(bullet)
    for bullet1 in rocket1_bullets:
        for bullet2 in rocket2_bullets:
            if bullet1.colliderect(bullet2):
                rocket1_bullets.remove(bullet1)
                rocket2_bullets.remove(bullet2)

rocket1_bullets = []
rocket2_bullets = []

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, "black")
    screen.blit(draw_text, (900/2 - draw_text.get_width()/2, 500/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

clock = pygame.time.Clock()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_LCTRL:
                bullet = pygame.Rect(rocket2.rect.x + rocket2.rect.width, rocket2.rect.y + rocket2.rect.height/2 - 2, 10, 5)
                rocket2_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()
            if event.key == K_RCTRL:
                bullet = pygame.Rect(rocket1.rect.x + rocket1.rect.width, rocket1.rect.y + rocket1.rect.height/2 - 2, 10, 5)
                rocket1_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()
        
        if event.type == rocket1_hit:
            rocket1_health -= 1
            BULLET_HIT_SOUND.play()

        if event.type == rocket2_hit:
            rocket2_health -= 1
            BULLET_HIT_SOUND.play()
        
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_a]:
        rocket2.move_horizontal(-VEL, 1)
    if keys_pressed[K_d]:
        rocket2.move_horizontal(VEL, 1)
    if keys_pressed[K_w]:
        rocket2.move_vertical(-VEL)
    if keys_pressed[K_s]:
        rocket2.move_vertical(VEL)

    if keys_pressed[K_LEFT]:
        rocket1.move_horizontal(-VEL, 1)
    if keys_pressed[K_RIGHT]:
        rocket1.move_horizontal(VEL, 1)
    if keys_pressed[K_UP]:
        rocket1.move_vertical(-VEL)
    if keys_pressed[K_DOWN]:
        rocket1.move_vertical(VEL)
    
    draw_window()
    sprites.draw(screen)
    draw_bullets()
    handle_bullets()

    if rocket1_health <= 0:
        winner_text = "Rocket 2 Wins"
        draw_winner(winner_text)
    
    if rocket2_health <= 0:
        winner_text = "Rocket 1 Wins"
        draw_winner(winner_text)

    pygame.display.update()

pygame.quit()
