import pygame

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True
    x_pos = 0
    clock = pygame.time.Clock()
    v = 10
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():

            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            pygame.draw.circle(screen, (255, 0, 0), (20, 200), int(x_pos))
            x_pos += v * clock.tick() / 1000  # v * t в секундах



        # отрисовка и изменение свойств объектов
        # ...

        # обновление экрана
        pygame.display.flip()
    pygame.quit()
