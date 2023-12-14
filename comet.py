# Imports
import sys
import math
import pygame
import time
from random import randint

# Constants
WIDTH = 1300
HEIGHT = 700
temp = False
GRAVITY = 2

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Font
font_type = pygame.font.Font('freesansbold.ttf',32)
text = font_type.render('F1 - Follow mode   F2 - Free mode  F3 - Gravity Mode', True, (250, 250, 250))
textRect = text.get_rect()
textRect.center = (WIDTH /2, 40)

# Classes

class Bullet:
    def __init__(self):
        self.bullet_speed = 10
        self.bullet_color = (100, 100, 100)
        self.shoot_state = False
        self.bullet_xs = []
        self.bullet_ys = []
        self.angles = []
        self.gravity = 10
        self.starting_times = []

    def event_check(self, x, y, b_x, b_y):

        if self.shoot_state:
            self.add_bullet(x, y, b_x, b_y)
            self.starting_times.append(time.time())

    def remove_bullets(self):

        if len(self.bullet_xs) > 0 and (self.bullet_xs[0] < 0 or self.bullet_xs[0] > WIDTH or  self.bullet_ys[0] > HEIGHT):

            del self.bullet_xs[0]
            del self.bullet_ys[0]
            del self.angles[0]
            del self.starting_times[0]


    def add_bullet(self, temp_hand_pos_x, temp_hand_pos_y, body_pos_x, body_pos_y):

        self.bullet_xs.append(temp_hand_pos_x)
        self.bullet_ys.append(temp_hand_pos_y)

        angle = math.atan2(temp_hand_pos_x - body_pos_x, temp_hand_pos_y - body_pos_y) + randint(0,5)/50

        self.angles.append(angle)

    def position_update(self, screen):
        for i in range(len(self.bullet_xs)):
            self.bullet_xs[i] += self.bullet_speed * math.sin(self.angles[i])
            self.bullet_ys[i] += self.bullet_speed * math.cos(self.angles[i]) + self.gravity * (time.time() - self.starting_times[i])
            self.draw_bullets(screen, i)

    def draw_bullets(self, screen, i):
        pygame.draw.circle(screen, self.bullet_color,(self.bullet_xs[i], self.bullet_ys[i]), 5)

