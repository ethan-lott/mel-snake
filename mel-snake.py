# Import necessary packages.
import pygame
import random

# Define constants.
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
PINK = (255,230,230)
GREEN = (0,200,0)
ARROWS = [pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN]
DIS_WIDTH = 640
DIS_HEIGHT  = 640
SNAKE_SPEED = 6
SNAKE_BLOCK = 40

# Initialize game window.
pygame.init()
dis = pygame.display.set_mode((DIS_WIDTH,DIS_HEIGHT+SNAKE_BLOCK))
pygame.display.set_caption('Snake 2: Mel-ectric Boogaloo')
clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, SNAKE_BLOCK)
score_font = pygame.font.SysFont(None, SNAKE_BLOCK)

## Initialize images.
body_img = pygame.image.load('images/mel-body.png')                                # load and scale mel's body
body_img = pygame.transform.scale(body_img, (SNAKE_BLOCK, SNAKE_BLOCK))
tail_img = pygame.image.load('images/mel-tail.png')                                # load and scale mel's tail
tail_img = pygame.transform.scale(tail_img, (SNAKE_BLOCK, SNAKE_BLOCK))
ethan_img = pygame.image.load('images/ethan.png')                                  # load and scale ethan's face
ethan_img = pygame.transform.scale(ethan_img, (SNAKE_BLOCK, SNAKE_BLOCK))
grace_img = pygame.image.load('images/grace.png')                                  # load and scale grace's face
grace_img = pygame.transform.scale(grace_img, (SNAKE_BLOCK, SNAKE_BLOCK))
sophie_img = pygame.image.load('images/sophie.png')                                # load and scale sophie's face
sophie_img = pygame.transform.scale(sophie_img, (SNAKE_BLOCK, SNAKE_BLOCK))
anna_img = pygame.image.load('images/anna.png')                                # load and scale sophie's face
anna_img = pygame.transform.scale(anna_img, (SNAKE_BLOCK, SNAKE_BLOCK))
food_imgs = [ethan_img, grace_img, sophie_img, anna_img]

## Initialize sounds.
mel_sound = pygame.mixer.Sound('sounds/mel-meow.wav')
ethan_sound = pygame.mixer.Sound('sounds/ethan-ow.wav')
sophie_sound = pygame.mixer.Sound('sounds/sophie-hey.wav')
anna_sound = pygame.mixer.Sound('sounds/anna-briskot.wav')
grace_sound = pygame.mixer.Sound('sounds/grace-melon.wav')

def display_score(score):
    value = score_font.render("Your Score: " + str(score), True, GREEN)
    dis.blit(value, (0, 0))

## Create a new version of our snake.
def our_snake(head_img, body_img, tail_img, snake_list):
    # Add tail or not.
    if len(snake_list) > 1:
        dis.blit(pygame.transform.rotate(tail_img, snake_list[1][2] * 90), (snake_list[0][0],snake_list[0][1]))
        start = 1
    else:
        start = 0

    # Add body.
    i = start
    for x in snake_list[start:-1]:
        dis.blit(pygame.transform.rotate(body_img, snake_list[i+1][2] * 90), (x[0],x[1]))
        i += 1

    # Add head.
    dis.blit(head_img, (snake_list[-1][0],snake_list[-1][1]))

## Display a message on screen.
def message(msg,color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [2*SNAKE_BLOCK, DIS_HEIGHT/2])

