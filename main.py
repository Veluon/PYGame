import pygame
import random
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data_04', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def decode(file):
    result = []
    for i in file.readlines():
        pre_presult = []
        for j in i.strip():
            pre_presult.append(j)
        result.append(pre_presult)
    return result


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
                    pygame.draw.rect(arg, "white", (self.left + w * self.cell_size,
                                                    self.top + h * self.cell_size,
                                                    self.cell_size,
                                                    self.cell_size), 1)
                elif self.board[h][w] == "W":
                    pygame.draw.rect(arg, "yellow", (self.left + w * self.cell_size,
                                                     self.top + h * self.cell_size,
                                                     self.cell_size,
                                                     self.cell_size), 1)
                elif self.board[h][w] == "S":
                    pygame.draw.rect(arg, "blue", (self.left + w * self.cell_size,
                                                   self.top + h * self.cell_size,
                                                   self.cell_size,
                                                   self.cell_size), 1)


class MainCharacter(pygame.sprite.Sprite):
    image = None

    def __init__(self, *group, size=(500, 500)):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
        super().__init__(*group)
        # if MainCharacter.image is None:
        # MainCharacter.image = load_image("boom.png")
        # self.image = MainCharacter.image
        # width, height = size
        # self.rect = self.image.get_rect()
        # self.rect.x = random.randrange(width - self.image.get_rect().width)
        # self.rect.y = random.randrange(height - self.image.get_rect().height)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = self.image


def main():
    pygame.init()
    size = 1024, 576
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Game')

    # поле
    board_start = [[0] * 32 for _ in range(18)]
    board = Board(board_start)

    # группа, содержащая все спрайты
    all_sprites = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    load_file = open("data/locations/lvl1.txt", "r")
                    board = Board(decode(load_file))
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
        board.render(screen)
        pygame.display.flip()
        all_sprites.draw(screen)


if __name__ == '__main__':
    main()
