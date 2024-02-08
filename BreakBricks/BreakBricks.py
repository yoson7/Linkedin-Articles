import pygame, pygame.gfxdraw, random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    KEYDOWN,
    K_ESCAPE,
    QUIT
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# ===============  Create Bricks  ===============

def create_bricks():

    bricks = pygame.sprite.Group()

    for x in range(10):
        if (x % 2) == 1:
            length = 0
        else:
            length = -20
        for y in range(21):
            height = 100 + (x * 20)
            length_position = length + (y * 40)
            br = Bricks()
            br.rect.left = length_position
            br.rect.top = height
            bricks.add(br)

    return  bricks

# ===============  Paint Bricks  ===============

def random_color():
    accepted = False
    while not accepted:
        a = random.randrange(0,255)
        b = random.randrange(0,255)
        c = random.randrange(0,255)

        if ((a > 20) or (b > 20) or (c > 20)):
            color = (a, b, c)
            accepted = True

    return color


# ===============  Change direction  ===============
def change_direction(direction, collision):
    if direction == 'up-right' and collision == 'right':
        direction = 'up-left'
    if direction == 'down-right' and collision == 'right':
        direction = 'down-left'
    if direction == 'up-left' and collision == 'left':
        direction = 'up-right'
    if direction == 'down-left' and collision == 'left':
        direction = 'down-right'
    if direction == 'up-right' and collision == 'top':
        direction = 'down-right'
    if direction == 'up-left' and collision == 'top':
        direction = 'down-left'
    if direction == 'down-right' and collision == 'bottom':
        direction = 'up-right'
    if direction == 'down-left' and collision == 'bottom':
        direction = 'up-left'

    return direction

# ===============  Check bricks collision  ===============

def bricks_collision(ball, brick):
    if ((ball.rect.top + 1) or (ball.rect.top) or (ball.rect.top - 1)) == brick.rect.bottom:
        colision = 'top'
    elif ((ball.rect.bottom + 1) or (ball.rect.bottom) or (ball.rect.bottom - 1)) == brick.rect.top:
        colision = 'bottom'
    elif ((ball.rect.right + 1) or (ball.rect.right) or (ball.rect.right - 1)) == brick.rect.left:
        colision = 'right'
    elif ((ball.rect.left + 1) or (ball.rect.left) or (ball.rect.left - 1)) == brick.rect.right:
        colision = 'left'
    else:
        colision = 'none'

    return colision


# ===============  Player  ===============
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = ((SCREEN_WIDTH / 2), 585))

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

# ===============  Ball  ===============

class Ball(pygame.sprite.Sprite):
    def __init__(self):
         super(Ball, self).__init__()
         circle = pygame.Surface((32, 32), pygame.SRCALPHA)
         pygame.draw.circle(circle, (255, 255, 255), (16, 16), 8, 16)
         self.surf = circle
         self.rect = self.surf.get_rect(center=(random.randrange(5, 790), 550))

    def update(self, direction):

        if self.rect.right > SCREEN_WIDTH:
            direction = change_direction(direction, 'right')

        if self.rect.left < 0:
            direction = change_direction(direction, 'left')

        if self.rect.top < 0:
            direction = change_direction(direction, 'top')

        if self.rect.top > (SCREEN_HEIGHT + 5):
            self.kill()


        if direction == 'up-right':
            self.rect.move_ip(1, -1)
        if direction == 'up-left':
            self.rect.move_ip(-1, -1)
        if direction == 'down-right':
            self.rect.move_ip(1, 1)
        if direction == 'down-left':
            self.rect.move_ip(-1, 1)

        return direction

# ===============  Bricks  ===============
class Bricks(pygame.sprite.Sprite):
    def __init__(self):
        super(Bricks, self).__init__()
        color = random_color()
        self.surf = pygame.Surface((40, 20))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        pygame.draw.rect(self.surf, (128,128,128), (0, 0, 40, 20), 2)

    def update(self):
        if self.surf.get_at((5, 5))[:3] != (0,0,0):
            color = self.surf.get_at((5, 5))[:3]
            self.surf.fill((0, 0, 0))
            pygame.draw.rect(self.surf, color, (0, 0, 40, 20), 2)
        else:
            self.kill()

# ===============  Run the game  ===============

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("BreakBricks")
bricks = create_bricks()
all_sprites = pygame.sprite.Group()
ball = Ball()
player = Player()

players = pygame.sprite.Group(player)
all_sprites.add(ball, player)

for x in bricks:
    all_sprites.add(x)

clock = pygame.time.Clock()
running = True
direction = 'up-right'

while running:
    for x in pygame.event.get():
        if x.type == KEYDOWN:

            if x.key == K_ESCAPE:
                running = False


        elif x.type == QUIT:
            running = False

    if pygame.sprite.spritecollideany(ball, players):
        direction = change_direction(direction, 'bottom')

    brick_col = pygame.sprite.spritecollide(ball, bricks, False)
    if brick_col:

        collision = bricks_collision(ball, brick_col[0])
        if collision != 'none':
            brick_col[0].update()
            direction = change_direction(direction, collision)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    direction = ball.update(direction)
    screen.fill((0,0,0))

    for spr in all_sprites:
        screen.blit(spr.surf, spr.rect)

    pygame.display.flip()
    clock.tick(200)

pygame.quit()