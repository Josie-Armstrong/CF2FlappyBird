import pygame, sys, random, math
import Bird, Pipe, RestartButton, SizeToken, Coin, Shop, ShopButton, HeartShield
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
fps = 60

#set screen dimensions
screen_width = 664
screen_height = 736

#set up game windpw
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird (But Cool)")

#load images
bg = pygame.image.load('./Game Textures/Backgrounds/level1.png').convert()
bg = pygame.transform.scale(bg, (3660, 620)) # scale background image

ground = pygame.image.load('./Game Textures/Grounds/ground1.png').convert()

button_img = pygame.image.load('./Game Textures/Buttons/restart_btn_new.png').convert_alpha()
button_img = pygame.transform.scale(button_img, (120,42))

coin_img = pygame.image.load('./Game Textures/Coin/coin.png').convert_alpha()
coin_img = pygame.transform.scale_by(coin_img, 3)
coin_bg = pygame.image.load('./Game Textures/Coin/coin_bg.png').convert_alpha()
coin_bg = pygame.transform.scale_by(coin_bg, 6)

shop_btn_img = pygame.image.load('./Game Textures/Shop/shop_btn.png').convert_alpha()
shop_btn_img = pygame.transform.scale_by(shop_btn_img, 4)


# load alt grounds
ground1 = pygame.image.load('./Game Textures/Grounds/ground1.png').convert()
ground2 = pygame.image.load('./Game Textures/Grounds/ground2.png').convert()
ground3 = pygame.image.load('./Game Textures/Grounds/ground3.png').convert()
ground4 = pygame.image.load('./Game Textures/Grounds/ground4.png').convert()

# scaling ground images
ground4 = pygame.transform.scale(ground4, (900,168))


#define font
font = pygame.font.SysFont('Courier', 60)
coin_font = pygame.font.SysFont('Courier',40)

#define color
white = (255,255,255)
black = (0,0,0)

# define game variables
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 300
# frequencies
pipe_frequency = 1500 #milliseconds (1.5 sec)
token_frequency = 600 # milliseconds, like above
coin_frequency = 800 # milliseconds too
heart_shield_frequency = 750
buy_frequency = 300
# last instances
last_pipe = pygame.time.get_ticks() - pipe_frequency
last_token = pygame.time.get_ticks() - token_frequency
last_coin = pygame.time.get_ticks() - token_frequency
last_heart_shield_use = pygame.time.get_ticks() - heart_shield_frequency
last_buy = pygame.time.get_ticks() - buy_frequency
# other variables
score = 0
pass_pipe = False
level = 1 # for changing levels
lvl_change = False
last_lvl_change = 0
coin_count = 0 # global coin-tracking variable
total_heart_count = 10
heart_count = 10
shield_count = 10
shop_open = False

#define ground variables
ground_scroll = 0
ground_tiles = 2
ground_width = ground.get_width()

# define background variables
bg_width = bg.get_width()
bg_tiles = 2
bg_scroll = 0

#drawing text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

# draw coin count to screen
def draw_coins():
    global coin_count
    global screen

    coin_count_x = 0

    if coin_count < 10:
        coin_count_x = screen_width - 60
    elif coin_count < 100:
        coin_count_x = screen_width - 85
    else:
        coin_count_x = screen_width - 105

    screen.blit(coin_bg, (screen_width - 120, 0))
    screen.blit(coin_img, (screen_width - 30, 7))
    draw_text(str(coin_count), coin_font, black, coin_count_x, 3)

#reset score
def reset_game():
    global score, bg_scroll, level, last_lvl_change, heart_count, total_heart_count

    pipe_group.empty()
    large_token_group.empty()
    small_token_group.empty()
    coin_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    bg_scroll = 0
    level = 1
    last_lvl_change = 0
    heart_count = total_heart_count
    # print("Heart Count:" + str(heart_count))
    change_level()

    return score