class Player():

    def __init__(self, x, y):

        # Position
        self.x = x
        self.y = y
        self.velx = 0
        self.vely = 0

        # Hand
        self.hand_x=0
        self.hand_y=0
        self.hand_distance_from_center = 80

        self.head_diameter = 50
        self.head_color = (250, 120, 60)
        self.tail_color = (0, 100, 100)


        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False


        self.speed = 4
        self.friction = 0.1
        self.jump_accelerate = 10
        self.gravity = 0.25
        self.jump_time = time.time()

        self.mode = 0
        self.angle_in_radians = 0
        self.prev_angle = 0

        self.tail_xpos = []
        self.tail_ypos = []
        self.tail_len = 50

    def draw_hand(self, screen):
        tempx, tempy = pygame.mouse.get_pos()

        self.angle_in_radians = math.atan2(tempx - self.x, tempy - self.y)

        self.hand_x = self.hand_distance_from_center * math.sin(self.angle_in_radians) + self.x
        self.hand_y = self.hand_distance_from_center * math.cos(self.angle_in_radians) + self.y

        pygame.draw.circle(screen, self.head_color, (self.hand_x, self.hand_y), 10)

    def draw(self, screen):

        # Draw tail
        for i in range(len(self.tail_xpos)):
            if i%2:
                pygame.draw.circle(screen, self.tail_color, (self.tail_xpos[i], self.tail_ypos[i]), i/2)
            else:
                pygame.draw.circle(screen, (200, 100, 100), (self.tail_xpos[i], self.tail_ypos[i]), i/2)

        # Draw head
        pygame.draw.circle(screen, self.head_color, (self.x, self.y), self.head_diameter)

    def gravity_mode(self):

        if self.left_pressed and not self.right_pressed and not self.up_pressed and not self.down_pressed:
            if self.velx > -self.speed:
                self.velx -= self.friction

        if self.right_pressed and not self.left_pressed and not self.up_pressed and not self.down_pressed:
            if self.velx < self.speed:
                self.velx += self.friction

        if self.down_pressed and not self.up_pressed and not self.left_pressed and not self.right_pressed:
            if self.vely < self.speed:
                self.vely += self.friction



        # Friction
        if not self.left_pressed and self.velx < 0:
            self.velx += self.friction
            if self.velx > 0:
                self.velx = 0
        if not self.right_pressed and self.velx > 0:
            self.velx -= self.friction
            if self.velx < 0:
                self.velx = 0

        if not self.down_pressed and self.vely > 0:
            self.vely -= self.friction
            if self.vely < 0:
                self.vely = 0

        self.x += self.velx
        self.y += self.vely
        if self.y < HEIGHT- self.head_diameter/2:
            self.vely += self.gravity
            self.y += self.vely


    def arrow_mode(self):
        if self.left_pressed and not self.right_pressed and not self.up_pressed and not self.down_pressed:
            if self.velx > -self.speed:
                self.velx -= self.friction

        if self.right_pressed and not self.left_pressed and not self.up_pressed and not self.down_pressed:
            if self.velx < self.speed:
                self.velx += self.friction

        if self.up_pressed and not self.down_pressed and not self.left_pressed and not self.right_pressed:

            if self.vely > -self.speed:
                self.vely -= self.friction

        if self.down_pressed and not self.up_pressed and not self.left_pressed and not self.right_pressed:
            if self.vely < self.speed:
                self.vely += self.friction

        # Diagonal movement acceleration
        if self.right_pressed and self.up_pressed:
            if self.velx < +self.speed / math.sqrt(2):
                self.velx += self.friction / math.sqrt(2)

            if self.vely > -self.speed / math.sqrt(2):
                self.vely -= self.friction / math.sqrt(2)

        if self.right_pressed and self.down_pressed:
            if self.velx < +self.speed / math.sqrt(2):
                self.velx += self.friction / math.sqrt(2)

            if self.vely < +self.speed / math.sqrt(2):
                self.vely += self.friction / math.sqrt(2)

        if self.left_pressed and self.up_pressed:
            if self.velx > -self.speed / math.sqrt(2):
                self.velx -= self.friction / math.sqrt(2)

            if self.vely > -self.speed / math.sqrt(2):
                self.vely -= self.friction / math.sqrt(2)

        if self.left_pressed and self.down_pressed:
            if self.velx > -self.speed / math.sqrt(2):
                self.velx -= self.friction / math.sqrt(2)

            if self.vely < +self.speed / math.sqrt(2):
                self.vely += self.friction / math.sqrt(2)

        # Friction
        if not self.left_pressed and self.velx < 0:
            self.velx += self.friction
            if self.velx > 0:
                self.velx = 0
        if not self.right_pressed and self.velx > 0:
            self.velx -= self.friction
            if self.velx < 0:
                self.velx = 0
        if not self.up_pressed and self.vely < 0:
            self.vely += self.friction
            if self.vely > 0:
                self.vely = 0
        if not self.down_pressed and self.vely > 0:
            self.vely -= self.friction
            if self.vely < 0:
                self.vely = 0

        self.x += self.velx
        self.y += self.vely

    def follow_mode(self):


            tempx, tempy = pygame.mouse.get_pos()
            self.prev_angle = self.angle_in_radians
            self.angle_in_radians = math.atan2(tempx - self.x, tempy - self.y)

            self.velx = self.speed * math.sin(self.angle_in_radians)
            self.vely = self.speed * math.cos(self.angle_in_radians)




            self.x += self.velx
            self.y += self.vely

    def update(self):

        if self.mode == 0:
            self.follow_mode()

        elif self.mode == 1:
            self.arrow_mode()

        elif self.mode == 2:
            self.gravity_mode()


        # Window boundaries
        if self.x < player.head_diameter:
            self.x = player.head_diameter
        if self.x > WIDTH - player.head_diameter:
            self.x = WIDTH - player.head_diameter
        if self.y < player.head_diameter:
            self.y = player.head_diameter
        if self.y > HEIGHT - player.head_diameter:
            self.y = HEIGHT - player.head_diameter
            self. vely = 0

        self.rect = pygame.Rect(self.x, self.y, 20, 20)

        # Tail position
        if len(self.tail_xpos) < self.tail_len:
            self.tail_xpos.append(self.x)
            self.tail_ypos.append(self.y)
        else:
            self.tail_xpos.pop(0)
            self.tail_ypos.pop(0)




def check_events(player, bullets, temp):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.MOUSEBUTTONDOWN and not bullets.shoot_state:
            if pygame.mouse.get_pressed(3)[0]:
                bullets.shoot_state = True


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left_pressed = True
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True


            if event.key == pygame.K_UP:
                player.up_pressed = True

                if HEIGHT - player.y == player.head_diameter:
                    player.vely -= player.jump_accelerate
                    player.jump_time = time.time()

            if event.key == pygame.K_DOWN:
                player.down_pressed = True

            if event.key == pygame.K_F1:
                player.mode = 0
            if event.key == pygame.K_F2:
                player.mode = 1
            if event.key == pygame.K_F3:
                player.mode = 2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left_pressed = False
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
            if event.key == pygame.K_UP:
                player.up_pressed = False
            if event.key == pygame.K_DOWN:
                player.down_pressed = False

        if event.type == pygame.MOUSEBUTTONUP:

            bullets.shoot_state = False







# Objects innitialization

player = Player(490, 490)
player.draw(screen)
player.draw_hand(screen)
player.update()

bullets = Bullet()

# Main loop



while True:
    check_events(player, bullets, temp)

    screen.fill('black')
    screen.blit(text, textRect)
    player.draw(screen)
    player.draw_hand(screen)
    player.update()
    bullets.event_check(player.hand_x, player.hand_y, player.x, player.y)
    bullets.position_update(screen)
    bullets.remove_bullets()



    pygame.display.flip()
    clock.tick(120)
