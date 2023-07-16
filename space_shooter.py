import pygame
import os
import random
from screeninfo import get_monitors
pygame.mixer.init()
pygame.init()

FPS = 165

# Thanks to misha

FIRE_RATE = 0.215  # Fire a bullet every 0.215 seconds

# Window you play on
# WIDTH = 1350
WIDTH = [i.width for i in get_monitors()][-1]
# HEIGHT = WIDTH // 1.77777777
HEIGHT = [i.height for i in get_monitors()][-1]
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

font = pygame.font.Font(None,30)

# Variables that scale with aspect ratio and fps
VELOCITY = (WIDTH // 129) // (FPS / 60)
BULLET_VELOCITY = (WIDTH // 90) // (FPS / 60)

LIVES = 5

# RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Border that separates the ships
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Loading in sounds
bullet_sound = pygame.mixer.Sound(os.path.join("Assets", "Assets_Gun+Silencer.mp3"))
bullet_sound.set_volume(0.02)

# Loading in models
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = WIDTH // 15, HEIGHT // 12.5
YELLOW_SPACESHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "yellow_spaceship.png")), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
RED_SPACESHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "red_spaceship.png")), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space_background.jpg")), (WIDTH, HEIGHT))

# Loading in buttons
QUIT_BTN = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Quit_btn.png")), (100, 31))

BUTTON_WIDTH, BUTTON_HEIGHT = 91, 62
BUTTON_1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "button_1.png")),
                                  (BUTTON_WIDTH, BUTTON_HEIGHT))
BUTTON_2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "button_2.png")),
                                  (BUTTON_WIDTH, BUTTON_HEIGHT))
BUTTON_3 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "button_3.png")),
                                  (BUTTON_WIDTH, BUTTON_HEIGHT))
BUTTON_4 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "button_4.png")),
                                  (BUTTON_WIDTH, BUTTON_HEIGHT))
BUTTON_5 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "button_5.png")),
                                  (BUTTON_WIDTH, BUTTON_HEIGHT))
BUTTON_6 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "button_6.png")),
                                  (BUTTON_WIDTH, BUTTON_HEIGHT))
BUTTON_7 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "button_7.png")),
                                  (BUTTON_WIDTH, BUTTON_HEIGHT))
ai_buttons = [BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4, BUTTON_5, BUTTON_6, BUTTON_7]

