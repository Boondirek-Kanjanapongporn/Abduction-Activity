import pygame
from pygame import mixer
import math as m
import random as r
import pickle
import math
import os
import sys

# Colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(250, 250, 250)
DARKGRAY = pygame.Color(169, 169, 169)
BLUE = pygame.Color(47, 141, 255)
DARKBLUE = pygame.Color(14, 77, 146)
CHERRYRED = pygame.Color(205, 0, 26)
DARKRED = pygame.Color(161, 0, 14)
YELLOW = pygame.Color(250, 202, 15)
WARNINGYELLOW = pygame.Color(238, 210, 2)
DARKYELLOW = pygame.Color(246, 190, 0)
COINYELLOW = pygame.Color(235, 196, 27)
ORANGE = pygame.Color(255, 165, 0)
DARKORANGE = pygame.Color(230, 126, 0)
YELLOWORANGE = pygame.Color(255, 174, 66)
REDORANGE = pygame.Color(255, 69, 0)

# Resources Path
RESOURCESPATH = "resources/"

# Initialize the pygame
pygame.init()

USER_INPUT = ""

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

data_path = resource_path("data.dat")

if os.path.exists(data_path):
    with open(data_path, "rb") as file:
        DATA_DICT = pickle.load(file)
        print("Data loaded successfully")
else:
    print("ERROR: Could not find data.dat")

USER_DICT = {}

# Essential Variables
FPS = 60
CURRENT_SCREEN = 'START'
LIFE = 3
ABDUCTIONSCORE = 0
FINALSCORE = 0
BATTERIES = 5
COINGAIN = 0
EXTRACOIN = 0
CLOCK = pygame.time.Clock()
CURRENT_TIME = 0
HUMANRELOAD = 150
HUMAN_BENCH_LIST = []
BATAMOUNTS = 1
SKIN = 0
HUMANLEVEL2 = 0
HUMANLEVEL3 = 0
BATLEVEL2 = False
BATLEVEL3 = False
BATSPAWN_NONLINEAR_PROGRESS = 1
WHEN_BAT_SHOULD_SPAWN = 10

# Fonts
GLOBAL_FONT = pygame.font.SysFont('candara', 30)
TEXT_FONT = pygame.font.SysFont('candara', 25)
SCORE_FONT = pygame.font.SysFont('impact', 35)
BUTTON_FONT = pygame.font.SysFont('impact', 25)
WARNING_FONT = pygame.font.SysFont('impact', 20)

# Create the screen
screenWidth = 720
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Title and Icon
pygame.display.set_caption("Abduction Activity")
icon = pygame.image.load(resource_path(RESOURCESPATH + "UFO_abduction.png"))
pygame.display.set_icon(icon)
logoImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "alien warning.png")), (187, 163))
titleImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "title.png")), (500, 73))
gameoverImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "gameover.png")), (406, 75))
restartImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "restart.png")), (250, 36))
right_arrow = pygame.image.load(resource_path(RESOURCESPATH + "right_arrow.png"))
left_arrow = pygame.image.load(resource_path(RESOURCESPATH + "left_arrow.png"))
# enterImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "enter.png")), (110, 42))

# Adding Sound Effects
start_music = mixer.Sound(resource_path(RESOURCESPATH + "Silent Owl.mp3"))
background_music = mixer.Sound(resource_path(RESOURCESPATH + "MoriCalliopeBGM.mp3"))
explosion_sound = mixer.Sound(resource_path(RESOURCESPATH + "Explosion effect.wav"))
hit_sound = mixer.Sound(resource_path(RESOURCESPATH + "Hit effect.mp3"))
start_music.set_volume(0.05)
background_music.set_volume(0.05)
explosion_sound.set_volume(0.08)

# Login/Signup Booleans
SIGN_UP = False
loginWarning = False
signupWarning = False
signupSuccess = False

# Login/ Signup Textbox/ Text
login_text = GLOBAL_FONT.render("LOGIN: ", True, BLACK)
login_button_text = BUTTON_FONT.render("LOGIN", True, WHITE)
signup_text = GLOBAL_FONT.render("SIGN UP: ", True, BLACK)
signup_button_text = BUTTON_FONT.render("SIGN UP", True, WHITE)
username_text = GLOBAL_FONT.render("Username: ", True, WHITE)
loginWarning_text = WARNING_FONT.render("**Username not found!!!", True, CHERRYRED)
loginWarning_text2 = WARNING_FONT.render("Please Sign-up or Re-enter Username...", True, CHERRYRED)
signupWarning_text = WARNING_FONT.render("**Username already exist!!!", True, CHERRYRED)
signupWarning_text2 = WARNING_FONT.render("Please Login or Re-enter New Username...", True, CHERRYRED)
signupSuccess_text = WARNING_FONT.render("**Sign-up Successfully!!!", True, BLUE)
signupSuccess_text2 = WARNING_FONT.render("Please try to Login", True, BLUE)

# Rectangles Login/Sign Up
background_rect = pygame.rect.Rect(150, 25, screenWidth-300, screenHeight-50)
login_rect = pygame.rect.Rect(150, 45, screenWidth-300, 35)
signup_rect = pygame.rect.Rect(150, 45, screenWidth-300, 35)
username_textbox = pygame.rect.Rect(350, 95, 200, 40)
login_button = pygame.rect.Rect(185, 350, 160, 40)
signup_button = pygame.rect.Rect(375, 349, 160, 40)
box_border = pygame.Rect(350, 95, 200, 40)

# Main Menu Booleans and shop indexes
MENU_PAGE = 'map'
SHOP_BUTTON = 'ufo'

# Shop Indexes
ufo_index = 0
ufo0_name = TEXT_FONT.render("Default UFO", True, WHITE)
ufo0_image = pygame.image.load(resource_path(RESOURCESPATH + "ufo0.png"))
ufo1_name = TEXT_FONT.render("Radio UFO", True, WHITE)
ufo1_cost = BUTTON_FONT.render("Cost: 500", True, COINYELLOW)
ufo1_image = pygame.image.load(resource_path(RESOURCESPATH + "ufo1.png"))
ufo2_name = TEXT_FONT.render("Hi-Tech UFO", True, WHITE)
ufo2_cost = BUTTON_FONT.render("Cost: 1000", True, COINYELLOW)
ufo2_image = pygame.image.load(resource_path(RESOURCESPATH + "ufo2.png"))