def scroll_background():
    global bg_scroll

    if (game_over == False and flying == True):
        # drawing the background
        for i in range(0, bg_tiles):
            screen.blit(bg, (i * bg_width + bg_scroll,0))

        # scrolling background and resetting scroll
        bg_scroll -= scroll_speed
        if abs(bg_scroll) > bg_width:
            bg_scroll = 0
    else:
        for i in range(0, bg_tiles):
            screen.blit(bg, (i * bg_width + bg_scroll,0))

def scroll_ground():
    global ground_scroll

    if (game_over == False and flying == True):
        # screen.blit(ground, (ground_scroll, 618))
        for i in range(0, ground_tiles):
                screen.blit(ground, (i * ground_width + ground_scroll, 618))
        
        # scroll the ground, move tiles if needed
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > ground_width:
            ground_scroll = 0
            # print("ground reset")
    else:
        for i in range(0, ground_tiles):
                screen.blit(ground, (i * ground_width + ground_scroll,618))

def change_level():
    global ground
    global level

    large_token_group.empty()
    small_token_group.empty()
    flappy.sizeChange(1, True)
    pipe_gap = 300

    if level == 1:
        ground = ground1
    elif level == 2:
        ground = ground2
    elif level == 3:
        ground = ground3
    elif level == 4:
        ground = ground4
    # print("level changed")

def run_shop(time_now):
    global shop, shop_open, coin_count, shield_count, heart_count, total_heart_count, last_buy, buy_frequency

    shop_action = shop.draw()
    if shop_action == 0:
        shop_open = False
    elif shop_action == 1:
        if (coin_count >= 20) and (shield_count < 10) and (time_now - last_buy > buy_frequency):
            coin_count -= 20
            shield_count += 1
            last_buy = time_now
    elif shop_action == 2:
        if (coin_count >= 100) and (heart_count < 10) and (time_now - last_buy > buy_frequency):
            coin_count -= 100
            total_heart_count += 1
            heart_count = total_heart_count
            last_buy = time_now

def draw_hearts_and_shields():
    global heart_count, shield_count, screen

    for i in range(0,10):
        if i < heart_count:
            heart_array[i].draw()
        if i < shield_count:
            shield_array[i].draw()

# Bird class - NOW IN EXTERNAL FILE
''' class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images =[]
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'./Game Textures/Sprites/Birds L1/coolbird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0 #bird's velocity
        self.jumped = False
        self.mid_air = False

    def update(self):


        #gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 618: #if bird is above the ground (inc y means moving down)
                self.rect.y += int(self.vel)

                
        if game_over == False:
        #jumping
            self.mid_air = True
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.mid_air == True:
                self.jumped = True
                self.vel = -10 

            if key[pygame.K_SPACE] == False:
                self.jumped = False




            #handle animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel*-2)'''

# Pipe class - NOW IN EXTERNAL FILE
''' class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./Game Textures/Obstacles/level1.png')
        self.image = pygame.transform.scale(self.image, (78, 560))
        self.rect = self.image.get_rect()
        #position 1 is from top, -1 is from bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) #False = x-axis, True = y-axis
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
        if position == -1: 
            self.rect.topleft = [x,y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0: #gets rid of pipes that are offscreen to save memory
            self.kill()'''

''' class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1: #mouse presssed use index values for left, right, middle click
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action''' 
        
#sprite groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
large_token_group = pygame.sprite.Group() # size change level
small_token_group = pygame.sprite.Group() # size change level
coin_group = pygame.sprite.Group() # coin group

#sprites
flappy = Bird.Bird(100,int(screen_height / 2))

#add sprite groups 
bird_group.add(flappy)

#create restart button instance
button = RestartButton.Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img, screen)

# create shop and button to access
shop_button = ShopButton.ShopButton(10, 10, shop_btn_img, screen)
shop = Shop.Shop(screen, screen_width, screen_height)

# heart and shield arrays
heart_array = []
shield_array = []

for i in range(0,10):
    new_heart = HeartShield.HeartShield('h',i,screen_height, screen)
    new_shield = HeartShield.HeartShield('s',i,screen_height, screen)

    heart_array.append(new_heart)
    shield_array.append(new_shield)

