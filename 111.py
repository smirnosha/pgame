import os
import sys

import pygame

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
FPS = 200
clock = pygame.time.Clock()
x = 300
y = 500
x1 = 500
y1 = 200
t = True
t1 = True


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
    'demops': load_image('demops.jpg'),
}
player_image = load_image('mar.png', -1)
pt_image = load_image('pt.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            walls_group.add(self)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move_up(self):
        self.rect = self.rect.move(0, -50)

    def move_down(self):
        self.rect = self.rect.move(0, 50)

    def move_left(self):
        self.rect = self.rect.move(-50, 0)

    def move_right(self):
        self.rect = self.rect.move(50, 0)


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
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '-':
                Tile('empty', x, y)
                flower = Flower(x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)

    return new_player, x, y, flower


class Car(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('pt.png', -1)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.flip(self.image, True, False)
        self.t = True
        self.rect.y = 300
        self.rect.x = 500

    def update(self):
        if self.t:
            self.rect.y += 1
        else:
            self.rect.y -= 1
        if self.rect.y >= 450:
            self.t = False
        if self.rect.y <= 0:
            self.t = True


class Car2(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('pt.png', -1)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.flip(self.image, True, False)
        self.t1 = True
        self.rect.y = 500
        self.rect.x = 200

    def update(self):
        if self.t1:
            self.rect.y += 1
        else:
            self.rect.y -= 10
        if self.rect.y >= 450:
            self.t1 = False
        if self.rect.y <= 0:
            self.t1 = True


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


class Flower(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('demops.jpg')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)
        self.add(flower_group, all_sprites)


flower_group = pygame.sprite.Group()


def level_1():
    player, level_x, level_y, flower = generate_level(load_level('mappp'))
    start_screen()
    running = True
    group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    camera = Camera()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move_right()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move_left()

            if event.type == pygame.QUIT:
                terminate()

        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in group:
            camera.apply(sprite)

        if not pygame.sprite.collide_rect(player, flower):
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            flower_group.draw(screen)
            walls_group.update()
        else:
            all_sprites.empty()
            player_group.empty()
            tiles_group.empty()
            flower_group.empty()
            return
    camera = Camera()
    group = pygame.sprite.Group()
    Car2(group)
    Car(group)

    pygame.display.flip()
    clock.tick(fps)


def level_2():
    player, level_x, level_y, flower = generate_level(load_level('mapp'))
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()

            if event.type == pygame.QUIT:
                terminate()
            if not pygame.sprite.collide_rect(player, flower):
                screen.fill(pygame.Color(0, 0, 0))
                tiles_group.draw(screen)
                player_group.draw(screen)
                flower_group.draw(screen)
                walls_group.update()
            else:
                all_sprites.empty()
                player_group.empty()
                tiles_group.empty()
                flower_group.empty()
                return
        camera = Camera()
        group = pygame.sprite.Group()
        Car2(group)
        Car(group)
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in group:
            camera.apply(sprite)
            pygame.display.flip()
            clock.tick(fps)


def level_3():
    player, level_x, level_y, flower = generate_level(load_level('mappp'))
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()

            if event.type == pygame.QUIT:
                terminate()
            if not pygame.sprite.collide_rect(player, flower):
                screen.fill(pygame.Color(0, 0, 0))
                tiles_group.draw(screen)
                player_group.draw(screen)
                flower_group.draw(screen)
                walls_group.update()
            else:
                all_sprites.empty()
                player_group.empty()
                tiles_group.empty()
                flower_group.empty()
                return
        camera = Camera()
        group = pygame.sprite.Group()
        Car2(group)
        Car(group)
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in group:
            camera.apply(sprite)
            pygame.display.flip()
            clock.tick(fps)


def level_4():
    player, level_x, level_y, flower = generate_level(load_level('data/mapppp'))

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.move_up()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player.move_down()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()

            if event.type == pygame.QUIT:
                terminate()
            tiles_group.draw(screen)
            player_group.draw(screen)
            flower_group.draw(screen)
        camera = Camera()
        group = pygame.sprite.Group()
        Car2(group)
        Car(group)
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in group:
            camera.apply(sprite)
        pygame.display.flip()
        clock.tick(fps)


fps = 100
level_1()
level_2()
level_3()
level_4()

terminate()