upgrades_index = 0
human_image = pygame.image.load(resource_path(RESOURCESPATH + "sprite-run1.png"))
upgrades0_name = TEXT_FONT.render("Heart Amount", True, WHITE)
upgrades0_cost = BUTTON_FONT.render("Cost: 200", True, COINYELLOW)
upgrades0_image = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "heart.png")), (128, 128))
upgrades1_name = TEXT_FONT.render("Reduce Human Rate", True, WHITE)
upgrades1_cost = BUTTON_FONT.render("Cost: 200", True, COINYELLOW)
upgrades2_name = TEXT_FONT.render("Reduce Bat Rate", True, WHITE)
upgrades2_cost = BUTTON_FONT.render("Cost: 200", True, COINYELLOW)
upgrades2_image = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-fly1.png")), (128, 128))

skin_index = 0
skin0_name = TEXT_FONT.render("Invisible Hat", True, WHITE)
skin1_name = TEXT_FONT.render("Christmas Hat", True, WHITE)
skin1_cost = BUTTON_FONT.render("Cost: 150", True, COINYELLOW)
skin1_image = pygame.image.load(resource_path(RESOURCESPATH + "christmas-hat.png"))
skin2_name = TEXT_FONT.render("Birthday Hat", True, WHITE)
skin2_cost = BUTTON_FONT.render("Cost: 250", True, COINYELLOW)
skin2_image = pygame.image.load(resource_path(RESOURCESPATH + "birthday-hat.png"))

# Main Menu Text
back_space_textW = WARNING_FONT.render("Press [Backspace] to Login Again", True, WHITE)
map_button_textW = GLOBAL_FONT.render("MAP", True, WHITE)
map_button_textB = GLOBAL_FONT.render("MAP", True, BLACK)
shop_button_textW = GLOBAL_FONT.render("SHOP", True, WHITE)
shop_button_textB = GLOBAL_FONT.render("SHOP", True, BLACK)
manual_button_textW = GLOBAL_FONT.render("MANUAL", True, WHITE)
manual_button_textB = GLOBAL_FONT.render("MANUAL", True, BLACK)
mysterious_forest_text = GLOBAL_FONT.render("THE MYSTERIOUS WOODS", True, WHITE)
play_button_textB = BUTTON_FONT.render("PLAY", True, BLACK)
rules_text = GLOBAL_FONT.render("RULES:", True, WHITE)
rules1_text = TEXT_FONT.render("1. When start, HEART: 3 and BATTERY: 5", True, WHITE)
rules2_text = TEXT_FONT.render("2. Press W, A, S, or D to move", True, WHITE)
rules3_text = TEXT_FONT.render("3. Press [SPACE] to abduct humans", True, WHITE)
rules4_text = TEXT_FONT.render("4. Capture all Humans while avoiding Bats", True, WHITE)
rules5_text = TEXT_FONT.render("5. Pick up Accumulator to charge Battery", True, WHITE)
rules6_text = TEXT_FONT.render("6. Collide Human to Bat -> HEART -= 1", True, WHITE)
rules7_text = TEXT_FONT.render("7. Press [SPACE] -> BATTERY -= 1", True, WHITE)
ufo_button_textW = BUTTON_FONT.render("UFO", True, WHITE)
ufo_button_textB = BUTTON_FONT.render("UFO", True, BLACK)
upgrades_button_textW = BUTTON_FONT.render("UPGRADES", True, WHITE)
upgrades_button_textB = BUTTON_FONT.render("UPGRADES", True, BLACK)
skin_button_textW = BUTTON_FONT.render("SKIN", True, WHITE)
skin_button_textB = BUTTON_FONT.render("SKIN", True, BLACK)
buy_button_textB = BUTTON_FONT.render("BUY", True, BLACK)
choose_button_textB = BUTTON_FONT.render("CHOOSE", True, BLACK)
max_button_textB = BUTTON_FONT.render("MAX", True, BLACK)
in_use_text = BUTTON_FONT.render("In Use", True, COINYELLOW)

# Rectangles Main Menu
mainmenu_rect = pygame.rect.Rect(75, 60, screenWidth-150, screenHeight-120)
map_button = pygame.rect.Rect(75, 60, (screenWidth-150)/3, 50)
shop_button = pygame.rect.Rect(265, 60, (screenWidth-150)/3, 50)
manual_button = pygame.rect.Rect(455, 60, (screenWidth-150)/3, 50)
play_button = pygame.rect.Rect(285, 355, 160, 40)
ufo_button = pygame.rect.Rect(110, 165, 150, 45)
upgrades_button = pygame.rect.Rect(110, 220, 150, 45)
skin_button = pygame.rect.Rect(110, 275, 150, 45)
shop_rect = pygame.rect.Rect(285, 150, 335, 210)
buy_button = pygame.rect.Rect(383, 370, 140, 40)
coin_rect = pygame.rect.Rect(510, 118, 110, 25)

# Background image
backgroundImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "cartoon-night-forest.png")), (screenWidth, screenHeight+20))
backgroundImg2 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "cartoon-night-forest.png")), (290, 177))
scrollingBack = 0

# Heart life
heartImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "heart.png")), (39, 39))

# Score
SCORESIZE = 50
SCOREFONT = pygame.font.SysFont('impact', SCORESIZE)
SCOREX = screenWidth/2 - 15
SCOREY = 5
# print(pygame.font.get_fonts())

# Battery image
BatteryList = []
battery0 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "battery0.png")), (45, 75))
battery1 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "battery1.png")), (45, 75))
battery2 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "battery2.png")), (45, 75))
battery3 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "battery3.png")), (45, 75))
battery4 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "battery4.png")), (45, 75))
battery5 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "battery5.png")), (45, 75))
BatteryList.append(battery0)
BatteryList.append(battery1)
BatteryList.append(battery2)
BatteryList.append(battery3)
BatteryList.append(battery4)
BatteryList.append(battery5)

# UFO image
ufoImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "ufo0.png")), (64, 64))
PLAYERX = screenWidth / 2 - 32
PLAYERY = screenHeight / 2 - 32
PLAYERSPEED = 4
W_change = 0
A_change = 0
S_change = 0
D_change = 0

# Ufo beam (Ready/Fire) image
beamImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "yellow-beam.png")), (90, 100))
BEAMX = 0
BEAMY = 0
beam_tick = 0
beam_state = 'ready'

# Battery Accumulator image
accumulatorImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "accumulator1.png")), (32, 32))
ACCUMULATORX = r.randint(10, screenWidth-32)
ACCUMULATORY = r.randint(0, int(screenHeight/2))
accumulator_tick = 0
accumulator_cooldown = False

# Coin image
coinImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "Coin1.png")), (25, 26))
coin1Img = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "Coin1.png")), (16, 17))
COINX = r.randint(10, screenWidth-25)
COINY = r.randint(0, int(screenHeight/1.5))
coin_tick = 0
coin_cooldown = False

# Explosion image
explosionImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "explosion.png")), (108, 98))
explode_state = 'ready'
explosion_tick = 0

