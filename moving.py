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


class Player(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("tree.png")
        self.rect = self.image.get_rect()
        self.coords = [(370, 160), (570, 150),(220, 55)]
        self.tek = 0
        self.rect.x = width - 200
        self.rect.y = height - 100

    def update(self, *args):
        try:
            self.rect.x, self.rect.y = self.coords[self.tek]
            self.tek += 1
        except IndexError:
            if self.tek != len(self.coords):
                self.rect.x, self.rect.y = self.coords[0]
            else:
                sys.exit()

    def move(self, dx, dy):
        self.pos_x += dx
        self.pos_y += dy
        self.update()


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
    balls = []
    # (-1, -1)
    # (x, y, kx, ky)
    screen.fill((0, 0, 0))
    v = 100  # пикселей в секунду
    clock = pygame.time.Clock()
    draw = False
    coord = (0, 0)
    r = 10
    fps = 10
    move = False
    last_event = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                move = True
                last_event = event
                clock.tick(fps)
            if event.type == pygame.KEYUP:
                move = False
        if move:
            all_sprites.update(last_event)
        clock.tick(fps)
        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (255, 255, 255), [100, 0], [width - 100, height], 5)
        pygame.draw.line(screen, (255, 255, 255), [420, 220], [width, height - 200], 5)
        pygame.draw.circle(screen, (255, 255, 255), (422, 220), 20)
        pygame.draw.circle(screen, (255, 255, 255), (620, 210), 20)
        pygame.draw.circle(screen, (255, 255, 255), (270, 115), 20)
        pygame.draw.circle(screen, (255, 255, 255), (width - 150, height - 40), 20)
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()