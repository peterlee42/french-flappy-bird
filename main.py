import pygame
from pygame.locals import *
from constants import *
from random import randint, choice

pygame.init()

clock = pygame.time.Clock()
fps = 120

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

font = pygame.font.SysFont('Brush Script MT', 60)
font_two = pygame.font.SysFont('Brush Script MT', 30)
white = (255, 255, 255)
blue = (0, 0, 205)

# game variables
ground_scroll = 0
scroll_speed = 2

flying = False
game_over = False

pipe_gap = 200
pipe_freq = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_freq

score = 0
pass_pipe = False

coin_score_count = 0

one_tenth = screen_width / 10


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    food_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0

    return score


def draw_ingredient_name():
    draw_text('Ingrédients', font_two, blue, int(one_tenth + 35), 75)


def draw_coin_count():
    draw_text(str(coin_score_count),
              font, white, int(one_tenth * 2), 20)


def score_captions(variable):
    if variable == 1:
        draw_text('Ingrédients', font_two, blue, int(one_tenth * 2 - 42), 75)
    if variable == -1:
        draw_text('Score', font_two, blue, int(screen_width / 2 - 18), 75)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.birds = [bird_one, bird_two, bird_three]
        for bird in self.birds:
            img = bird
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        # gravity
        if flying == True:
            self.vel += 0.2
            if self.vel > 4:
                self.vel = 4
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -6

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # handle the animation
            self.counter += 1
            flap_cd = 10

            if self.counter > flap_cd:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            # rotate bird
            self.image = pygame.transform.rotate(
                self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(
                self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe
        self.rect = self.image.get_rect()
        # 1 = top, -1 - bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Foods(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = choice(foods)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        pos = pygame.mouse.get_pos()

        # check mouse is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.x))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

button = Button(screen_width // 2 - 50, screen_height //
                2 - 100, restart_button)


run = True
while run:

    clock.tick(fps)

    screen.blit(paris, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    food_group.draw(screen)

    screen.blit(ground, (ground_scroll, 768))

    # score check
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    if len(food_group) > 0:
        if pygame.sprite.groupcollide(bird_group, food_group, False, True):
            coin_score_count += 1
    draw_coin_count()

    score_captions(-1)
    score_captions(1)

    # look for collision
    # False1 = Birdgroup deleted, false2 = pipegroup deleted.
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

        # check ground collision
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_freq:
            random_foods = choice(foods)

            pipe_height = randint(-100, 100)

            btm_pipe = Pipe(screen_width, int(
                screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(
                screen_height / 2) + pipe_height, 1)

            food = Foods(screen_width + 5,
                         top_pipe.rect.bottom + 75)

            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)

            food_group.add(food)

            last_pipe = time_now

        screen.blit(ground, (ground_scroll, 768))
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()
        food_group.update()

    # check for game over + reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()
            coin_score_count = 0
            screen.blit(ground, (ground_scroll, 768))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()


pygame.quit()