# Bat Sprite
bat1 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-fly1.png")), (48, 48))
bat2 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-fly2.png")), (48, 48))
bat3 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-fly3.png")), (48, 48))
bat4 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-fly4.png")), (48, 48))
BATX = screenWidth
BATY = r.randint(0, int(screenHeight/1.5))
target_BATY = PLAYERY
count = 0

# Bat class
class Bat_animation(pygame.sprite.Sprite):
    def __init__(self, x, y, state):
        super().__init__()
        self.x = x
        self.y = y
        self.state = state
        self.bat_motion = []
        self.bat_motion.append(bat1)
        self.bat_motion.append(bat2)
        self.bat_motion.append(bat3)
        self.bat_motion.append(bat4)
        self.current = 0
        self.image = self.bat_motion[self.current]

        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

    def isCollision(self):
        # global PLAYERX, PLAYERY
        distance = m.sqrt(pow(self.x - PLAYERX, 2) + pow(self.y - PLAYERY-8, 2))
        if distance <= 40:
            return True
        return False

    def update(self):
        global LIFE
        # bat animation speed
        self.current += 0.16

        # bat flying speed
        self.x += -3
        if self.current >= len(self.bat_motion):
            self.current = 0

        # updating animation and x axis
        self.image = self.bat_motion[int(self.current)]
        self.rect.topleft = [self.x, self.y]

        # bat end loop boundaries
        if self.x <= -16:
            self.x = screenWidth
            if self.state == 'target':
                self.y = PLAYERY
            else:
                self.y = r.randint(0, int(screenHeight / 1.5))

        # Sprite-bat collision
        if self.isCollision():
            if LIFE > 1:
                hit_sound.play()
            self.x = screenWidth
            if self.state == 'target':
                self.y = PLAYERY
            else:
                self.y = r.randint(0, int(screenHeight/1.5))
            LIFE -= 1


# setting Bat Sprite class and groups
animated_bats = pygame.sprite.Group()
bat_sprite = Bat_animation(BATX, BATY, 'normal')
animated_bats.add(bat_sprite)

# Human Sprite
skinImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "christmas-hat.png")), (16, 16))
sprite1 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-run1.png")), (35, 50))
sprite2 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-run2.png")), (35, 50))
sprite3 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-run3.png")), (35, 50))
sprite4 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-run4.png")), (35, 50))
sprite5 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-run5.png")), (35, 50))
sprite6 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-run6.png")), (35, 50))
sprite7 = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "sprite-run7.png")), (35, 50))
SPRITEX = screenWidth
SPRITEY = 400

# Human Class
class Humansprite_animation(pygame.sprite.Sprite):
    def __init__(self, x, y, state, skin):
        super().__init__()
        self.x = x
        self.y = y
        self.state = state
        self.skin = skin
        if self.state == 'title':
            self.speed = 0
        else:
            self.speed = - (r.randint(1, 2) + r.randint(0, 9)/10)
        # print(self.speed)
        self.sprite_motion = []
        self.sprite_motion.append(sprite1)
        self.sprite_motion.append(sprite2)
        self.sprite_motion.append(sprite3)
        self.sprite_motion.append(sprite4)
        self.sprite_motion.append(sprite5)
        self.sprite_motion.append(sprite6)
        self.sprite_motion.append(sprite7)
        self.current = 0
        self.image = self.sprite_motion[self.current]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    def isCollision(self):
        # global BEAMX, BEAMY
        distance = m.sqrt(pow(self.x - BEAMX-20, 2) + pow(self.y - BEAMY-5, 2))
        if distance <= 40:
            return True
        return False

    def update(self):
        global ABDUCTIONSCORE
        global beam_state
        global beam_tick
        if self.skin == 1:
            screen.blit(skinImg, (self.x+13, self.y-8))
        elif self.skin == 2:
            screen.blit(skinImg, (self.x + 14, self.y - 9))
        # animation per frame speed
        self.current += 0.6
        # Sprite running speed
        # self.x += -2.4
        self.x += self.speed
        if self.current >= len(self.sprite_motion):
            self.current = 0

        # updating animation and x axis
        self.image = self.sprite_motion[int(self.current)]
        self.rect.topleft = [self.x, self.y]

        # sprite end boundaries
        if self.x <= -16:
            self.kill()
            ABDUCTIONSCORE -= 1

        # Sprite-beam collision
        if beam_state == 'fire':
            if self.isCollision():
                self.kill()
                ABDUCTIONSCORE += 1
                beam_state = 'ready'
                beam_tick = 0


# the only sprite in the title page
title_sprite = pygame.sprite.Group()
title_human = Humansprite_animation(screenWidth/2 - 15, SPRITEY, 'title', 0)
title_sprite.add(title_human)

# setting Human Sprite class, group, and reload
animated_sprites = pygame.sprite.Group()
human_reload = HUMANRELOAD
# human_sprite = Humansprite_animation(SPRITEX, SPRITEY, 'normal', skin_index)
# animated_sprites.add(human_sprite)


def saveDataDict():
    with open(data_path, "wb") as f:
        pickle.dump(DATA_DICT, f)


def city_background(x, y):
    screen.blit(backgroundImg, (x, y))


def logo(x, y):
    screen.blit(logoImg, (x, y))


def title(x1, y1, x2, y2):
    screen.blit(titleImg, (x1, y1))
    enter_sign = SCORE_FONT.render("Press [Enter] to Login", True, WHITE)
    if -0.80 < m.sin(CURRENT_TIME/200) < 1:
        screen.blit(enter_sign, (x2, y2))


def gameover(x1, y1, x2, y2):
    screen.blit(gameoverImg, (x1, y1))
    replay_sign = SCORE_FONT.render("Press [Enter] to Main Menu", True, WHITE)
    screen.blit(replay_sign, (x2, y2))


def playerlife():
    # global LIFE
    if LIFE >= 1:
        screen.blit(heartImg, (screenWidth-39, 0))
    if LIFE >= 2:
        screen.blit(heartImg, (screenWidth-78, 0))
    if LIFE >= 3:
        screen.blit(heartImg, (screenWidth-117, 0))
    if LIFE >= 4:
        screen.blit(heartImg, (screenWidth-156, 0))
    if LIFE >= 5:
        screen.blit(heartImg, (screenWidth-195, 0))
    else:
        pass


def show_score(x, y, state):
    score = SCOREFONT.render(str(state), True, WHITE)
    screen.blit(score, (x, y))


def show_coingain(x, y, state):
    coingain = BUTTON_FONT.render("Coin: " + str(state), True, COINYELLOW)
    screen.blit(coingain, (x, y))


def batterylife(x, y):
    global BATTERIES
    if BATTERIES == -1:
        BATTERIES = 0
    screen.blit(BatteryList[BATTERIES], (x, y))


