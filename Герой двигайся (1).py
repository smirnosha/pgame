import pygame
import os
import sys


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


class Cursor(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('5.jpg')
        self.rect = self.image.get_rect()

    def update(self):
        sp = pygame.key.get_pressed()
        if sp[pygame.K_LEFT] == 1:
            self.rect.x -= 1
        if sp[pygame.K_RIGHT] == 1:
            self.rect.x += 1
        if sp[pygame.K_UP] == 1:
            self.rect.y -= 1
        if sp[pygame.K_DOWN] == 1:
            self.rect.y += 1


pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)
group = pygame.sprite.Group()
Cursor(group)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            group.update()
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    group.update()
    group.draw(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(128)
pygame.quit()
