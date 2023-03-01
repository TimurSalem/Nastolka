import os
import sys
import random
import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame

pygame.init()
size = width, height = 900, 700
screen = pygame.display.set_mode(size)



def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
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
    else:
        image = image.convert_alpha()
    return image


class Mountain(pygame.sprite.Sprite):
    image = load_image("mage.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.w)
        self.rect.y = height - 300
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN:
            key = args[0]
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.rect.y -= 1
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.rect.y += 1
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.rect.x += 1
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.rect.x -= 1
        clock.tick(200)


class Landing(pygame.sprite.Sprite):
    imgs = [pygame.transform.scale(load_image("bliny.png"), (64, 64)),
            pygame.transform.scale(load_image("cake.png"), (52, 62))]
    image = imgs[random.randint(0, 100) % 2]


    def __init__(self, pos):
        super().__init__(all_sprites)
        imgs = [pygame.transform.scale(load_image("bliny.png"), (64, 64)),
                pygame.transform.scale(load_image("cake.png"), (52, 62))]
        image = imgs[random.randint(0, 100) % 2]
        self.image = image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        global count
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(0, 1)
        else:
            count += 1
            all_sprites.remove(self)


all_sprites = pygame.sprite.Group()
image = load_image("fon_night.png")
screen.blit(image, image.get_rect())
mountain = Mountain()
font = pygame.font.Font(None, 35)

def start_screen():
    FPS = 100
    intro_text = ["Правила игры",
                  "Поймайте за 30 секунд как можно больше еды",
                  "Перемещение влево - вправо стрелочками"]

    fon = pygame.transform.scale(load_image('fon_night.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

fps = 140
fps1 = 100
clock = pygame.time.Clock()

running = True
count = 0
move = False
pygame.time.set_timer(pygame.USEREVENT, 1000)
start = pygame.time.get_ticks()
start_screen()
while running:
    sec = (pygame.time.get_ticks() - start) / 1000
    for event in pygame.event.get():
        if sec > 30:
            running = False
            print(count)
            break
        if event.type == pygame.KEYDOWN:
            move = True
            last_event = event
        if event.type == pygame.KEYUP:
            move = False
        if event.type == pygame.USEREVENT:
            Landing((random.randint(0, 700), 0))
    text = font.render('Score:' + str(count), 1, pygame.Color('white'))
    screen.blit(text, (850, 670))
    all_sprites.update()
    screen.fill((0, 0, 0))
    if move:
        mountain.update(last_event)
    screen.blit(image, image.get_rect())
    text = font.render('Score: ' + str(count), 1, pygame.Color('white'))
    screen.blit(text, (750, 670))
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()