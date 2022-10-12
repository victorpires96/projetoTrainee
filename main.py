import pygame
import random

pygame.init()

WIDTH = HEIGHT = 539
FPS = 15
CLOCK = pygame.time.Clock()
ROUND_RUNNING = False
MARGIN = 1
PLAYER_X = random.randint(3, 8)
PLAYER_Y = random.randint(3, 8)
SCORE = -1
CURRENT_TIME = 0
SPAWN_TIME = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont('None', 20)

ENEMY_X, ENEMY_Y = 0, 0
enemy_type = ''
NUMBER_OF_ENEMIES = 5
ENEMY_X_POSITION = []
ENEMY_Y_POSITION = []
ENEMY_TYPES = []


def draw():
    SCREEN.fill(BLACK)

    for row in range(12):
        for column in range(12):
            if row == 0 or column == 0 or row == 11 or column == 11:
                color = GRAY
            else:
                color = WHITE
            pygame.draw.rect(SCREEN, color, [(WIDTH/12 + int(MARGIN)) * row,
                                             (HEIGHT/12 + int(MARGIN)) * column,
                                             WIDTH/15, HEIGHT/15])

    for i in range(NUMBER_OF_ENEMIES):
        pygame.draw.rect(SCREEN, RED, ((WIDTH / 12 + int(MARGIN)) * ENEMY_X_POSITION[i],
                                       (HEIGHT / 12 + int(MARGIN)) * ENEMY_Y_POSITION[i], WIDTH / 15, HEIGHT / 15))

    pygame.draw.rect(SCREEN, GREEN, ((WIDTH / 12 + int(MARGIN)) * PLAYER_X,
                                     (HEIGHT / 12 + int(MARGIN)) * PLAYER_Y, WIDTH / 15, HEIGHT / 15))

    SCORE_TEXT = FONT.render(f'Score: {SCORE}', True, RED)
    SCREEN.blit(SCORE_TEXT, (0, 0))

    pygame.display.flip()
    pygame.display.update()


def create_enemies():
    global ENEMY_X, ENEMY_Y, ENEMY_TYPES, enemy_type, SCORE, SPAWN_TIME, valido
    enemy_position = (0, 11)
    ENEMY_Y_POSITION.clear()
    ENEMY_X_POSITION.clear()
    ENEMY_TYPES.clear()
    SCORE += 1

    while len(ENEMY_TYPES) < NUMBER_OF_ENEMIES:
        possible_position = random.randrange(2)
        if possible_position == 0:
            ENEMY_X = random.choice(enemy_position)
            ENEMY_Y = random.randint(1, 10)
            if ENEMY_X == 0:
                enemy_type = 'left'
            else:
                enemy_type = 'right'
        elif possible_position == 1:
            ENEMY_X = random.randint(1, 10)
            ENEMY_Y = random.choice(enemy_position)
            if ENEMY_Y == 0:
                enemy_type = 'upper'
            else:
                enemy_type = 'lower'

        # print(f'x:{ENEMY_X}, y:{ENEMY_Y}, type:{enemy_type}')
        if len(ENEMY_TYPES) == 0:
            ENEMY_X_POSITION.append(ENEMY_X)
            ENEMY_Y_POSITION.append(ENEMY_Y)
            ENEMY_TYPES.append(enemy_type)
        else:
            for i in range(len(ENEMY_TYPES)):
                if not((ENEMY_X == ENEMY_Y_POSITION[i] and ENEMY_Y == ENEMY_X_POSITION[i])
                       or (enemy_type == ENEMY_TYPES[i] and ENEMY_X == ENEMY_X_POSITION[i])
                       or (enemy_type == ENEMY_TYPES[i] and ENEMY_Y == ENEMY_Y_POSITION[i])
                       or (ENEMY_X - ENEMY_Y_POSITION[i] == ENEMY_Y - ENEMY_X_POSITION[i])
                       or (enemy_type == 'left' and ENEMY_TYPES[i] == 'right' and ENEMY_Y == ENEMY_Y_POSITION[i])
                       or (enemy_type == 'right' and ENEMY_TYPES[i] == 'left' and ENEMY_Y == ENEMY_Y_POSITION[i])
                       or (enemy_type == 'upper' and ENEMY_TYPES[i] == 'lower' and ENEMY_X == ENEMY_X_POSITION[i])
                       or (enemy_type == 'lower' and ENEMY_TYPES[i] == 'upper' and ENEMY_X == ENEMY_X_POSITION[i])):
                    # print(f'valid entry, x,y,type {ENEMY_X}{ENEMY_Y}{enemy_type} compared to {ENEMY_X_POSITION[i]}{ENEMY_Y_POSITION[i]}{ENEMY_TYPES[i]}')
                    valido = True
                else:
                    valido = False
                    # print(f'number collides with previous entries x,y,type [{ENEMY_X}][{ENEMY_Y}]{enemy_type} compared to {ENEMY_X_POSITION[i]}{ENEMY_Y_POSITION[i]}{ENEMY_TYPES[i]}')
                    break
            if valido:
                ENEMY_X_POSITION.append(ENEMY_X)
                ENEMY_Y_POSITION.append(ENEMY_Y)
                ENEMY_TYPES.append(enemy_type)

    # print(f'{ENEMY_X_POSITION}, {ENEMY_Y_POSITION}, {ENEMY_TYPES}')
    SPAWN_TIME = pygame.time.get_ticks()


def enemy_movement():
    global ROUND_RUNNING, SCORE

    for i in range(NUMBER_OF_ENEMIES):
        if ENEMY_TYPES[i] == 'left':
            ENEMY_X_POSITION[i] += 1
        elif ENEMY_TYPES[i] == 'right':
            ENEMY_X_POSITION[i] -= 1
        elif ENEMY_TYPES[i] == 'upper':
            ENEMY_Y_POSITION[i] += 1
        elif ENEMY_TYPES[i] == 'lower':
            ENEMY_Y_POSITION[i] -= 1

    for i in range(NUMBER_OF_ENEMIES):
        if ENEMY_X_POSITION[i] > 11 or ENEMY_X_POSITION[i] < 0 or ENEMY_Y_POSITION[i] > 11 or ENEMY_Y_POSITION[i] < 0:
            create_enemies()
            break


def collision():
    global ROUND_RUNNING, SCORE
    for i in range(NUMBER_OF_ENEMIES):
        if ENEMY_X_POSITION[i] == PLAYER_X and ENEMY_Y_POSITION[i] == PLAYER_Y:
            ROUND_RUNNING = False
            print(f'you lost, with {SCORE} points')
            SCORE = 0
            break


def main_game():
    global PLAYER_Y, PLAYER_X, ROUND_RUNNING, SPAWN_TIME, CURRENT_TIME

    if not ROUND_RUNNING:
        create_enemies()
        ROUND_RUNNING = True

    while ROUND_RUNNING:
        CLOCK.tick(FPS)
        CURRENT_TIME = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ROUND_RUNNING = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ROUND_RUNNING = False
                    break
                if event.key == pygame.K_UP:
                    if PLAYER_Y > 1:
                        PLAYER_Y -= 1
                elif event.key == pygame.K_DOWN:
                    if PLAYER_Y < 10:
                        PLAYER_Y += 1
                elif event.key == pygame.K_RIGHT:
                    if PLAYER_X < 10:
                        PLAYER_X += 1
                elif event.key == pygame.K_LEFT:
                    if PLAYER_X > 1:
                        PLAYER_X -= 1

        draw()
        if CURRENT_TIME - SPAWN_TIME >= 1000:
            enemy_movement()
        collision()


if __name__ == '__main__':
    main_game()

pygame.quit()
