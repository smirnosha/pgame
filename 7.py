import os
import sys

import pygame

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=-1):
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


class Landing(pygame.sprite.Sprite):
    image = load_image("pt.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(0, 1)


class Mountain(pygame.sprite.Sprite):
    image = load_image("mountains.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height


all_sprites = pygame.sprite.Group()
mountain = Mountain()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Landing(event.pos)
    screen.fill((160, 210, 255))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(200)
pygame.quit()