#run the game
while True:

    clock.tick(fps)

    scroll_background()
    # screen.blit(bg, (0,0))

    #draw sprites to screen
    bird_group.draw(screen)
    bird_group.update(flying, game_over)
    pipe_group.draw(screen)
    coin_group.draw(screen)

    # draw tokens if level is 4
    if level == 4:
        large_token_group.draw(screen)
        small_token_group.draw(screen)

    # screen.blit(ground, (ground_scroll, 618))
    screen.blit(ground, (0,618))
    # scroll_ground()

    # draw shop button if a round is not in progress
    if flying == False and game_over == False and shop_open == False:
        shop_button.draw()
        if shop_button.check_pressed() == True:
            shop_open = True
            print("shop open!")
    
    if shop_open == True:
        time_now = pygame.time.get_ticks()
        run_shop(time_now)
    
    # draw hearts and shields
    draw_hearts_and_shields()

    #check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    # print(score) DEBUG

    if shop_open == False:
        #draw score to screen
        draw_text(str(score), font, white, int(screen_width / 2), 20)
    
    # draw coin count to screen
    draw_coins()

    #look for pipe collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        # if pipe collision is true, use a shield or heart if possible. If not possible, end game.
        time_now = pygame.time.get_ticks()
        if time_now - last_heart_shield_use > heart_shield_frequency:
            if(shield_count > 0):
                shield_count -= 1
            elif(heart_count > 0):
                heart_count -= 1
            else:
                game_over = True
            last_heart_shield_use = time_now

    #look for ground collision
    if flappy.rect.bottom >= 618:
        game_over = True
        flying = False

    # look for coin collisions, update coins
    if pygame.sprite.groupcollide(coin_group, bird_group, True, False):
        coin_count += 1
    
    # look for token collisions, randomizing pipe gap, level 4 only
    if level == 4:
        # removing tokens that collide with pipes
        pygame.sprite.groupcollide(large_token_group, pipe_group, True, False)
        pygame.sprite.groupcollide(small_token_group, pipe_group, True, False)

        # removing tokens that collide with bird, triggering bird changes
        if pygame.sprite.groupcollide(large_token_group, bird_group, True, False):
            flappy.sizeChange(1.2)
        if pygame.sprite.groupcollide(small_token_group, bird_group, True, False):
            flappy.sizeChange(0.8)
        
        pipe_gap = random.randint(150,300)


    #generate pipes, coins, and lvl 4 tokens
    if game_over == False and flying == True:

        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100) #randomize distsnce between pipes
            btm_pipe = Pipe.Pipe(screen_width, int(screen_height / 2) + pipe_height, -1, pipe_gap)
            top_pipe = Pipe.Pipe(screen_width, int(screen_height / 2) + pipe_height, 1, pipe_gap)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        

        # generate new coins
        if time_now - last_coin > coin_frequency:
            coiny = random.randint(100, 500)
            coinx = screen_width

            new_coin = Coin.Coin(coinx, coiny)
            coin_group.add(new_coin)
            last_coin = time_now

        # generating size change tokens if level is 4
        if level == 4:
            if time_now - last_token > token_frequency:
                tokeny = random.randint(100, 500)
                tokenx = screen_width
                token_type = random.randint(0,1)

                token = SizeToken.Token(tokenx, tokeny, token_type)
                
                if token.type == "large":
                    large_token_group.add(token)
                elif token.type == "small":
                    small_token_group.add(token)
                
                last_token = time_now
            
            large_token_group.update(scroll_speed)
            small_token_group.update(scroll_speed)
            
        pipe_group.update(scroll_speed)
        coin_group.update(scroll_speed)

    #check for game over and reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()
            bg_scroll = 0
            flappy.sizeChange(0, True)
    
    # check for level change
    if (score % 10 == 0) and last_lvl_change < score:
        if (level < 4) and (score <= 30):
            level += 1
        else:
            level = random.randint(1,4)
        lvl_change = True
        last_lvl_change = score
        # print("level changed")
    
    # using the change_level function if the level has changed
    if lvl_change == True:
        change_level()
        lvl_change = False

    # check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            # flying = True
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE and flying == False:
                flying = True
            if event.key == K_4:
                level = 4
                change_level()

    pygame.display.update()

