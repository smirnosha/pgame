import os
import sys

import pygame

pygame.init()
size = width, height = 800, 400
screen = pygame.display.set_mode(size)
FPS = 200
clock = pygame.time.Clock()
x = 200
y = 100
t = True
YELLOW = (255, 255, 0)


class Fon(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('fon.jpg')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


start_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    Fon(start_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        start_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'demops': load_image('demops.jpg')
}
player_image = load_image('mar.png', -1)
pt_image = load_image('pt.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall' or tile_type == 'demops':
            walls_group.add(self)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.image1 = pt_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, event):
        if event.key == pygame.K_RIGHT:
            self.rect.x += 50
        if event.key == pygame.K_LEFT:
            self.rect.x -= 50
        if event.key == pygame.K_UP:
            self.rect.y -= 50
        if event.key == pygame.K_DOWN:
            self.rect.y += 50
        if pygame.sprite.spritecollideany(self, walls_group):
            if event.key == pygame.K_RIGHT:
                self.rect.x -= 50
            if event.key == pygame.K_LEFT:
                self.rect.x += 50
            if event.key == pygame.K_UP:
                self.rect.y += 50
            if event.key == pygame.K_DOWN:
                self.rect.y -= 50


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '-':
                Tile('demops', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Car(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('pt.png', -1)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self, y):
        self.rect.y = y
        self.rect.x = x


group = pygame.sprite.Group()
Car(group)

running = True

start_screen()
player, level_x, level_y = generate_level(load_level('mapp'))
camera = Camera()
running = True
x_pos = 100
v = 20  # пикселей в секунду
fps = 60
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player_group.update(event)

    if t:
        y += 100 * clock.tick() / 1000
    else:
        y -= 100 * clock.tick() / 1000
    if y >= 450:
        t = False
    if y <= 0:
        t = True
    group.update(y)
    screen.fill((0, 0, 0))
    group.draw(screen)
    pygame.display.flip()
    group.draw(screen)
    # изменяем ракурс камеры
    camera.update(player);
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()

    x_pos += v / fps
    clock.tick(fps)

terminate()
