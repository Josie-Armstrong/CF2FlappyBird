import pygame, sys, random, math
import Bird, Pipe, RestartButton, SizeToken
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
bg = pygame.transform.scale(bg, (4200, 700)) # scale background image
ground = pygame.image.load('./Game Textures/Grounds/ground.png')
button_img = pygame.image.load('./Game Textures/Buttons/restart.png')

#define font
font = pygame.font.SysFont('Times New Roman', 60)

#define color
white = (255,255,255)


#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 300
pipe_frequency = 1500 #milliseconds (1.5 sec)
token_frequency = 600 # milliseconds, like above
last_pipe = pygame.time.get_ticks() - pipe_frequency
last_token = pygame.time.get_ticks() - token_frequency
score = 0
pass_pipe = False
level = 1 # for changing levels

# define background variables
bg_width = bg.get_width()
bg_tiles = 2
bg_scroll = 0


#drawing text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))
    
#reset score
def reset_game(): 
    pipe_group.empty()
    large_token_group.empty()
    small_token_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    bg_scroll = 0
    return score

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

#sprites
flappy = Bird.Bird(100,int(screen_height / 2))


#add sprite groups 
bird_group.add(flappy)


#create restart button instance
button = RestartButton.Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img, screen)

#run the game
while True:

    clock.tick(fps)

    # scrolls if game/round is going, else maintains a static background
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

    #draw sprites to screen
    bird_group.draw(screen)
    bird_group.update(flying, game_over)
    pipe_group.draw(screen)

    # draw tokens if level 4
    if level == 4:
        large_token_group.draw(screen)
        small_token_group.draw(screen)



    #draw the ground
    screen.blit(ground, (ground_scroll, 618))

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

    #draw score to screen
    draw_text(str(score), font, white, int(screen_width / 2), 20)
     

    #look for pipe collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True


    #look for ground collision
    if flappy.rect.bottom >= 618:
        game_over = True
        flying = False
    
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


    #generate pipes and ground
    if game_over == False and flying == True:
        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100) #randomize distsnce between pipes
            btm_pipe = Pipe.Pipe(screen_width, int(screen_height / 2) + pipe_height, -1, pipe_gap)
            top_pipe = Pipe.Pipe(screen_width, int(screen_height / 2) + pipe_height, 1, pipe_gap)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        

        # generating size change tokens if level is 4
        if level == 4:
            if time_now - last_token > token_frequency:
                tokeny = random.randint(100, 500)
                tokenx = 664
                token_type = random.randint(0,1)

                token = SizeToken.Token(tokenx, tokeny, token_type)
                
                if token.type == "large":
                    large_token_group.add(token)
                elif token.type == "small":
                    small_token_group.add(token)
                
                last_token = time_now

        #draw scrolling ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
            
        pipe_group.update(scroll_speed)
        large_token_group.update(scroll_speed)
        small_token_group.update(scroll_speed)

    #check for game over and reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()
            bg_scroll = 0
            flappy.sizeChange(0, True)

    # check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        if event.type == pygame.KEYDOWN:
            if event.key == K_4:
                level = 4

    pygame.display.update()

