import pygame
from fighter import Fighter

pygame.init()

#game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.update
pygame.display.set_caption("Figtherz")


#frame rate
clock = pygame.time.Clock()
FPS = 60

#define colors
YELLOW = (255,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

#define fighter varibles
#shadow 500 * 1050
SHADOW_SIZE = 50
SHADOW_SCALE = 3
SHADOW_OFFSET  = [10, 9]
SHADOW_DATA = [SHADOW_SIZE,SHADOW_SCALE, SHADOW_OFFSET]
#trunks 960 * 800
TRUNKS_SIZE = 80
TRUNKS_SCALE = 3
TRUNKS_OFFSET = [26,35]
TRUNKS_DATA = [TRUNKS_SIZE,TRUNKS_SCALE,TRUNKS_OFFSET]

#background image
bg_image = pygame.image.load("assets\images\stages\chamber 2.jpg").convert_alpha()

#spritesheets
shadow_sheet = pygame.image.load("assets\images\shadow\shadow spaced.xcf").convert_alpha()
trunks_sheet = pygame.image.load("assets\images\\trunks\swordsman spaced.xcf").convert_alpha()


#frames in each animation
#idle,jump,walk run, attack 1, attack 2, attack 3, charge attack, block, get hit, death, recover 1 , recover 2
SHADOW_ANIMATION_STEPS = [6,12,18,7,8,10,21,5,13,13]
KNUCKLES_ANIMATION_STEPS = [8,12,8,6,6,16,14,13,3,3,16,9]

#idle,jump,move front/back, attack 1 , attack 2, attack 3,charge attack,block, get hit, death,reset
TRUNKS_ANIMATION_STEPS = [7,7,2,4,6,4,10,3,4,8]
FRIEZA_ANIMATION_STEPS =[5,7,2,2,9,3,4,6,2,4,3,5]
#function for draw background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

#function for health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE,(x-3,y-3, 405, 35))
    pygame.draw.rect(screen, RED,(x,y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x,y, 400*ratio, 30))

#create both fighters
fighter_1 = Fighter(100, 310, False, SHADOW_DATA, shadow_sheet, SHADOW_ANIMATION_STEPS)
fighter_2 = Fighter(800, 310, True, TRUNKS_DATA, trunks_sheet, TRUNKS_ANIMATION_STEPS)

#game loop
open = True
while open:
    clock.tick(FPS)

    #call background function
    draw_bg()

    #show stats
    draw_health_bar(fighter_1.health, 20,20)
    draw_health_bar(fighter_2.health, 580,20)



    #move fighters
    fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen, fighter_2)
    #fighter_2.move()

    #update characters
    fighter_1.update()
    fighter_2.update()


    #draw fighters

    fighter_1.draw(screen)
    fighter_2.draw(screen)


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            open = False
    
    
    #update display
    pygame.display.update()

#exit pygame
pygame.quit()
quit()