BULLET_HEIGHT = int(WIDTH * 0.0105)
BULLET_WIDTH = int(BULLET_HEIGHT * 1.5545)
YELLOW_BULLET = pygame.transform.scale(pygame.image.load(os.path.join(
    "Assets", "yellow_ship_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
RED_BULLET = pygame.transform.scale(pygame.image.load(os.path.join(
    "Assets", "red_ship_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))

GAME_OVER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "game_over.jpg")), (WIDTH, HEIGHT))

HEART_DIMENSIONS = WIDTH//38
HEART = pygame.transform.scale(pygame.image.load(os.path.join(
    "Assets", "heart.png")), (HEART_DIMENSIONS, HEART_DIMENSIONS))


def draw_window(red, yellow, QUIT, red_bullets, yellow_bullets, red_lives, yellow_lives, dead, pause, buttons):
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
        WIN.blit(HEART, (WIDTH - WIDTH // 27.143 - idi * HEART_DIMENSIONS, 15))
    for idi, i in enumerate(yellow_lives):
        WIN.blit(HEART, (idi * HEART_DIMENSIONS + WIDTH // 63.33, 15))

    if pause:
        WIN.fill(WHITE)

        for idi, i in enumerate(ai_buttons):
            x = BUTTON_WIDTH*1.5*(len(ai_buttons)/2) + idi*BUTTON_WIDTH*1.5
            y = int(HEIGHT/2 - BUTTON_HEIGHT/2)
            buttons.append(i.get_rect().move(x, y))
            WIN.blit(i, (x, y))

        WIN.blit(QUIT_BTN, QUIT)

    if dead:
        WIN.blit(GAME_OVER, (0, 0))

    pygame.display.update()


def yellow_movement(keys_pressed, yellow, velocity):
    if keys_pressed[pygame.K_a] and yellow.x > 0:  # LEFT
        yellow.x -= velocity
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width < BORDER.x:  # RIGHT
        yellow.x += velocity
    if keys_pressed[pygame.K_w] and yellow.y > 0:  # UP
        yellow.y -= velocity
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height < HEIGHT:  # DOWN
        yellow.y += velocity


def red_movement(keys_pressed, red, velocity):
    if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width:  # LEFT
        red.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width < WIDTH:  # RIGHT
        red.x += velocity
    if keys_pressed[pygame.K_UP] and red.y > 0:  # UP
        red.y -= velocity
    if keys_pressed[pygame.K_DOWN] and red.y + red.height < HEIGHT:  # DOWN
        red.y += velocity


def bullets(yellow_bullets, red_bullets, yellow, red, red_hit, yellow_hit):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):  # If yellow bullet hits red
            # pygame.event.post(pygame.event.Event(RED_HIT))
            red_hit[0] = True
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH or bullet.y > HEIGHT or bullet.y < 0:
            yellow_bullets.remove(bullet)  # Deleting bullets that go offscreen
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):  # If red bullet hits yellow
            # pygame.event.post(pygame.event.Event(YELLOW_HIT))
            yellow_hit[0] = True
            red_bullets.remove(bullet)
        if bullet.x + bullet.width < 0 or bullet.y > HEIGHT or bullet.y < 0:
            red_bullets.remove(bullet)  # Deleting bullets that go offscreen


def yellow_shoot(yellow, yellow_bullets):
    yellow_bullets.append(pygame.Rect(yellow.x, yellow.y + yellow.height // 2, 10, 5))
    bullet_sound.play()


def red_shoot(red, red_bullets):
    red_bullets.append(pygame.Rect(red.x, red.y + red.height // 2, 10, 5))
    bullet_sound.play()


def ai_lvl1(yellow, yellow_bullets, second, ai_last_shot_time, velocity, move_oscillator, dead):
    if not dead:
        if second - ai_last_shot_time[0] >= 1.5:  # If it's been more than 1.5 seconds since the ai last shot
            ai_last_shot_time[0] = second  # Reset timer
            yellow_shoot(yellow, yellow_bullets)
            move_oscillator[0] = 0
        if second - ai_last_shot_time[0] >= 0.75:  # If it's been more than 0.75 seconds since the ai last shot
            move_oscillator[0] = 1
        # Moving the ship up and down periodically
        if move_oscillator[0] == 0 and yellow.y > 0:
            yellow.y -= velocity // 1.5
        elif move_oscillator[0] == 1 and yellow.y + yellow.height < HEIGHT:
            yellow.y += velocity // 1.5


def ai_lvl2(yellow, yellow_bullets, second, ai_last_shot_time, velocity, random_move, ai_last_move_time, dead):
    if not dead:
        if second - ai_last_shot_time[0] >= 0.9:  # If it's been more than 0.9 seconds since the ai last shot
            ai_last_shot_time[0] = second  # Reset timer
            yellow_shoot(yellow, yellow_bullets)
        if second - ai_last_move_time[0] >= 0.6:  # If it's been more than 0.6 seconds since the ai last moved
            random_move[0] = random.randint(0, 8)
            ai_last_move_time[0] = second  # Reset timer
        elif second - ai_last_move_time[0] >= random.uniform(1, 2):
            # If it's been more than (random float between 1 and 2) seconds since the ai last moved, don't move anymore
            random_move[0] = 0

        # 25% chance to move left or right
        if random_move[0] == 1 and yellow.x > 0:  # LEFT
            yellow.x -= velocity * 0.6
        elif random_move[0] == 2 and yellow.x + yellow.width < BORDER.x:  # RIGHT
            yellow.x += velocity * 0.6
        # 75% chance to move up or down
        elif 5 >= random_move[0] >= 3 and yellow.y > 0:  # UP
            yellow.y -= velocity * 0.7
        elif 8 >= random_move[0] >= 6 and yellow.y + yellow.height < HEIGHT:  # DOWN
            yellow.y += velocity * 0.7
        # elif random_move[0] == 0:  # STAY STILL
        #     pass


def ai_lvl3(yellow, yellow_bullets, second, ai_last_shot_time, velocity, random_move, ai_last_move_time, dead):
    if not dead:
        if second - ai_last_shot_time[0] >= 0.75:  # If it's been more than 0.75 seconds since the ai last shot
            ai_last_shot_time[0] = second  # Reset timer
            yellow_shoot(yellow, yellow_bullets)
        if second - ai_last_move_time[0] >= 0.3:  # If it's been more than 0.3 seconds since the ai last moved
            random_move[0] = random.randint(0, 8)
            ai_last_move_time[0] = second  # Reset timer
        elif second - ai_last_move_time[0] >= random.uniform(1, 3):
            # If it's been more than (random float between 1 and 3) seconds since the ai last moved, don't move anymore
            random_move[0] = 0

        # 25% chance to move left or right
        if random_move[0] == 1 and yellow.x > 0:  # LEFT
            yellow.x -= velocity * 0.8
        elif random_move[0] == 2 and yellow.x + yellow.width < BORDER.x:  # RIGHT
            yellow.x += velocity * 0.8
        # 75% chance to move up or down
        elif 5 >= random_move[0] >= 3 and yellow.y > 0:  # UP
            yellow.y -= velocity * 0.9
        elif 8 >= random_move[0] >= 6 and yellow.y + yellow.height < HEIGHT:  # DOWN
            yellow.y += velocity * 0.9
        # elif random_move[0] == 0:  # STAY STILL
        #     pass


def ai_lvl_4(yellow, yellow_bullets, red, second, dead,
             ai_last_shot_time, velocity, ai_last_move_time):
    if not dead:
        if second - ai_last_shot_time[0] >= 0.7 and abs(red.y - yellow.y) <= SPACESHIP_HEIGHT:
            ai_last_shot_time[0] = second  # Reset timer
            yellow_shoot(yellow, yellow_bullets)
        if second - ai_last_move_time[0] >= 0.3:
            if 0 - SPACESHIP_HEIGHT // 2 > red.y - yellow.y and yellow.y > 0:
                yellow.y -= velocity * 0.8
            if red.y - yellow.y >= SPACESHIP_HEIGHT // 2 and yellow.y + yellow.height < HEIGHT:
                yellow.y += velocity * 0.8
            if 0 - SPACESHIP_HEIGHT < red.y - yellow.y < SPACESHIP_HEIGHT:
                ai_last_move_time[0] = second


def ai_lvl_5(yellow, yellow_bullets, red, red_bullets, second, dead,
             ai_last_shot_time, velocity, ai_last_move_time):
    if not dead:
        bullet_near = False
        if len(red_bullets) > 0:
            for bullet in red_bullets:
                if abs(yellow.x - bullet.x) <= (60 * (WIDTH // 129)) * FIRE_RATE:
                    # (60*(WIDTH//129))*FIRE_RATE is simplified FPS * VELOCITY * FIRE_RATE which is the distance
                    # travelled of a red bullet after 0.215 seconds, the maximum fire rate of a red bullet.
                    # It is the minimum distance between bullets
                    if (0 > yellow.y + (SPACESHIP_HEIGHT//2) - bullet.y + (BULLET_HEIGHT//2) > 1-SPACESHIP_HEIGHT) \
                            and yellow.y > 0:
                        yellow.y -= VELOCITY
                        bullet_near = True
                    if (0 <= yellow.y + (SPACESHIP_HEIGHT // 2) - bullet.y + (BULLET_HEIGHT // 2) < SPACESHIP_HEIGHT) \
                            and yellow.y + yellow.height < HEIGHT:
                        yellow.y += VELOCITY
                        bullet_near = True
        if second - ai_last_shot_time[0] >= 0.8 and abs(red.y - yellow.y) <= SPACESHIP_HEIGHT:
            ai_last_shot_time[0] = second  # Reset timer
            yellow_shoot(yellow, yellow_bullets)
        if not bullet_near and second - ai_last_move_time[0] >= 0.3:
            if 0 - SPACESHIP_HEIGHT // 2 > red.y - yellow.y and yellow.y > 0:
                yellow.y -= velocity * 0.8
            if red.y - yellow.y >= SPACESHIP_HEIGHT // 2 and yellow.y + yellow.height < HEIGHT:
                yellow.y += velocity * 0.8
            if 0 - SPACESHIP_HEIGHT < red.y - yellow.y < SPACESHIP_HEIGHT:
                ai_last_move_time[0] = second


def ai_lvl_6(yellow, yellow_bullets, red, red_bullets, second, dead,
             ai_last_shot_time, velocity, ai_last_move_time):
    if not dead:
        bullet_near = False
        if len(red_bullets) > 0:
            for bullet in red_bullets:
                if abs(yellow.x - bullet.x) <= (60 * (WIDTH // 129)) * FIRE_RATE:
                    if (0 > yellow.y + (SPACESHIP_HEIGHT // 2) - bullet.y + (
                            BULLET_HEIGHT // 2) > 1 - SPACESHIP_HEIGHT * 1.2) \
                            and yellow.y > 0:
                        yellow.y -= VELOCITY
                        bullet_near = True
                    if (0 <= yellow.y + (SPACESHIP_HEIGHT // 2) - bullet.y + (
                            BULLET_HEIGHT // 2) < SPACESHIP_HEIGHT * 1.2) \
                            and yellow.y + yellow.height < HEIGHT:
                        yellow.y += VELOCITY
                        bullet_near = True
        if second - ai_last_shot_time[0] >= 0.5:
            ai_last_shot_time[0] = second  # Reset timer
            yellow_shoot(yellow, yellow_bullets)
        if not bullet_near and second - ai_last_move_time[0] >= 0.2:
            if 0 - SPACESHIP_HEIGHT // 2 > red.y - yellow.y and yellow.y > 0:
                yellow.y -= velocity  # UP
            if red.y - yellow.y >= SPACESHIP_HEIGHT // 2 and yellow.y + yellow.height < HEIGHT:
                yellow.y += velocity  # DOWN
            if 0 - SPACESHIP_HEIGHT < red.y - yellow.y < SPACESHIP_HEIGHT:
                ai_last_move_time[0] = second


def ai_lvl_7(yellow, yellow_bullets, red, red_bullets, second, dead,
             ai_last_shot_time, velocity, ai_last_move_time):
    if not dead:
        bullet_near_1 = False
        bullet_near_2 = False
        bullet_near_2_up = False
        bullet_near_2_down = False
        if len(red_bullets) > 0:
            for idi, bullet in enumerate(red_bullets):
                if abs(yellow.x - bullet.x) <= (60 * (WIDTH // 129)) * FIRE_RATE:
                    if (SPACESHIP_HEIGHT * 1.1 > yellow.y + (SPACESHIP_HEIGHT//2) - bullet.y + (BULLET_HEIGHT//2)
                    > 1 - SPACESHIP_HEIGHT * 1.1) and len(red_bullets) >= idi + 2:
                        bullet_near_2 = red_bullets[idi+1]
                        if bullet_near_2.x <= (60 * (WIDTH // 129)) * FIRE_RATE * 2.5:
                            if (0 <= yellow.y + (SPACESHIP_HEIGHT // 2) - bullet.y + (
                            BULLET_HEIGHT // 2) < SPACESHIP_HEIGHT * 1.2):
                                bullet_near_2_down = True
                            if (0 > yellow.y + (SPACESHIP_HEIGHT // 2) - bullet.y + (
                            BULLET_HEIGHT // 2) > 1 - SPACESHIP_HEIGHT * 1.2):
                                bullet_near_2_up = True
                    if bullet_near_2_down and yellow.y > 0:
                        yellow.y -= VELOCITY  # UP
                    if bullet_near_2_up and yellow.y + yellow.height < HEIGHT:
                        yellow.y -= VELOCITY  # DOWN
                    elif (0 > yellow.y + (SPACESHIP_HEIGHT // 2) - bullet.y + (
                            BULLET_HEIGHT // 2) > 1 - SPACESHIP_HEIGHT * 1.2) \
                            and yellow.y > 0:
                        yellow.y -= VELOCITY  # UP
                    #     bullet_near_1 = True
                    # elif (0 <= yellow.y + (SPACESHIP_HEIGHT // 2) - bullet.y + (
                    #         BULLET_HEIGHT // 2) < SPACESHIP_HEIGHT * 1.2) \
                    #         and yellow.y + yellow.height < HEIGHT and not bullet_near_2_up:
                    #     yellow.y += VELOCITY  # DOWN
                    #     bullet_near_1 = True
        if second - ai_last_shot_time[0] >= 0.5:
            ai_last_shot_time[0] = second  # Reset timer
            yellow_shoot(yellow, yellow_bullets)
        if not bullet_near_1 and not bullet_near_2_up and not bullet_near_2_down\
                and second - ai_last_move_time[0] >= 0.2:
            if 0 - SPACESHIP_HEIGHT // 2 > red.y - yellow.y and yellow.y > 0:
                yellow.y -= velocity
            if red.y - yellow.y >= SPACESHIP_HEIGHT // 2 and yellow.y + yellow.height < HEIGHT:
                yellow.y += velocity
            if 0 - SPACESHIP_HEIGHT < red.y - yellow.y < SPACESHIP_HEIGHT:
                ai_last_move_time[0] = second


# def endgame(red_lives, yellow_lives, yellow_bullets, red_bullets, red, yellow):
#     red_lives = [i for i in range(LIVES)]
#     yellow_lives = [i for i in range(LIVES)]
#     yellow_bullets = []
#     red_bullets = []
#     red.x, red.y = int(WIDTH * 0.75), HEIGHT // 2
#     yellow.x, yellow.y = int(WIDTH * 0.25), HEIGHT // 2


def main():
    # AI variables
    random_move = [0]  # List so it's mutable
    ai_last_shot_time = [0]
    ai_last_move_time = [0]
    move_oscillator = [0]
    ai_lvl = 6
    ai = True
    # Drawing the hit_box for the ships
    red = RED_SPACESHIP.get_rect().move(int(WIDTH*0.75-SPACESHIP_WIDTH/2), HEIGHT // 2)
    yellow = YELLOW_SPACESHIP.get_rect().move(int(WIDTH * 0.25-SPACESHIP_WIDTH/2), HEIGHT // 2)

    QUIT = QUIT_BTN.get_rect().move(WIDTH // 2 - 50, 10)

    buttons = []

    red_hit = [False]
    yellow_hit = [False]
    red_dead = [False]
    yellow_dead = [False]

    pause = False

    red_bullets = []
    yellow_bullets = []
    red_lives = [i for i in range(LIVES)]
    yellow_lives = [i for i in range(LIVES)]
    second = 0  # Time
    red_last_shot_time = 0
    yellow_last_shot_time = 0
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        clock.tick(FPS)  # Caps framerate
        second += 1 / FPS  # Keeps track of time
        pos = pygame.mouse.get_pos()

        if len(yellow_lives) == 0 or len(red_lives) == 0:
            dead = True
        else:
            dead = False


        if ai and not pause:
            if ai_lvl == 1:
                ai_lvl1(yellow, yellow_bullets, second, ai_last_shot_time, VELOCITY, move_oscillator, dead)
            elif ai_lvl == 2:
                ai_lvl2(yellow, yellow_bullets, second, ai_last_shot_time,
                        VELOCITY, random_move, ai_last_move_time, dead)
            elif ai_lvl == 3:
                ai_lvl3(yellow, yellow_bullets, second, ai_last_shot_time, VELOCITY, random_move, ai_last_move_time,
                        dead)
            elif ai_lvl == 4:
                ai_lvl_4(yellow, yellow_bullets, red, second, dead,
                         ai_last_shot_time, VELOCITY, ai_last_move_time)
            elif ai_lvl == 5:
                ai_lvl_5(yellow, yellow_bullets, red, red_bullets, second, dead,
                         ai_last_shot_time, VELOCITY, ai_last_move_time)
            elif ai_lvl == 6:
                ai_lvl_6(yellow, yellow_bullets, red, red_bullets, second, dead,
                         ai_last_shot_time, VELOCITY, ai_last_move_time)
            elif ai_lvl == 7:
                ai_lvl_7(yellow, yellow_bullets, red, red_bullets, second, dead,
                         ai_last_shot_time, VELOCITY, ai_last_move_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            # Shooting
            if event.type == pygame.KEYDOWN and not dead and not pause:
                if event.key == pygame.K_LCTRL and not ai and second - yellow_last_shot_time >= FIRE_RATE:
                    yellow_last_shot_time = second
                    yellow_shoot(yellow, yellow_bullets)
                if event.key == pygame.K_RCTRL and second - red_last_shot_time >= FIRE_RATE:
                    red_last_shot_time = second
                    red_shoot(red, red_bullets)
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    pause = True

        if pygame.mouse.get_pressed()[0] and pause:
            pos = pygame.mouse.get_pos()
            if QUIT.collidepoint(pos):
                raise SystemExit
            # for i in range(7):
            #     if buttons[i-1].collidepoint(pos):
            #         ai_lvl = i
            #         dead = True
            if buttons[0].collidepoint(pos):
                ai_lvl = 1
                dead = True
            if buttons[1].collidepoint(pos):
                ai_lvl = 2
                dead = True
            if buttons[2].collidepoint(pos):
                ai_lvl = 3
                dead = True
            if buttons[3].collidepoint(pos):
                ai_lvl = 4
                dead = True
            if buttons[4].collidepoint(pos):
                ai_lvl = 5
                dead = True
            if buttons[5].collidepoint(pos):
                ai_lvl = 6
                dead = True
            if buttons[6].collidepoint(pos):
                ai_lvl = 7
                dead = True
            pause = False

        if red_hit[0]:
            del red_lives[-1]
            red_hit[0] = False
        if yellow_hit[0]:
            del yellow_lives[-1]
            yellow_hit[0] = False

        if not dead and not pause:
            bullets(yellow_bullets, red_bullets, yellow, red, red_hit, yellow_hit)
            keys_pressed = pygame.key.get_pressed()
            red_movement(keys_pressed, red, VELOCITY)
            if not ai:
                yellow_movement(keys_pressed, yellow, VELOCITY)
        elif dead:
            if GAME_OVER.get_rect().collidepoint(pos) and pygame.mouse.get_pressed()[0]:  # Left click
                red_lives = [i for i in range(LIVES)]
                yellow_lives = [i for i in range(LIVES)]
                yellow_bullets = []
                red_bullets = []
                red.x, red.y = int(WIDTH * 0.75), HEIGHT // 2
                yellow.x, yellow.y = int(WIDTH * 0.25), HEIGHT // 2
                dead = False
        draw_window(red, yellow, QUIT, red_bullets, yellow_bullets, red_lives, yellow_lives, dead, pause, buttons)


if __name__ == "__main__":
    main()
