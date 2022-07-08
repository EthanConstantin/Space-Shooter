import pygame
import os
pygame.mixer.init()

FPS = 120

WIDTH = 950
HEIGHT = WIDTH//1.77777777
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

VELOCITY = (WIDTH//129)//(FPS/60)
BULLET_VELOCITY = (WIDTH//90)//(FPS/60)

LIVES = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
RED_DEAD = pygame.USEREVENT + 3
YELLOW_DEAD = pygame.USEREVENT + 4

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Loading in sounds
soundObj = pygame.mixer.Sound(os.path.join("Assets","Assets_Gun+Silencer.mp3"))
soundObj.set_volume(0.3)

# Loading in the models
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = WIDTH//15, HEIGHT//12.5
YELLOW_SPACESHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "yellow_spaceship.png")), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
RED_SPACESHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "red_spaceship.png")), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space_background.jpg")), (WIDTH, HEIGHT))
BULLET_HEIGHT = int(WIDTH*0.01158)
BULLET_WIDTH = int(BULLET_HEIGHT*1.5455)
YELLOW_BULLET = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "yellow_ship_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
RED_BULLET = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "red_ship_bullet.png")), (BULLET_WIDTH, BULLET_HEIGHT))
GAME_OVER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "game_over.jpg")), (WIDTH, HEIGHT))
HEART = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "heart.png")), (25, 25))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_lives, yellow_lives, dead):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        WIN.blit(RED_BULLET, (bullet.x, bullet.y))
    for bullet in yellow_bullets:
        WIN.blit(YELLOW_BULLET, (bullet.x, bullet.y))

    for idi, i in enumerate(red_lives):
        WIN.blit(HEART, (WIDTH-35-idi*25, 15))
    for idi, i in enumerate(yellow_lives):
        WIN.blit(HEART, (idi*25+15, 15))

    if dead:
        WIN.blit(GAME_OVER, (0, 0))

    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow, velocity):
    if keys_pressed[pygame.K_a] and yellow.x > 0:  # LEFT
        yellow.x -= velocity
    if keys_pressed[pygame.K_d] and yellow.x + yellow.height < BORDER.x:  # RIGHT
        yellow.x += velocity
    if keys_pressed[pygame.K_w] and yellow.y > 0:  # UP
        yellow.y -= velocity
    if keys_pressed[pygame.K_s] and yellow.y + yellow.width < HEIGHT:  # DOWN
        yellow.y += velocity


def handle_red_movement(keys_pressed, red, velocity):
    if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width:  # LEFT
        red.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and red.x + red.height < WIDTH:  # RIGHT
        red.x += velocity
    if keys_pressed[pygame.K_UP] and red.y > 0:  # UP
        red.y -= velocity
    if keys_pressed[pygame.K_DOWN] and red.y + red.width < HEIGHT:  # DOWN
        red.y += velocity


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x + bullet.width < 0:
            red_bullets.remove(bullet)


def handle_endgame(red_lives, yellow_lives):
    pass

def main():
    # Drawing the ships on the window
    dead = False
    second = 0
    tod = 0
    red = RED_SPACESHIP.get_rect()
    red = red.move(int(WIDTH*0.75), HEIGHT//2)
    yellow = YELLOW_SPACESHIP.get_rect()
    yellow = yellow.move(int(WIDTH*0.25), HEIGHT//2)
    red_bullets = []
    yellow_bullets = []
    red_lives = [i for i in range(LIVES)]
    yellow_lives = [i for i in range(LIVES)]
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        second += 1/FPS
        if len(yellow_lives) == 0 or len(red_lives) == 0:
            dead = True
        else:
            dead = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and dead == False:
                if event.key == pygame.K_LCTRL:
                    soundObj.play()
                    yellow_bullets.append(pygame.Rect(yellow.x, yellow.y + yellow.height//2, 10, 5))
                if event.key == pygame.K_RCTRL:
                    red_bullets.append(pygame.Rect(red.x, red.y + red.height//2, 10, 5))

            if event.type == RED_HIT:
                del red_lives[-1]
            if event.type == YELLOW_HIT:
                del yellow_lives[-1]


        if dead == False:
            keys_pressed = pygame.key.get_pressed()
            handle_yellow_movement(keys_pressed, yellow, VELOCITY)
            handle_red_movement(keys_pressed, red, VELOCITY)

            handle_bullets(yellow_bullets, red_bullets, yellow, red)
            tod = second
        else:
            # handle_endgame(red_lives, yellow_lives)
            if second > tod+5:
                red_lives = [i for i in range(LIVES)]
                yellow_lives = [i for i in range(LIVES)]

        draw_window(red, yellow, red_bullets, yellow_bullets, red_lives, yellow_lives, dead)
    pygame.quit()


if __name__ == "__main__":
    main()
