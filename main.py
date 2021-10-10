import pygame
import time
import random

clock = pygame.time.Clock()
fps = 60
top= 90
top2=120

# game window
screen_width = 1366
screen_height = 768
pygame.init()
pygame.display.set_caption("Retro Battle")
screen = pygame.display.set_mode((screen_width, screen_height))  # +bottom_panel))
background_img = pygame.image.load("resources/Background/bg9.jfif").convert_alpha()
kunai = pygame.image.load("resources/Icons/kunai.png").convert_alpha()
kunai = pygame.transform.scale(kunai, (20,40))


# define fonts
font=pygame.font.SysFont('cursive',30)

#define game variables
current_player=1
total_players=3
action_cooldown=0
action_wait_time=90
attack = False
clicked = False

# define colors
red = (255,0,0)
green = (0,255,0)



# function to draw bg image
def draw_bg():
    screen.blit(background_img, (0, 0))

# draw panenl
# 255, 183, 197- sakura pink
def draw_panel():
    draw_text(f'{ninja.name} HP: {ninja.hp}',font, (235, 171, 227 ), 90, 120)# knight is a instance of fighter class
    for count, i in enumerate(bandit_list):
        #name and health
        draw_text(f'{i.name} HP: {i.hp}',font, ( 235, 171, 227 ), 1100, 120+count*30)#
   

# function to draw text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x, y))


# hero class
class fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.strength = strength
        self.max_hp = max_hp
        self.potions = potions
        self.hp = max_hp
        self.x = x
        self.y = y
        self.alive = True
        self.frame_index = 0
        self.animation_list = []
        self.action=0 #0-idle 1-Attack 2-Hurt 3-Dead
        self.update_time = pygame.time.get_ticks()

        # Add animation for Idle character
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'resources/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale( img, (100,100))
            temp_list.append(img)
        self.animation_list.append(temp_list)   

        # Add animation for attack
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'resources/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale( img, (100,100))
            temp_list.append(img)
        self.animation_list.append(temp_list) 

        # Add animation for Hurt
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'resources/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale( img, (100,100))
            temp_list.append(img)
        self.animation_list.append(temp_list) 
       

        # Add animation for Death
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'resources/{self.name}/Death/{i}.png')
            img = pygame.transform.scale( img, (100,100))
            temp_list.append(img)
        self.animation_list.append(temp_list) 

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)



    # animation image update
    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index>=len(self.animation_list[self.action]):
            self.idle()

    def idle(self):
        self.action=0
        self.frame_index=0
        self.update_time=pygame.time.get_ticks()



    def attack(self,target):
        rand=random.randint(-10,10)
        damage=self.strength+rand
        target.hp-=damage
        #check if target dead
        if target.hp < 1:
            target.hp = 0
            target.alive = False   

        self.action=1
        self.frame_index=0
        self.update_time=pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)




class health_bar():
    def __init__(self,x,y,hp,max_hp):
        self.x=x
        self.y=y
        self.hp=hp
        self.max_hp=max_hp

    def draw(self,hp):
        self.hp=hp    #update health
        ratio=self.hp/self.max_hp
        pygame.draw.rect(screen, (54, 55, 56), (self.x, self.y, 200, 10))
        pygame.draw.rect(screen, (163,21,146), (self.x, self.y, 200*ratio, 10))


ninja = fighter(180, 600, 'Ninja', 100, 10, 3)
bandit1 = fighter(1000, 590, 'Bandit', 50, 6, 1)
bandit2 = fighter(1080, 590, 'Bandit', 20, 6, 1)
bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)
ninja_health=health_bar(90,140, ninja.hp, ninja.max_hp)
bandit1_health=health_bar(1100, top2+20,bandit1.hp, bandit1.max_hp)
bandit2_health=health_bar(1100, top2+50,bandit2.hp, bandit2.max_hp)



run = True

while run:
    clock.tick(fps)
    # draw background
    draw_bg()
    draw_panel()


    # draw panel
    # draw_panel()

    # draw hero
    ninja.update()
    ninja.draw()
    ninja_health.draw(ninja.hp)
    bandit1_health.draw(bandit1.hp)
    bandit2_health.draw(bandit2.hp)

    for bandit in bandit_list:
        bandit.update()
        bandit.draw()


    #player action control

    attack = False
    target = None 

    #make mouse visible for each game iteration
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            #hide mousee
            pygame.mouse.set_visible(False)
            #show kunai instead of mouse
            screen.blit(kunai, pos)
            if clicked == True:
                attack = True
                target = bandit_list[count]
    #player action
    if ninja.alive == True:
        if current_player==1:
            action_cooldown+=1
            if action_cooldown >= action_wait_time:

                if attack == True and target != None:
                    ninja.attack(target)
                    current_player+=1
                    action_cooldown = 0

    for count, bandit in enumerate(bandit_list):
        if current_player == 2+count:
            if bandit.alive==True:
                action_cooldown+=1
                if action_cooldown >= action_wait_time:
                    bandit.attack(ninja)
                    current_player += 1
                    action_cooldown = 0
            else:
                current_player+=1
    #reset chance back to ninja
    if current_player>total_players:
        current_player=1



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()