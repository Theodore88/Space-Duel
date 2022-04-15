import os
from turtle import window_width
import pygame
import random
from pygame import mixer

from pygame import key

pygame.font.init()
pygame.mixer.init()

FPS = 60
WIDTH = 1500
HEIGHT = 800
BLACK_SHIP_WIDITH = 105
BLACK_SHIP_HEIGHT = 105
WHITE_SHIP_WIDITH = 110
WHITE_SHIP_HEIGHT = 100

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE= (255, 255 ,255)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

SHIP_VEL = 10
BULLET_VEL = 20

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Sounds and Images', 'Space.jpg')),(WIDTH, HEIGHT))

BLACK_SHIP = pygame.transform.scale(pygame.image.load(os.path.join('Sounds and Images','Black Ship.png')),(BLACK_SHIP_WIDITH, BLACK_SHIP_HEIGHT))
BLACK_SHIP_ROTATE = pygame.transform.rotate((BLACK_SHIP), 270)


WHITE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join('Sounds and Images', 'Blue Ship.png')),(WHITE_SHIP_WIDITH, WHITE_SHIP_HEIGHT))
WHITE_SHIP_ROTATE = pygame.transform.rotate((WHITE_SHIP), 90)

HEALTH_FONT = pygame.font.SysFont('arial', 40)
WINNER_FONT = pygame.font.SysFont('arial', 80)

LASER_SOUND = pygame.mixer.Sound(os.path.join('Sounds and Images','Laser Sound.wav'))
HIT_SOUND = pygame.mixer.Sound(os.path.join('Sounds and Images','Hit Sound.wav'))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join('Sounds and Images','Game Over Sound.wav'))


WIN = pygame.display.set_mode((WIDTH, HEIGHT))

black_ship_bullets_list = []
white_ship_bullets_list = []

BLACK_HIT = pygame.USEREVENT + 1
WHITE_HIT = pygame.USEREVENT + 2

def win(winner_text):
    text = WINNER_FONT.render(winner_text, 1, BLUE)
    if winner_text == "WHITE WINS!":
        WIN.blit(text, ((WIDTH//2) - 280 , (HEIGHT//2) - 100 ))

    if winner_text == "BLACK WINS!":
        WIN.blit(text, ((WIDTH//2) - 280 , (HEIGHT//2) - 100 ))
    
    pygame.display.update()
    pygame.time.delay(1500)
    black_ship_bullets_list.clear()
    white_ship_bullets_list.clear()
    main()

def edit_window(black_ship_rect, white_ship_rect, black_health, white_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.line(WIN, BLACK, ((WIDTH//2) - 40,0),((WIDTH//2) - 40, HEIGHT), 20)
    black_health= HEALTH_FONT.render(f'Black Health: {black_health}', 1, WHITE)
    white_health= HEALTH_FONT.render(f'White Health: {white_health}', 1, WHITE)
    WIN.blit(black_health, (10, 10))
    WIN.blit(white_health, (WIDTH - white_health.get_width() - 10,10))
    WIN.blit(BLACK_SHIP_ROTATE, (black_ship_rect.x,black_ship_rect.y))
    WIN.blit(WHITE_SHIP_ROTATE, (white_ship_rect.x, white_ship_rect.y))

    for bullet in black_ship_bullets_list:
            pygame.draw.rect(WIN, YELLOW, bullet)
    

    for bullet in white_ship_bullets_list:
        pygame.draw.rect(WIN, RED, bullet)
    

    pygame.display.update()

def movement(black_ship_rect, white_ship_rect):
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT] and white_ship_rect.x >= 0 and (white_ship_rect.x >= (WIDTH//2) - 20):    
        white_ship_rect.x -= SHIP_VEL
    
    if keys_pressed[pygame.K_RIGHT] and white_ship_rect.x <= WIDTH - WHITE_SHIP_WIDITH:    
        white_ship_rect.x += SHIP_VEL
    
    if keys_pressed[pygame.K_UP] and white_ship_rect.y >= 0:    
        white_ship_rect.y -= SHIP_VEL

    if keys_pressed[pygame.K_DOWN] and white_ship_rect.y <= HEIGHT - WHITE_SHIP_HEIGHT :    
        white_ship_rect.y += SHIP_VEL

    if keys_pressed[pygame.K_a] and black_ship_rect.x >= 0:    
        black_ship_rect.x -= SHIP_VEL
    
    if keys_pressed[pygame.K_d] and black_ship_rect.x <= WIDTH - BLACK_SHIP_WIDITH and black_ship_rect.x <= ((WIDTH//2) - 160):    
        black_ship_rect.x += SHIP_VEL
    
    if keys_pressed[pygame.K_w] and black_ship_rect.y >= 0:    
        black_ship_rect.y -= SHIP_VEL

    if keys_pressed[pygame.K_s] and black_ship_rect.y <= HEIGHT - BLACK_SHIP_HEIGHT :    
        black_ship_rect.y += SHIP_VEL

def shooting(black_ship_rect, white_ship_rect):
    
    for bullet in black_ship_bullets_list:
            bullet.x += BULLET_VEL
            if bullet.x > WIDTH:
                black_ship_bullets_list.remove(bullet)
            if white_ship_rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(WHITE_HIT))
                black_ship_bullets_list.remove(bullet)
                HIT_SOUND.play()
    
    for bullet in white_ship_bullets_list:
            bullet.x -= BULLET_VEL
            if bullet.x < 0:
                white_ship_bullets_list.remove(bullet)
            if black_ship_rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(BLACK_HIT))
                white_ship_bullets_list.remove(bullet)
                HIT_SOUND.play()
                



def main():
    black_ship_rect = pygame.Rect(160,300, BLACK_SHIP_WIDITH, BLACK_SHIP_HEIGHT)  
    white_ship_rect = pygame.Rect(1200,290, WHITE_SHIP_WIDITH, WHITE_SHIP_HEIGHT)
    black_health = 10
    white_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:  
        clock.tick(FPS) 
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(black_ship_bullets_list) < 3:
                    black_ship_bullet = pygame.Rect(black_ship_rect.x + BLACK_SHIP_WIDITH, (black_ship_rect.y + BLACK_SHIP_HEIGHT //2), 20, 5)  
                    black_ship_bullets_list.append(black_ship_bullet)
                    LASER_SOUND.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(white_ship_bullets_list) < 3:
                    white_ship_bullet = pygame.Rect(white_ship_rect.x - WHITE_SHIP_WIDITH + 100, (white_ship_rect.y + WHITE_SHIP_HEIGHT //2) , 20, 5)  
                    white_ship_bullets_list.append(white_ship_bullet)
                    LASER_SOUND.play()
              
            
            if event.type == BLACK_HIT:
                 black_health -= 1

            if event.type == WHITE_HIT:
                white_health -= 1
            
            winner_text = ""

            if black_health <= 0:
                winner_text = "WHITE WINS!"
                GAME_OVER_SOUND.play()
        
            if white_health <= 0:
                winner_text = "BLACK WINS!"
                GAME_OVER_SOUND.play()
            
            if winner_text != "":
                win(winner_text)
                break

        

        edit_window(black_ship_rect, white_ship_rect, black_health, white_health)
        movement(black_ship_rect, white_ship_rect)
        shooting(black_ship_rect, white_ship_rect)

    main()
    

if __name__ == "__main__":
    main()