def ufo(x, y):
    screen.blit(ufoImg, (x, y))


def fire_beam(x, y):
    screen.blit(beamImg, (x, y))


def accumulator(x, y):
    screen.blit(accumulatorImg, (x, y))


def isUFOACCCollision(playerx, playery, accumulatorx, accumulatory):
    distance = m.sqrt(pow(playerx - accumulatorx+20, 2) + pow(playery - accumulatory, 2))
    if distance <= 35:
        return True
    return False


def coin(x, y):
    screen.blit(coinImg, (x, y))


def isUFOCoinCollision(playerx, playery, coinx, coiny):
    distance = m.sqrt(pow(playerx - coinx+20, 2) + pow(playery - coiny+15, 2))
    if distance <= 35:
        return True
    return False


def explosion(x, y):
    screen.blit(explosionImg, (x, y))


# Game loop
# Load data
running = True
start_music.play(-1)
while running:

    screen.fill((255, 255, 255))
    CURRENT_TIME = pygame.time.get_ticks()
    mouseX, mouseY = pygame.mouse.get_pos()

    # defining background animation
    scrollingBack -= 0.8
    if scrollingBack <= -screenWidth:
        scrollingBack = 0

    # Draw background by position of the generated background
    city_background(scrollingBack, 0)
    city_background(screenWidth + scrollingBack, 0)

    # START screen ------------------------------------------------------------------------------------
    if CURRENT_SCREEN == 'START':

        # Draw Logo and Title
        logo(screenWidth/3+25, screenHeight/7)
        title(screenWidth/7+7, screenHeight/2, screenWidth/4 + 30, screenHeight/2+70)

        # Draw Title Human Sprite
        title_sprite.draw(screen)
        title_sprite.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    CURRENT_SCREEN = 'LOGIN'

    # LOGIN screen -------------------------------------------------------------------------------------
    if CURRENT_SCREEN == 'LOGIN':

        # Draw Background rect and Username textbox
        username_input_text = BUTTON_FONT.render(USER_INPUT, True, BLACK)
        pygame.draw.rect(screen, BLACK, background_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, username_textbox, border_radius=10)
        screen.blit(username_input_text, (360, 100))
        screen.blit(username_text, (200, 100))

        # Check if mouse is over username textbox
        if 350 <= mouseX <= 550 and 95 <= mouseY <= 135:
            mouseOnTextbox = True
            pygame.draw.rect(screen, DARKRED, box_border, 2, border_radius=10)
        else:
            mouseOnTextbox = False

        # Login Button + Animation
        if 185 <= mouseX <= 345 and 350 <= mouseY <= 390:
            pygame.draw.rect(screen, DARKRED, login_button, border_radius=15)
        else:
            pygame.draw.rect(screen, CHERRYRED, login_button, border_radius=15)

        # Signup Button + Animation
        if 375 <= mouseX <= 535 and 349 <= mouseY <= 389:
            pygame.draw.rect(screen, DARKBLUE, signup_button, border_radius=15)
        else:
            pygame.draw.rect(screen, BLUE, signup_button, border_radius=15)

        # Login and Signup Button Text
        screen.blit(login_button_text, (235, 353))
        screen.blit(signup_button_text, (415, 354))

        # Change between Login and Signup page
        if not SIGN_UP:
            pygame.draw.rect(screen, CHERRYRED, login_rect)
            screen.blit(login_text, (165, 50))
            # No username in data.dat warning
            if loginWarning:
                screen.blit(loginWarning_text, (165, 200))
                screen.blit(loginWarning_text2, (178, 220))
        else:
            pygame.draw.rect(screen, BLUE, signup_rect)
            screen.blit(signup_text, (165, 50))
            if signupWarning:
                screen.blit(signupWarning_text, (165, 200))
                screen.blit(signupWarning_text2, (178, 220))
            if signupSuccess:
                screen.blit(signupSuccess_text, (165, 200))
                screen.blit(signupSuccess_text2, (178, 220))

        # Capture Pygame Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()        # Used for Capital letter keys
                # Check Mouse hovers over Username textbox
                if mouseOnTextbox:
                    if len(USER_INPUT) < 10:        # Username can't be over 10 letters
                        if 48 <= event.key <= 57 or 97 <= event.key <= 122:         # Check pressed keys on Textbox
                            # Check for Shift or Capital keys
                            if 97 <= event.key <= 122 and mods & pygame.KMOD_LSHIFT or mods & pygame.KMOD_CAPS:
                                USER_INPUT += chr(event.key-32)
                            else:
                                USER_INPUT += chr(event.key)        # Not Capital Letter
                    if event.key == pygame.K_BACKSPACE:             # Capture Backspace key
                        if len(USER_INPUT) > 0:
                            USER_INPUT = USER_INPUT[:-1]            # Erase last letter in USER_INPUT
                    # print(USER_INPUT)

            if event.type == pygame.MOUSEBUTTONUP:
                # if Login Page:
                if not SIGN_UP:
                    if 185 <= mouseX <= 345 and 350 <= mouseY <= 390:
                        # print("Login pressed")
                        # Read data.dat file and load into Data_Dict
                        with open(data_path, "rb") as f:
                            DATA_DICT = pickle.load(f)

                        # If user_input in data.dat and not empty string
                        if USER_INPUT in DATA_DICT.keys() and len(USER_INPUT) != 0:
                            # print("Login Successfully")
                            USER_DICT = DATA_DICT[USER_INPUT]
                            loginWarning = False
                            signupWarning = False
                            signupSuccess = False
                            CURRENT_SCREEN = 'MAIN MENU'
                        else:
                            loginWarning = True
                            # print("Login Unsuccessfully")

                    # Change from Login Page to Signup Page
                    if 375 <= mouseX <= 535 and 349 <= mouseY <= 389:
                        # print("Signup pressed")
                        loginWarning = False
                        SIGN_UP = True
                else:
                    # Signup Page
                    if 185 <= mouseX <= 345 and 350 <= mouseY <= 390:
                        # print("Login pressed")
                        SIGN_UP = False
                        signupWarning = False
                        signupSuccess = False
                    if 375 <= mouseX <= 535 and 349 <= mouseY <= 389:
                        # print("Signup pressed")
                        # User_input already in data.dat
                        if USER_INPUT in DATA_DICT.keys():
                            signupWarning = True
                            signupSuccess = False
                        else:
                            USER_DICT["username"] = USER_INPUT      # add new User_input into data.dat and saveDatDic
                            USER_DICT["score"] = 0
                            USER_DICT["coin"] = 0
                            USER_DICT["life"] = 3
                            USER_DICT["human"] = 1
                            USER_DICT["bat"] = 1
                            USER_DICT["ufo0"] = 1
                            USER_DICT["skin0"] = 1
                            DATA_DICT[USER_INPUT] = USER_DICT
                            saveDataDict()
                            signupWarning = False
                            signupSuccess = True

    # MAIN MENU screen ---------------------------------------------------------------------------------
    if CURRENT_SCREEN == 'MAIN MENU':

        # Draw Main rectangle/ Backspace to Login/ Map button/ Shop button/ Manual button text (The one on top)
        pygame.draw.rect(screen, BLACK, mainmenu_rect)
        screen.blit(back_space_textW, (10, 5))
        screen.blit(map_button_textW, (139, 70))
        screen.blit(shop_button_textW, (325, 70))
        screen.blit(manual_button_textW, (495, 70))

        # Menu Page Conditions
        # if Menu_page is in map
        if MENU_PAGE == 'map':
            pygame.draw.rect(screen, WARNINGYELLOW, map_button)         # Draw Yellow Rectangle on Map button on top
            # pygame.draw.rect(screen, WHITE, map_button, 3)
            screen.blit(map_button_textB, (139, 70))                    # Draw Black Map text on top
            screen.blit(mysterious_forest_text, (195, 125))             # Name of map "The Mysterious Forest"
            screen.blit(backgroundImg2, (217, 165))                     # Picture below the name of the text

            # Display HighScore
            score_text = WARNING_FONT.render("HighScore: " + str(USER_DICT['score']), True, DARKRED)
            screen.blit(score_text, (515, 165))

            # Play button animation
            if 285 <= mouseX <= 445 and 355 <= mouseY <= 395:
                pygame.draw.rect(screen, DARKYELLOW, play_button, border_radius=15)
                screen.blit(play_button_textB, (340, 359))
            else:
                pygame.draw.rect(screen, WARNINGYELLOW, play_button, border_radius=15)
                screen.blit(play_button_textB, (340, 359))

        # if Menu_page is in shop
        elif MENU_PAGE == 'shop':
            # pygame.draw.rect(screen, WHITE, store_button, 3)
            pygame.draw.rect(screen, WARNINGYELLOW, shop_button)        # Draw Yellow Rectangle on Shop button on top
            pygame.draw.rect(screen, WHITE, shop_rect, 1)               # Draw White Border Rectangle to displays items
            screen.blit(right_arrow, (565, 225))                        # Right Arrow to change items
            screen.blit(left_arrow, (290, 225))                         # Left Arrow to change items

            # Display Coin amount
            coin_text = WARNING_FONT.render(str(USER_DICT['coin']), True, COINYELLOW)       # Update Coin amount
            pygame.draw.rect(screen, WHITE, coin_rect, border_radius=15)                    # Coin White background
            screen.blit(coin1Img, (519, 121))                                               # Coin image besides number
            screen.blit(coin_text, (540, 117))                                              # Amount of Coin

            # Buy/Choose Button animation
            if 383 <= mouseX <= 523 and 370 <= mouseY <= 410:
                pygame.draw.rect(screen, DARKORANGE, buy_button, border_radius=15)
            else:
                pygame.draw.rect(screen, ORANGE, buy_button, border_radius=15)

            # Button Texts
            screen.blit(shop_button_textB, (325, 70))                                   # Shop Button Text
            screen.blit(ufo_button_textW, (165, 173))                                   # Ufo Button Text
            screen.blit(upgrades_button_textW, (134, 227))                              # Upgrades Button Text
            screen.blit(skin_button_textW, (161, 282))                                  # Skin Button Text

            # if Shop_button is ufo page
            if SHOP_BUTTON == 'ufo':
                pygame.draw.rect(screen, ORANGE, ufo_button)                            # Orange color on ufo button
                screen.blit(ufo_button_textB, (165, 173))                               # Black text on Ufo button

                # Default Ufo page
                if ufo_index == 0:
                    screen.blit(ufo0_name, (390, 160))
                    screen.blit(ufo0_image, (388, 190))
                    # if "ufo0" in USER_DICT.keys():
                    if USER_DICT["ufo0"] == 1:                                          # If default ufo is in use
                        screen.blit(in_use_text, (420, 315))
                    screen.blit(choose_button_textB, (413, 375))
                    # else:
                    # screen.blit(buy_button_textB, (431, 375))

                # Radio Ufo page
                elif ufo_index == 1:
                    screen.blit(ufo1_name, (395, 160))
                    screen.blit(ufo1_image, (388, 190))
                    if "ufo1" in USER_DICT.keys():                              # If already purchase Radio ufo
                        if USER_DICT["ufo1"] == 1:                              # If Radio ufo is chosen
                            screen.blit(in_use_text, (420, 315))
                        screen.blit(choose_button_textB, (413, 375))
                    else:
                        screen.blit(ufo1_cost, (405, 315))                      # Cost and Buy button
                        screen.blit(buy_button_textB, (431, 375))

                # Hi-Tech Ufo Page
                elif ufo_index == 2:
                    screen.blit(ufo2_name, (390, 160))
                    screen.blit(ufo2_image, (388, 190))
                    if "ufo2" in USER_DICT.keys():                              # If already purchase Hi-Tech Ufo
                        if USER_DICT["ufo2"] == 1:                              # IF Hi-Tech ufo is chosen
                            screen.blit(in_use_text, (420, 315))
                        screen.blit(choose_button_textB, (413, 375))
                    else:
                        screen.blit(ufo2_cost, (400, 315))                      # Cost and Buy Button
                        screen.blit(buy_button_textB, (431, 375))

            # if Shop_button is is upgrades page
            elif SHOP_BUTTON == 'upgrades':

                # Update upgrade levels to Max every run
                heartlevel_button_textB = BUTTON_FONT.render("lvl " + str(USER_DICT["life"] - 2), True, BLACK)
                humanlevel_button_textB = BUTTON_FONT.render("lvl " + str(USER_DICT["human"]), True, BLACK)
                batlevel_button_textB = BUTTON_FONT.render("lvl " + str(USER_DICT["bat"]), True, BLACK)

                pygame.draw.rect(screen, ORANGE, upgrades_button)               # Orange Color on upgrades button
                screen.blit(upgrades_button_textB, (134, 227))                  # Black text on upgrades

                # Heart/Life upgrades page
                if upgrades_index == 0:
                    screen.blit(upgrades0_name, (380, 160))
                    screen.blit(upgrades0_image, (388, 190))
                    if USER_DICT["life"] == 5:                                  # If Heart/life upgrades is at Max level
                        screen.blit(max_button_textB, (429, 375))
                    else:
                        screen.blit(upgrades0_cost, (405, 315))                 # Cost and Buy Button
                        screen.blit(heartlevel_button_textB, (433, 375))

                # Human upgrades page
                elif upgrades_index == 1:
                    screen.blit(upgrades1_name, (348, 160))
                    screen.blit(human_image, (410, 200))
                    if USER_DICT["human"] == 3:                                 # If human upgrades is at max level
                        screen.blit(max_button_textB, (429, 375))
                    else:
                        screen.blit(upgrades1_cost, (405, 315))                 # Cost and Buy Button
                        screen.blit(humanlevel_button_textB, (433, 375))

                # Bat upgrades page
                elif upgrades_index == 2:
                    screen.blit(upgrades2_name, (365, 160))
                    screen.blit(upgrades2_image, (388, 195))
                    if USER_DICT["bat"] == 3:                                   # If bat upgrades is at max level
                        screen.blit(max_button_textB, (429, 375))
                    else:
                        screen.blit(upgrades2_cost, (405, 315))                 # Cost and Buy Button
                        screen.blit(batlevel_button_textB, (433, 375))

            # if Shop_button is in Skin page
            elif SHOP_BUTTON == 'skin':
                pygame.draw.rect(screen, ORANGE, skin_button)                   # Orange Color on Skin Button
                screen.blit(skin_button_textB, (161, 282))                      # Black text on Skin button
                screen.blit(human_image, (410, 200))

                # Default skin page
                if skin_index == 0:
                    screen.blit(skin0_name, (390, 160))
                    if USER_DICT["skin0"] == 1:                                 # If default skin is chosen
                        screen.blit(in_use_text, (420, 315))
                    screen.blit(choose_button_textB, (413, 375))

                # Christmas hat skin page
                elif skin_index == 1:
                    screen.blit(skin1_name, (380, 160))
                    screen.blit(skin1_image, (446, 187))
                    if "skin1" in USER_DICT.keys():                             # If already bought Christmas hat skin
                        if USER_DICT["skin1"] == 1:                             # If Christmas hat skin is chosen
                            screen.blit(in_use_text, (420, 315))
                        screen.blit(choose_button_textB, (413, 375))
                    else:
                        screen.blit(skin1_cost, (405, 315))                     # Cost and Buy Button
                        screen.blit(buy_button_textB, (431, 375))

                # Birthday hat skin page
                elif skin_index == 2:
                    screen.blit(skin2_name, (388, 160))
                    screen.blit(skin2_image, (448, 185))
                    if "skin2" in USER_DICT.keys():                             # If already bought Birthday hat skin
                        if USER_DICT["skin2"] == 1:                             # If Birthday hat skin is chosen
                            screen.blit(in_use_text, (420, 315))
                        screen.blit(choose_button_textB, (413, 375))
                    else:
                        screen.blit(skin2_cost, (405, 315))                     # Cost and Buy Button
                        screen.blit(buy_button_textB, (431, 375))

            pygame.draw.rect(screen, WHITE, ufo_button, 2)
            pygame.draw.rect(screen, WHITE, upgrades_button, 2)
            pygame.draw.rect(screen, WHITE, skin_button, 2)

        # If Menu_page is in Manual
        elif MENU_PAGE == 'manual':
            pygame.draw.rect(screen, WARNINGYELLOW, manual_button)
            # pygame.draw.rect(screen, WHITE, manual_button, 3)
            screen.blit(manual_button_textB, (495, 70))
            screen.blit(rules_text, (100, 125))
            screen.blit(rules1_text, (110, 155))
            screen.blit(rules2_text, (110, 185))
            screen.blit(rules3_text, (110, 215))
            screen.blit(rules4_text, (110, 245))
            screen.blit(rules5_text, (110, 275))
            screen.blit(rules6_text, (110, 305))
            screen.blit(rules7_text, (110, 335))

        # Draw White Button Borders
        pygame.draw.rect(screen, WHITE, map_button, 3)
        pygame.draw.rect(screen, WHITE, shop_button, 3)
        pygame.draw.rect(screen, WHITE, manual_button, 3)

        # Capture Main menu Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                DATA_DICT[USER_INPUT] = USER_DICT
                saveDataDict()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:                             # Backspace to Login Page
                    DATA_DICT[USER_INPUT] = USER_DICT
                    saveDataDict()
                    CURRENT_SCREEN = 'LOGIN'
            if event.type == pygame.MOUSEBUTTONUP:
                if 75 <= mouseX < 265 and 60 <= mouseY <= 110:                  # Map button pressed
                    MENU_PAGE = 'map'
                elif 265 <= mouseX < 455 and 60 <= mouseY <= 110:               # SHop button pressed
                    MENU_PAGE = 'shop'
                    SHOP_BUTTON = 'ufo'                                         # Ufo page by default
                    ufo_index = 0
                    skin_index = 0
                elif 455 <= mouseX < 645 and 60 <= mouseY <= 110:               # Manual button pressed
                    MENU_PAGE = 'manual'

                # Menu_page is Map page
                if MENU_PAGE == 'map':
                    if 285 <= mouseX <= 445 and 355 <= mouseY <= 395:           # Play button pressed in Map Page
                        # Initialize all related variables
                        PLAYERX = screenWidth / 2 - 32
                        PLAYERY = screenHeight / 2 - 32
                        LIFE = USER_DICT["life"]
                        ABDUCTIONSCORE = 0
                        FINALSCORE = 0
                        BATTERIES = 5
                        COINGAIN = 0
                        EXTRACOIN = 0
                        CURRENT_TIME = 0
                        HUMANRELOAD = 150
                        HUMAN_BENCH_LIST = []
                        BATAMOUNTS = 1

                        # Load ufo picture to ufoImg
                        if USER_DICT["ufo0"] == 1:
                            ufoImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "ufo0.png")), (64, 64))
                        elif USER_DICT["ufo1"] == 1:
                            ufoImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "ufo1.png")), (64, 64))
                        elif USER_DICT["ufo2"] == 1:
                            ufoImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "ufo2.png")), (64, 64))

                        # Initialize additional Upgrades
                        if USER_DICT["human"] == 2:
                            HUMANLEVEL2 = 4
                        if USER_DICT["human"] == 3:
                            HUMANLEVEL2 = 8
                            HUMANLEVEL3 = 10
                        if USER_DICT["bat"] == 2:
                            BATLEVEL2 = True
                        if USER_DICT["bat"] == 3:
                            BATLEVEL3 = True

                        # Load Human sprite skin to skinImg and transfer to human_sprite animation class
                        if USER_DICT["skin0"] == 1:
                            SKIN = 0
                            human_sprite = Humansprite_animation(SPRITEX, SPRITEY, 'normal', SKIN)
                            animated_sprites.add(human_sprite)
                        elif USER_DICT["skin1"] == 1:
                            SKIN = 1
                            skinImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "christmas-hat.png")), (16, 16))
                            human_sprite = Humansprite_animation(SPRITEX, SPRITEY, 'normal', SKIN)
                            animated_sprites.add(human_sprite)
                        elif USER_DICT["skin2"] == 1:
                            SKIN = 2
                            skinImg = pygame.transform.scale(pygame.image.load(resource_path(RESOURCESPATH + "birthday-hat.png")), (16, 16))
                            human_sprite = Humansprite_animation(SPRITEX, SPRITEY, 'normal', SKIN)
                            animated_sprites.add(human_sprite)

                        # setting Bat Sprite class and groups
                        animated_bats = pygame.sprite.Group()
                        bat_sprite = Bat_animation(BATX, BATY, 'normal')
                        animated_bats.add(bat_sprite)

                        # setting Human Sprite class, group, and reload
                        animated_sprites = pygame.sprite.Group()
                        human_reload = HUMANRELOAD

                        # Stop start music and open background music
                        start_music.stop()
                        CURRENT_SCREEN = 'GAME'
                        background_music.play(-1)
                        # print("=============")

                # if Menu_page is in shop page
                if MENU_PAGE == 'shop':
                    if 110 <= mouseX <= 260 and 165 <= mouseY <= 210:
                        SHOP_BUTTON = 'ufo'
                    elif 110 <= mouseX <= 260 and 220 <= mouseY <= 265:
                        SHOP_BUTTON = 'upgrades'
                    elif 110 <= mouseX <= 260 and 275 <= mouseY <= 320:
                        SHOP_BUTTON = 'skin'

                    # Right/Left Arrow Event
                    if 565 <= mouseX <= 616 and 225 <= mouseY <= 276:
                        if SHOP_BUTTON == 'ufo':
                            ufo_index = (ufo_index + 1) % 3
                        elif SHOP_BUTTON == 'upgrades':
                            upgrades_index = (upgrades_index + 1) % 3
                        elif SHOP_BUTTON == 'skin':
                            skin_index = (skin_index + 1) % 3
                    elif 290 <= mouseX <= 341 and 225 <= mouseY <= 276:
                        if SHOP_BUTTON == 'ufo':
                            ufo_index = (ufo_index - 1) % 3
                        elif SHOP_BUTTON == 'upgrades':
                            upgrades_index = (upgrades_index - 1) % 3
                        elif SHOP_BUTTON == 'skin':
                            skin_index = (skin_index - 1) % 3

                    # Buy/Choose Button Event
                    if 383 <= mouseX <= 523 and 370 <= mouseY <= 410:

                        # Shop_button is in Ufo page
                        if SHOP_BUTTON == 'ufo':
                            # Default Ufo page
                            if ufo_index == 0:
                                USER_DICT["ufo0"] = 1
                                if "ufo1" in USER_DICT.keys():
                                    USER_DICT["ufo1"] = 0
                                if "ufo2" in USER_DICT.keys():
                                    USER_DICT["ufo2"] = 0
                            # Radio Ufo page
                            elif ufo_index == 1:
                                if "ufo1" in USER_DICT.keys():
                                    USER_DICT["ufo0"] = 0
                                    USER_DICT["ufo1"] = 1
                                    if "ufo2" in USER_DICT.keys():
                                        USER_DICT["ufo2"] = 0
                                else:
                                    if USER_DICT["coin"] >= 500:
                                        USER_DICT["ufo1"] = 0
                                        USER_DICT["coin"] -= 500
                                    else:
                                        pass
                            # Hi-Tech Ufo page
                            elif ufo_index == 2:
                                if "ufo2" in USER_DICT.keys():
                                    USER_DICT["ufo0"] = 0
                                    USER_DICT["ufo2"] = 1
                                    if "ufo1" in USER_DICT.keys():
                                        USER_DICT["ufo1"] = 0
                                else:
                                    if USER_DICT["coin"] >= 1000:
                                        USER_DICT["ufo2"] = 0
                                        USER_DICT["coin"] -= 1000
                                    else:
                                        pass

                        # Shop_button is in upgrades page
                        elif SHOP_BUTTON == 'upgrades':
                            if upgrades_index == 0:
                                if USER_DICT["life"] < 5:
                                    if USER_DICT["coin"] >= 200:
                                        USER_DICT["life"] += 1
                                        USER_DICT["coin"] -= 200
                            elif upgrades_index == 1:
                                if USER_DICT["human"] < 3:
                                    if USER_DICT["coin"] >= 200:
                                        USER_DICT["human"] += 1
                                        USER_DICT["coin"] -= 200
                            elif upgrades_index == 2:
                                if USER_DICT["bat"] < 3:
                                    if USER_DICT["coin"] >= 200:
                                        USER_DICT["bat"] += 1
                                        USER_DICT["coin"] -= 200

                        # Shop_button is in skin page
                        elif SHOP_BUTTON == 'skin':
                            if skin_index == 0:
                                USER_DICT["skin0"] = 1
                                if "skin1" in USER_DICT.keys():
                                    USER_DICT["skin1"] = 0
                                if "skin2" in USER_DICT.keys():
                                    USER_DICT["skin2"] = 0
                            elif skin_index == 1:
                                if "skin1" in USER_DICT.keys():
                                    USER_DICT["skin0"] = 0
                                    USER_DICT["skin1"] = 1
                                    if "skin2" in USER_DICT.keys():
                                        USER_DICT["skin2"] = 0
                                else:
                                    if USER_DICT["coin"] >= 150:
                                        USER_DICT["skin1"] = 0
                                        USER_DICT["coin"] -= 150
                                    else:
                                        pass
                            elif skin_index == 2:
                                if "skin2" in USER_DICT.keys():
                                    USER_DICT["skin0"] = 0
                                    USER_DICT["skin2"] = 1
                                    if "skin1" in USER_DICT.keys():
                                        USER_DICT["skin1"] = 0
                                else:
                                    if USER_DICT["coin"] >= 250:
                                        USER_DICT["skin2"] = 0
                                        USER_DICT["coin"] -= 250
                                    else:
                                        pass

    # GAME screen --------------------------------------------------------------------------------------
    if CURRENT_SCREEN == 'GAME':

        # position of the generated heart/life
        playerlife()

        # position of the generated score
        show_score(SCOREX, SCOREY, ABDUCTIONSCORE)

        # position of the generated coin gain
        show_coingain(screenWidth-117, 35, COINGAIN)

        # position of the generated battery
        batterylife(0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # print("yes")
                if event.key == pygame.K_w:
                    W_change = -PLAYERSPEED
                    # print("w is pressed")
                if event.key == pygame.K_a:
                    A_change = -PLAYERSPEED
                    # print("a is pressed")
                if event.key == pygame.K_s:
                    S_change = PLAYERSPEED
                    # print("s is pressed")
                if event.key == pygame.K_d:
                    D_change = PLAYERSPEED
                    # print("d is pressed")
                if event.key == pygame.K_SPACE:
                    if beam_state == 'ready':
                        beam_tick = pygame.time.get_ticks()
                        if BATTERIES != -1:
                            BATTERIES -= 1
                    if BATTERIES > -1:
                        beam_state = 'fire'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    W_change = 0
                if event.key == pygame.K_a:
                    A_change = 0
                if event.key == pygame.K_s:
                    S_change = 0
                if event.key == pygame.K_d:
                    D_change = 0
                # print("key isn't pressed")

        # Ufo movement
        PLAYERX += A_change + D_change
        PLAYERY += W_change + S_change

        # setting Ufo movement boundaries
        if PLAYERX <= 0:
            PLAYERX = 0
        elif PLAYERX >= screenWidth-64:
            PLAYERX = screenWidth-64
        if PLAYERY <= 0:
            PLAYERY = 0
        elif PLAYERY >= screenHeight/1.5:
            PLAYERY = screenHeight/1.5

        # beam movement / duration
        if beam_state == 'fire':
            BEAMX = PLAYERX - 12
            BEAMY = PLAYERY + 50
            fire_beam(BEAMX, BEAMY)
            if CURRENT_TIME - beam_tick > 800:
                beam_state = 'ready'
                beam_tick = 0

        # UFO-accumulator Collision
        if isUFOACCCollision(PLAYERX, PLAYERY, ACCUMULATORX, ACCUMULATORY):
            BATTERIES = 5
            # if not accumulator_cooldown:
            accumulator_tick = pygame.time.get_ticks()
            ACCUMULATORX = -100
            ACCUMULATORY = -100
            accumulator_cooldown = True

        # Accumulator cool down upon collision
        if accumulator_cooldown:
            if CURRENT_TIME - accumulator_tick > 800:
                ACCUMULATORX = r.randint(10, screenWidth - 32)
                ACCUMULATORY = r.randint(0, int(screenHeight / 2))
                accumulator_cooldown = False

        # Accumulator generation
        accumulator(ACCUMULATORX, ACCUMULATORY)

        # UFO-coin Collision
        if isUFOCoinCollision(PLAYERX, PLAYERY, COINX, COINY):
            COINGAIN += 10 + EXTRACOIN
            coin_tick = pygame.time.get_ticks()
            COINX = -50
            COINY = -50
            coin_cooldown = True

        # Coin cool down upon collision
        if coin_cooldown:
            if CURRENT_TIME - coin_tick > 6000:
                COINX = r.randint(10, screenWidth - 25)
                COINY = r.randint(0, int(screenHeight / 1.5))
                coin_cooldown = False

        coin(COINX, COINY)

        # UFO generation
        ufo(PLAYERX, PLAYERY)

        # Check Game over True/False and explosion
        if LIFE == 0 or ABDUCTIONSCORE < -25:
            FINALSCORE = ABDUCTIONSCORE
            if FINALSCORE > USER_DICT["score"]:
                USER_DICT["score"] = FINALSCORE
                score_text = WARNING_FONT.render("Hi-Score: " + str(USER_DICT['score']), True, DARKRED)
            USER_DICT["coin"] += COINGAIN
            explode_state = 'fire'
            explosion_sound.play()
            explosion_tick = pygame.time.get_ticks()
            LIFE = -1

        if explode_state == 'fire':
            if CURRENT_TIME - explosion_tick < 3000:
                explosion(PLAYERX-16, PLAYERY-16)
            else:
                background_music.stop()
                CURRENT_SCREEN = 'END'
                explode_state = 'ready'

        # Bat Sprite/ Bat-target UFO automation/rules/reload + Bat Upgrades
        if ABDUCTIONSCORE == WHEN_BAT_SHOULD_SPAWN:
            if ABDUCTIONSCORE == 10:
                target_bat_sprite = Bat_animation(BATX, target_BATY, 'normal')
                animated_bats.add(target_bat_sprite)
                BATAMOUNTS += 1
            elif ABDUCTIONSCORE == 20:
                target_bat_sprite = Bat_animation(BATX, target_BATY, 'target')
                animated_bats.add(target_bat_sprite)
                BATAMOUNTS += 1
            elif ABDUCTIONSCORE >= 30:
                if BATLEVEL2:
                    BATSPAWN_NONLINEAR_PROGRESS += 0.2
                elif BATLEVEL3:
                    BATSPAWN_NONLINEAR_PROGRESS += 0.3
                else:
                    BATSPAWN_NONLINEAR_PROGRESS += 0.1
                target_bat_sprite = Bat_animation(BATX, target_BATY, 'normal')
                animated_bats.add(target_bat_sprite)
                BATAMOUNTS += 1
            WHEN_BAT_SHOULD_SPAWN = ABDUCTIONSCORE + math.floor(10 * BATSPAWN_NONLINEAR_PROGRESS)
            # print("BAT AMOUNTS: " + str(BATAMOUNTS))      
        animated_bats.draw(screen)
        animated_bats.update()

        # Human Sprite automation/rules/reload
        if human_reload:
            human_reload -= 1
        else:
            human_sprite = Humansprite_animation(SPRITEX, SPRITEY, 'normal', SKIN)
            animated_sprites.add(human_sprite)

            # Controlling the reload time
            if ABDUCTIONSCORE >= 5 and ABDUCTIONSCORE % 5 == 0:
                if ABDUCTIONSCORE not in HUMAN_BENCH_LIST:
                    # More coin gain per collision
                    if ABDUCTIONSCORE % 10 == 0:
                        EXTRACOIN += 15
                    # Human reload algorithm + Human Upgrades
                    if HUMANRELOAD > 70 + HUMANLEVEL3:
                        HUMANRELOAD -= 10
                    elif 60 + HUMANLEVEL2 <= HUMANRELOAD <= 70 + HUMANLEVEL3:
                        HUMANRELOAD -= 2
                    elif 55 <= HUMANRELOAD < 60 + HUMANLEVEL2:
                        HUMANRELOAD -= 1
                # print(HUMANRELOAD)
                HUMAN_BENCH_LIST.append(ABDUCTIONSCORE)
            # looping reload
            human_reload = HUMANRELOAD

        animated_sprites.draw(screen)
        animated_sprites.update()

    # END screen ---------------------------------------------------------------------------------------
    if CURRENT_SCREEN == 'END':
        show_score(SCOREX, SCOREY, FINALSCORE)
        gameover(screenWidth/5+15, screenHeight/3, screenWidth/4-7, screenHeight/2+30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                DATA_DICT[USER_INPUT] = USER_DICT
                saveDataDict()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_music.play(-1)
                    CURRENT_SCREEN = 'MAIN MENU'

    pygame.display.update()
    CLOCK.tick(FPS)
