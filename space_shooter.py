import pygame
import os
import random
pygame.mixer.init()

FPS = 120

# Window you play on
WIDTH = 950
HEIGHT = WIDTH//1.77777777
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

# Arbitrary variables that scale with aspect ratio and fps
VELOCITY = (WIDTH//129)//(FPS/60)
BULLET_VELOCITY = (WIDTH//90)//(FPS/60)
LIVES = 5

# Custom events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
RED_DEAD = pygame.USEREVENT + 3
YELLOW_DEAD = pygame.USEREVENT + 4

# Making RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Creating the border that separates the ships
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Loading in sounds
soundObj = pygame.mixer.Sound(os.path.join("Assets", "Assets_Gun+Silencer.mp3"))
soundObj.set_volume(0.3)

# Loading in the models
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = WIDTH//15, HEIGHT//12.5
YELLOW_SPACESHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "yellow_spaceship.png")), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
RED_SPACESHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "red_spaceship.png")), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space_background.jpg")), (WIDTH, HEIGHT))

BULLET_HEIGHT = int(WIDTH*0.0105)
BULLET_WIDTH = int(BULLET_HEIGHT*1.5455)
YELLOW_BULLET = pygame.transform.scale(pygame.image.load(os.path.join(
    "Assets", "yellow_ship_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
RED_BULLET = pygame.transform.scale(pygame.image.load(os.path.join(
    "Assets", "red_ship_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))

GAME_OVER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "game_over.jpg")), (WIDTH, HEIGHT))

HEART_DIMENSIONS = WIDTH//38
HEART = pygame.transform.scale(pygame.image.load(os.path.join(
    "Assets", "heart.png")), (HEART_DIMENSIONS, HEART_DIMENSIONS))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_lives, yellow_lives, dead):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP, yellow)
    WIN.blit(RED_SPACESHIP, red)
    
    # Drawing bullets
    for bullet in red_bullets:
        WIN.blit(RED_BULLET, bullet)
    for bullet in yellow_bullets:
        WIN.blit(YELLOW_BULLET, bullet)

    # Drawing hearts
    for idi, i in enumerate(red_lives):
        WIN.blit(HEART, (WIDTH-WIDTH//27.143-idi*HEART_DIMENSIONS, 15))
    for idi, i in enumerate(yellow_lives):
        WIN.blit(HEART, (idi*HEART_DIMENSIONS+WIDTH//63.33, 15))

    if dead:
        WIN.blit(GAME_OVER, (0, 0))

    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow, velocity):
    if keys_pressed[pygame.K_a] and yellow.x > 0:  # LEFT
        yellow.x -= velocity
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width < BORDER.x:  # RIGHT
        yellow.x += velocity
    if keys_pressed[pygame.K_w] and yellow.y > 0:  # UP
        yellow.y -= velocity
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height < HEIGHT:  # DOWN
        yellow.y += velocity


def handle_red_movement(keys_pressed, red, velocity):
    if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width:  # LEFT
        red.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width < WIDTH:  # RIGHT
        red.x += velocity
    if keys_pressed[pygame.K_UP] and red.y > 0:  # UP
        red.y -= velocity
    if keys_pressed[pygame.K_DOWN] and red.y + red.height < HEIGHT:  # DOWN
        red.y += velocity


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY  # Acceleration
        if red.colliderect(bullet):  # If yellow bullet hits red
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)  # Deleting bullets that go offscreen
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY  # Acceleration
        if yellow.colliderect(bullet):  # If red bullet hits yellow
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x + bullet.width < 0:
            red_bullets.remove(bullet)  # Deleting bullets that go offscreen


def handle_ai_lvl1(yellow, yellow_bullets, second, ai_last_shot_time, velocity, move_oscillator, dead):
    if not dead:
        if second - ai_last_shot_time[0] >= 1.5:  # If it's been more than 1.5 seconds since the ai last shot
            ai_last_shot_time[0] = second  # Reset timer
            yellow_bullets.append(pygame.Rect(yellow.x, yellow.y + yellow.height // 2, 10, 5))
            move_oscillator[0] = 0
        if second - ai_last_shot_time[0] >= 0.75:  # If it's been more than 0.75 seconds since the ai last shot
            move_oscillator[0] = 1
        # Moving the ship up and down periodically
        if move_oscillator[0] == 0:
            yellow.y -= velocity//1.5
        elif move_oscillator[0] == 1:
            yellow.y += velocity//1.5


def handle_ai_lvl2(yellow, yellow_bullets, second, ai_last_shot_time, velocity, random_move, ai_last_move_time, dead):
    if not dead:
        if second - ai_last_shot_time[0] >= 1:  # If it's been more than 1 second since the ai last shot
            ai_last_shot_time[0] = second  # Reset timer
            yellow_bullets.append(pygame.Rect(yellow.x, yellow.y + yellow.height // 2, 10, 5))
        if second - ai_last_move_time[0] >= 0.4:  # If it's been more than 0.4 seconds since the ai last moved
            random_move[0] = random.randint(0, 8)
            ai_last_move_time[0] = second  # Reset timer
        elif second - ai_last_move_time[0] >= random.uniform(0, 3):
            # If it's been more than (random float between 0 and 3) seconds since the ai last moved, don't move anymore
            random_move[0] = 0

        # 25% chance to move left or right
        if random_move[0] == 1 and yellow.x > 0:  # LEFT
            yellow.x -= velocity
        elif random_move[0] == 2 and yellow.x + yellow.width < BORDER.x:  # RIGHT
            yellow.x += velocity
        # 75% chance to move up or down
        elif 5 >= random_move[0] >= 3 and yellow.y > 0:  # UP
            yellow.y -= velocity
        elif 8 >= random_move[0] >= 6 and yellow.y + yellow.height < HEIGHT:  # DOWN
            yellow.y += velocity
        # elif random_move[0] == 0:  # STAY STILL
        #     pass

        # Making the ship "bounce" off the walls
        if yellow.x <= 0:
            random_move[0] = 2
        elif yellow.x + yellow.width >= BORDER.x:
            yellow.x -= velocity
        elif yellow.y <= 0:
            yellow.y += velocity
        elif yellow.y + yellow.height >= HEIGHT:
            yellow.y -= velocity

# def endgame(red_lives, yellow_lives, yellow_bullets, red_bullets, red, yellow):
#     red_lives = [i for i in range(LIVES)]
#     yellow_lives = [i for i in range(LIVES)]
#     yellow_bullets = []
#     red_bullets = []
#     red.x, red.y = int(WIDTH * 0.75), HEIGHT // 2
#     yellow.x, yellow.y = int(WIDTH * 0.25), HEIGHT // 2


def main():
    # AI variables
    random_move = [0]
    ai_last_shot_time = [0]
    ai_last_move_time = [0]
    move_oscillator = [0]
    ai_lvl = 2
    ai = True
    # Integrate this into the game itself, not console input:
    # english_to_bool = {"yes": True, "no": False}
    # ai = english_to_bool[input("Would you like to turn on the ai? ").strip().lower()]
    # if ai:
    #     ai_lvl = int(input("What level ai do you want? (There are only 2 levels) ").strip())
    #     while 1 > ai_lvl > 2:
    #         ai_lvl = int(input("Make sure to only choose a level in between 1 and 2 ").strip())
    
    # Drawing the hit_box for the ships
    red = RED_SPACESHIP.get_rect().move(int(WIDTH*0.75), HEIGHT//2)
    yellow = YELLOW_SPACESHIP.get_rect().move(int(WIDTH*0.25), HEIGHT//2)

    # Making a list for each player's bullets and lives
    red_bullets = []
    yellow_bullets = []
    red_lives = [i for i in range(LIVES)]
    yellow_lives = [i for i in range(LIVES)]
    second = 0  # Time
    time_of_death = 0  # Used as a timer tool for game_over
    clock = pygame.time.Clock()
    run = True

    # Main game loop
    while run:
        clock.tick(FPS)  # Caps framerate
        second += 1/FPS  # Keeps track of time

        if len(yellow_lives) == 0 or len(red_lives) == 0:
            dead = True
        else:
            dead = False

        if ai:
            if ai_lvl == 1:
                handle_ai_lvl1(yellow, yellow_bullets, second, ai_last_shot_time, VELOCITY, move_oscillator, dead)
            if ai_lvl == 2:
                handle_ai_lvl2(yellow, yellow_bullets, second, ai_last_shot_time,
                               VELOCITY, random_move, ai_last_move_time, dead)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Shooting
            if event.type == pygame.KEYDOWN and not dead:
                if event.key == pygame.K_LCTRL and not ai:
                    soundObj.play()
                    yellow_bullets.append(pygame.Rect(yellow.x, yellow.y + yellow.height//2, 10, 5))
                if event.key == pygame.K_RCTRL:
                    red_bullets.append(pygame.Rect(red.x, red.y + red.height//2, 10, 5))

            if event.type == RED_HIT:
                del red_lives[-1]
            if event.type == YELLOW_HIT:
                del yellow_lives[-1]

        if not dead:
            keys_pressed = pygame.key.get_pressed()
            handle_bullets(yellow_bullets, red_bullets, yellow, red)
            handle_red_movement(keys_pressed, red, VELOCITY)
            if not ai:
                handle_yellow_movement(keys_pressed, yellow, VELOCITY)
            time_of_death = second
        elif second > time_of_death+5:
            # endgame(red_lives, yellow_lives, yellow_bullets, red_bullets, red, yellow)
            red_lives = [i for i in range(LIVES)]
            yellow_lives = [i for i in range(LIVES)]
            yellow_bullets = []
            red_bullets = []
            red.x, red.y = int(WIDTH * 0.75), HEIGHT // 2
            yellow.x, yellow.y = int(WIDTH * 0.25), HEIGHT // 2
            dead = False

        draw_window(red, yellow, red_bullets, yellow_bullets, red_lives, yellow_lives, dead)
    pygame.quit()


if __name__ == "__main__":
    main()
