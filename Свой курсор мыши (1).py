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
        self.image = load_image('1.png')
        self.rect = self.image.get_rect()

    def update(self, event):
        self.rect.x = event.pos[0]
        self.rect.y = event.pos[1]


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.mouse.set_visible(False)
    group = pygame.sprite.Group()
    clock = pygame.time.Clock()
    clock.tick(144)
    Cursor(group)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                group.update(event)
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        if pygame.mouse.get_focused():
            group.draw(screen)
        pygame.display.flip()
    pygame.quit()
