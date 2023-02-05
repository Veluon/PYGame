import pygame
import random
import os


def load_image(name):
    image = pygame.image.load(name)
    return image


def decode(file):
    result = []
    for i in file.readlines():
        pre_presult = []
        for j in i.strip():
            pre_presult.append(j)
        result.append(pre_presult)
    return result


def draw(arg, x, y, text):
    font = pygame.font.Font("data/fonts/font1.ttf", 30)
    text = font.render(text, True, (255, 255, 255))
    screen.blit(text, (x, y))


pygame.init()
size = 1024, 576
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
FPS = 60
lvl = 1

load_file = open(f"data/locations/lvl{str(lvl)}.txt", "r")
board_log = decode(load_file)

non_act_points = 0
act_points = 0

text_key = ""
ticks = 0


# классы


class Board:
    # создание поля
    def __init__(self, board_load):
        self.width = 32
        self.height = 18
        self.board = board_load
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 32
        self.spawn = (4 * 32, 6 * 32)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, arg):
        global non_act_points, act_points
        non_act_points = 0
        act_points = 0
        for w in range(self.width):
            for h in range(self.height):
                if self.board[h][w] == "O":
                    create_obj = Object(self.left + w * self.cell_size, self.top + h * self.cell_size,
                                        "data/sprites/objects/wall1.jpg")
                    collide_sprites.add(create_obj)
                    all_sprites.add(create_obj)

                elif self.board[h][w] == "#":
                    create_obj = Object(self.left + w * self.cell_size, self.top + h * self.cell_size,
                                        "data/sprites/objects/floor2.jpg")
                    all_sprites.add(create_obj)

                elif self.board[h][w] == "P":
                    create_obj = Point(self.left + w * self.cell_size, self.top + h * self.cell_size)
                    all_sprites.add(create_obj)
                    non_act_points += 1

                elif self.board[h][w] == "L":
                    create_obj = DamageObject(self.left + w * self.cell_size, self.top + h * self.cell_size)
                    all_sprites.add(create_obj)

                elif self.board[h][w] == "N":
                    create_obj = Portal(self.left + w * self.cell_size, self.top + h * self.cell_size)
                    all_sprites.add(create_obj)

                elif self.board[h][w] == "S":
                    create_obj = Object(self.left + w * self.cell_size, self.top + h * self.cell_size,
                                        "data/sprites/objects/floor2.jpg")
                    all_sprites.add(create_obj)
                    board.spawn = (self.left + w * self.cell_size, self.top + h * self.cell_size)


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, name, size=(32, 32)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image = load_image(name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect = self.rect


class DamageObject(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image = load_image("data/sprites/int_objects/spikes.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = False
        self.key = False

    def update(self):
        global collide_sprites, all_sprites, tick
        self.rect = self.rect
        if tick % 100 == 0:
            self.active = not self.active
            if self.active is True:
                self.image = load_image("data/sprites/int_objects/active_spikes.jpg")
            else:
                self.image = load_image("data/sprites/int_objects/spikes.jpg")
                self.key = True
        elif tick % 50 == 0 and self.key is True:
            self.image = load_image("data/sprites/int_objects/pre_active_spikes.jpg")
            self.key = False
        if pygame.sprite.spritecollideany(self, character_group):
            if self.active is True:
                collide_sprites = pygame.sprite.Group()
                all_sprites = pygame.sprite.Group()
                board.render(screen)
                character_group.draw(screen)
                character.rect.x = board.spawn[0]
                character.rect.y = board.spawn[1]


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image = load_image("data/sprites/int_objects/point.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = False

    def update(self):
        global act_points
        self.rect = self.rect
        if self.active is False:
            self.image = load_image("data/sprites/int_objects/point.jpg")
        else:
            self.image = load_image("data/sprites/int_objects/complete_point.jpg")
        if pygame.sprite.spritecollideany(self, character_group) and self.active is False:
            self.active = True
            act_points += 1


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image = load_image("data/sprites/int_objects/portal.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global lvl, load_file, board_log, all_sprites, board, collide_sprites, text_key
        if pygame.sprite.spritecollideany(self, character_group):
            if lvl < len(os.listdir("data/locations")) and act_points == non_act_points:
                collide_sprites = pygame.sprite.Group()
                all_sprites = pygame.sprite.Group()

                lvl += 1

                load_file = open(f"data/locations/lvl{str(lvl)}.txt", "r")
                board_log = decode(load_file)
                board = Board(board_log)
                board.render(screen)

                character.rect.x = board.spawn[0]
                character.rect.y = board.spawn[1]

                character_group.draw(screen)
            elif lvl >= len(os.listdir("data/locations")):
                character.rect.x = board.spawn[0]
                character.rect.y = board.spawn[1]
                text_key = "Игра пройдена"
            else:
                character.rect.x = board.spawn[0]
                character.rect.y = board.spawn[1]
                text_key = "Активируйте все точки"


class MainCharacter(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image = load_image("data/sprites/character/character_up.png")
        self.rect = self.image.get_rect()
        self.rect.x = 4 * 32
        self.rect.y = 6 * 32
        self.v = 2

        self.w_move = False
        self.s_move = False
        self.a_move = False
        self.d_move = False

    def update(self, *args):
        if self.w_move:
            self.image = load_image("data/sprites/character/character_up.png")
            self.rect.y -= self.v
            if pygame.sprite.spritecollideany(self, collide_sprites):
                self.rect.y += self.v
        if self.s_move:
            self.image = load_image("data/sprites/character/character_down.png")
            self.rect.y += self.v
            if pygame.sprite.spritecollideany(self, collide_sprites):
                self.rect.y -= self.v
        if self.a_move:
            self.image = load_image("data/sprites/character/character_left.png")
            self.rect.x -= self.v
            if pygame.sprite.spritecollideany(self, collide_sprites):
                self.rect.x += self.v
        if self.d_move:
            self.image = load_image("data/sprites/character/character_right.png")
            self.rect.x += self.v
            if pygame.sprite.spritecollideany(self, collide_sprites):
                self.rect.x -= self.v


# группа, содержащая все спрайты
collide_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
character_group = pygame.sprite.Group()

character = MainCharacter()
character_group.add(character)

board = Board(board_log)

tick = 0

# Всякое

running = True

board.render(screen)
character_group.draw(screen)
while running:
    clock.tick(FPS)
    all_sprites.update()
    character_group.update()
    tick += 1
    for event in pygame.event.get():
        draw(screen, 30, 255, "Активируйте все точки")
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.render(screen)
                character_group.draw(screen)

            if event.key == pygame.K_w:
                character.w_move = True
            if event.key == pygame.K_s:
                character.s_move = True
            if event.key == pygame.K_a:
                character.a_move = True
            if event.key == pygame.K_d:
                character.d_move = True
            if event.key == pygame.K_LSHIFT:
                character.v = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                character.w_move = False
            if event.key == pygame.K_s:
                character.s_move = False
            if event.key == pygame.K_a:
                character.a_move = False
            if event.key == pygame.K_d:
                character.d_move = False
            if event.key == pygame.K_LSHIFT:
                character.v = 2

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x = x // board.cell_size
            y = y // board.cell_size
            if not (0 <= x <= board.width and 0 <= y <= board.height):
                pos = None
            else:
                pos = x, y
            print(pos)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    if text_key != "":
        draw(screen, 64, 255, text_key)
        ticks += 1
        if ticks > 300:
            text_key = ""
            ticks = 0

    character_group.draw(screen)
    pygame.display.flip()
