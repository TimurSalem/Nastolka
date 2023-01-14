import pygame
import os
import sys

pygame.init()
pygame.display.set_caption('Механика')
size = width, height = 800, 400


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


player_image = load_image('tree.png')


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__(all_sprites)
        self.image = pygame.Surface((2 * 50, 2 * 50),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), radius)
        self.rect = pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)


class Player(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("tree.png")
        self.rect = self.image.get_rect()
        self.coords = [[(370, 160)], [(570, 150)], [(220, 55), (100, 55)]]
        self.tek = 0
        self.path_r = 0
        self.rect.x = width - 200
        self.rect.y = height - 100

    def update(self, *args):
        try:
            print(self.tek)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in all_sprites.sprites():
                    if i.rect.collidepoint(mouse_pos) and i != self.image:
                        c = (i.rect.x - 30, i.rect.y - 40)
                        self.rect.x, self.rect.y = c
                        j1 = 0
                        k1 = 0
                        for j in self.coords:
                            for k in j:
                                if k == c:
                                    self.path_r = k1 + 1
                                    self.tek = j1
                                    print(',,', self.path_r)
                                    break
                                k1 += 1
                            k1 = 0
                            print('    ', self.path_r)
                            j1 += 1
                        break
                print(self.tek, self.path_r)
            elif len(self.coords[self.tek]) >= 1 and self.tek != 0 and self.path_r != 0:
                self.rect.x, self.rect.y = self.coords[self.tek][self.path_r]
                self.path_r += 1
            elif self.tek == 0:
                self.rect.x, self.rect.y = self.coords[self.tek][self.path_r]
                self.tek += 1
        except IndexError:

            sys.exit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Механика')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    Player(all_sprites)
    all_sprites.draw(screen)

    running = True
    # (-1, -1)
    # (x, y, kx, ky)
    screen.fill((0, 0, 0))
    v = 100  # пикселей в секунду
    clock = pygame.time.Clock()
    draw = False
    coord = (0, 0)
    r = 10
    fps = 35
    move = False
    last_event = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                move = True
                last_event = event
                clock.tick(fps)
            if event.type == pygame.MOUSEBUTTONUP:
                move = False
            if event.type == pygame.KEYDOWN:
                move = True
                last_event = event
                clock.tick(fps)
            if event.type == pygame.KEYUP:
                move = False
        if move:
            all_sprites.update(last_event)
            clock.tick(fps)
        clock.tick(fps)
        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (255, 255, 255), [100, 0], [width - 100, height], 5)
        pygame.draw.line(screen, (255, 255, 255), [420, 220], [width, height - 200], 5)
        Ball(422, 220, 20)
        Ball(620, 210, 20)
        Ball(270, 115, 20)
        Ball(width - 150, height - 40, 20)
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()