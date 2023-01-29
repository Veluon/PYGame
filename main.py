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


def main():
    pygame.init()
    size = 1024, 576
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Game')
    clock = pygame.time.Clock()
    FPS = 60

    # классы

    class CollideObject(pygame.sprite.Sprite):
        def __init__(self, x, y, name):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((32, 32))
            self.image = load_image(name)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            self.rect = self.rect

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
            self.rect = self.rect
            if self.active is False:
                self.image = load_image("data/sprites/int_objects/point.jpg")
            else:
                self.image = load_image("data/sprites/int_objects/complete_point.jpg")
            if pygame.sprite.spritecollideany(self, character_group):
                self.active = True

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

        # настройка внешнего вида
        def set_view(self, left, top, cell_size):
            self.left = left
            self.top = top
            self.cell_size = cell_size

        def render(self, arg):
            for w in range(self.width):
                for h in range(self.height):
                    if self.board[h][w] == "O":
                        create_obj = CollideObject(self.left + w * self.cell_size, self.top + h * self.cell_size,
                                                   "data/sprites/objects/wall1.jpg")
                        collide_sprites.add(create_obj)
                        all_sprites.add(create_obj)

                    elif self.board[h][w] == "#":
                        create_obj = CollideObject(self.left + w * self.cell_size, self.top + h * self.cell_size,
                                                   "data/sprites/objects/floor1.jpg")
                        all_sprites.add(create_obj)

                    elif self.board[h][w] == "P":
                        create_obj = Point(self.left + w * self.cell_size, self.top + h * self.cell_size)
                        all_sprites.add(create_obj)
                        points.add(create_obj)
                    elif self.board[h][w] == "S":
                        pygame.draw.rect(arg, "blue", (self.left + w * self.cell_size,
                                                       self.top + h * self.cell_size,
                                                       self.cell_size,
                                                       self.cell_size), 1)

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
            self.rect = self.rect
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


    # поле
    board_log = [[0] * 32 for _ in range(18)]
    board = Board(board_log)

    # группа, содержащая все спрайты
    collide_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    points = pygame.sprite.Group()
    character_group = pygame.sprite.Group()
    character = MainCharacter()
    character_group.add(character)

    # Всякое

    running = True
    while running:
        clock.tick(FPS)
        all_sprites.update()
        character_group.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    load_file = open("data/locations/lvl1.txt", "r")
                    board_log = decode(load_file)
                    board = Board(board_log)
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
        character_group.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