## Run the game.
def gameLoop():

    global body_img, tail_img, ethan_img, grace_img, sophie_img, ethan_sound
    head_img = pygame.image.load('images/mel-face.png')                                # load and scale mel's head
    head_img = pygame.transform.scale(head_img, (SNAKE_BLOCK, SNAKE_BLOCK))

    ## Set starting game values.
    game_over = False               #
    game_close = False              #
    x0 = DIS_WIDTH/2                # x-coord of head
    y0 = DIS_HEIGHT/2+SNAKE_BLOCK # y-coord of head
    x0_change = 0                   # dX per frame
    y0_change = 0                   # dY per frame
    dir = 0                         # direction of current motion
    n_dir = 0                       # new direction after keystroke
    food_i = 0                      # index of food image
    arrow_queue = []

    ## Initialize snake and food.
    snake_List = []                 # list of all current pieces of snake: [x-coord, y-coord, direction]
    Length_of_snake = 1             # current length of snake
    food_x = x0 + 3*SNAKE_BLOCK     # x-coord of current food
    food_y = y0                     # y-coord of current food

    ## Initialize background pattern
    background = pygame.Surface((DIS_WIDTH, DIS_HEIGHT))
    ts, w, h, c1, c2 = round(SNAKE_BLOCK), *background.get_size(), PINK, WHITE
    tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
    [pygame.draw.rect(background, color, rect) for rect, color in tiles]

    ## Loop until user quits.
    while not game_close:

        ## If game ends, given option to play again.
        while game_over:

            ## Display score and offer to play again.
            value = score_font.render("Your Score: " + str(Length_of_snake-1), True, GREEN)
            dis.blit(value, (2*SNAKE_BLOCK, DIS_HEIGHT/2-SNAKE_BLOCK))
            message("Press Q-Quit or C-Play Again", BLACK)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = False
                        game_close = True
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():

            # End game if 'X' is clicked.
            if event.type == pygame.QUIT:
                game_close = True

            # Adjust direction if arrow button if pressed.
            if event.type == pygame.KEYDOWN and event.key in ARROWS:
                arrow_queue.append(event.key)

        if len(arrow_queue) > 0:
            if arrow_queue[0] == pygame.K_LEFT and dir != 0:
                x0_change = -SNAKE_BLOCK
                y0_change = 0
                n_dir = 2
            elif arrow_queue[0] == pygame.K_RIGHT and dir != 2:
                x0_change = SNAKE_BLOCK
                y0_change = 0
                n_dir = 0
            elif arrow_queue[0] == pygame.K_UP and dir != 3:
                y0_change = -SNAKE_BLOCK
                x0_change = 0
                n_dir = 1
            elif arrow_queue[0] == pygame.K_DOWN and dir != 1:
                y0_change = SNAKE_BLOCK
                x0_change = 0
                n_dir = 3

            # Rotate head image.
            head_img = pygame.transform.rotate(head_img, (n_dir - dir) * 90)
            dir = n_dir

            del arrow_queue[0]

        dis.blit(background, (0, SNAKE_BLOCK))

        # Update position.
        x0 += x0_change
        y0 += y0_change
        snake_Head = [x0,y0,dir]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # End game if head hits the wall.
        if x0 >= DIS_WIDTH or x0 < 0 or y0 >= DIS_HEIGHT+SNAKE_BLOCK or y0 < SNAKE_BLOCK:
            pygame.mixer.Sound.play(mel_sound)
            game_over = True

        # End game if head hits tail.
        for x in snake_List[:-1]:
            if x[:2] == snake_Head[:2]:
                pygame.mixer.Sound.play(mel_sound)
                game_over = True

        # If food is eaten, update snake length and food location.
        if x0 == food_x and y0 == food_y:
            if food_i == 0:
                sound = ethan_sound
            elif food_i == 1:
                sound = grace_sound
            elif food_i == 2:
                sound = sophie_sound
            else:
                sound = anna_sound
            pygame.mixer.Sound.play(sound)
            while True:
                food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / float(SNAKE_BLOCK)) * SNAKE_BLOCK
                food_y = round(random.randrange(SNAKE_BLOCK, DIS_HEIGHT) / float(SNAKE_BLOCK)) * SNAKE_BLOCK
                if [food_x, food_y] not in [z[:2] for z in snake_List]:
                    break
            food_i = random.randint(0, 3)
            Length_of_snake += 1

        pygame.draw.rect(dis, WHITE, (0, 0, DIS_WIDTH, SNAKE_BLOCK))

        if not game_over:
            our_snake(head_img, body_img, tail_img, snake_List)
            display_score(Length_of_snake-1)
            dis.blit(food_imgs[food_i], (food_x,food_y))

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

gameLoop()
