import os
import socket
import sys
from random import randint, choice

import time

import pygame
import sqlite3


def load_sprite(path, coord=(0, 0), prefix='sprites'):
	sprite = pygame.sprite.Sprite()
	sprite.image = pygame.image.load(f'{prefix}/{path}').convert_alpha()
	
	sprite.rect = sprite.image.get_rect()
	
	sprite.rect.x = coord[0]
	sprite.rect.y = coord[1]
	
	return sprite


def entry_to_lobby():
	"""
	метод входа в лобби
	"""
	global home_screen_flag, enter_name_flag
	home_screen_flag = False
	enter_name_flag = True


def exit():
	"""
	выход из игры
	"""
	pygame.quit()


def show_questions():
	questions_dict = {load_sprite('general_sprite.png', coord=(640, 540)): 'general',
					  load_sprite('geography_sprite.png', coord=(640, 540)): 'geography',
					  load_sprite('astronomy_sprite.png', coord=(640, 540)): 'astronomy'}
	
	con = sqlite3.connect('questions.db')
	
	# Создание курсора
	cur = con.cursor()
	
	questions_imported = cur.execute("""
	SELECT * FROM general
	""").fetchall()
	
	question_dict = {}
	
	for q in questions_imported:
		question_dict[q[0]] = eval(q[1])
		print(question_dict)
	
	question = choice(list(question_dict.keys()))
	answers = question_dict[question]
	
	for i in range(3):
		questions_sprites.add(questions_dict[list(question_dict.keys())[i]])
	
	con.commit()
	con.close()


class Button:
	def __init__(self, path, pinched_path, sprite_group: pygame.sprite.Group, func=None, buttons_actions: tuple = (),
				 coord=(0, 0), clamp=0):
		self.buttons_actions = buttons_actions
		self.sprite = load_sprite(path, coord)
		sprite_group.add(self.sprite)
		
		self.func = func
		
		self.pinched_path = pinched_path
		self.path = path
		
		self.coord = coord
		self.sprite_group = sprite_group
		
		self.induced = False
		self.pressed = False
		
		self.flag = False
	
	def check(self):
		"""
		метод проверки кнопок
		"""
		mouse_pos = pygame.mouse.get_pos()
		mouse_buttons = pygame.mouse.get_pressed()
		
		if self.sprite.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
			self.flag = True
		
		if self.sprite.rect.collidepoint(mouse_pos) and not mouse_buttons[0] and self.flag:
			self.flag = False
			self.sprite = load_sprite(self.pinched_path, self.coord)
			self.sprite_group.add(self.sprite)
			
			if self.func:
				self.func()
		else:
			self.sprite = load_sprite(self.path, self.coord)
			self.sprite_group.add(self.sprite)


'''подключение к серверу'''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
# sock.connect(('45.67.58.176', 8080))
sock.connect(('localhost', 8080))
'''.....................'''

pygame.init()
size = width, height = 1920, 1080

# screen = pygame.display.set_mode(size, pygame.FULLSCREEN, vsync=1)
screen = pygame.display.set_mode(size, vsync=1)

score = 0

# создание спрайтов

home_screen_sprites = pygame.sprite.Group()
home_screen_sprites.add(load_sprite('start_window.png'))

enter_name_screen_sprites = pygame.sprite.Group()
enter_name_screen_sprites.add(load_sprite('name_input_sprite.png', coord=(640, 540)))

lobby_screen_sprites = pygame.sprite.Group()

lobby_screen_sprites.add(load_sprite('carpet_blue.png', coord=(0, 0)))
lobby_screen_sprites.add(load_sprite('table.png', coord=(25, 0)))
lobby_screen_sprites.add(load_sprite('svitok_forest.png', coord=(400, 60)))
lobby_screen_sprites.add(load_sprite('campfire.png', coord=(600, 540)))

questions_sprites = pygame.sprite.Group()

# рендер текстов

pixel_font_48 = pygame.font.Font('assets/Pixel Times.ttf', 48)
pixel_font_56 = pygame.font.Font('assets/Pixel Times.ttf', 56)

enter_name_text = pixel_font_48.render('Введите Имя', True, (255, 255, 255))

skins = ['blue_knight.png', 'mage.png', 'shit_snowman.png']  # доступные скины
lobby_players_coords = [(460, 320), (460, 860), (900, 860), (900, 320)]

fir_rects = []

for _ in range(30):
	x, y = randint(400, 1200), randint(150, 1400)
	fir_sprite = load_sprite('fir.png', (x, y))
	
	# не допускания попаданий елок на костер и персонажей
	if not load_sprite('campfire.png', coord=(600, 540)).rect.colliderect(fir_sprite.rect) and all(
			[not fir_sprite.rect.colliderect(r) for r in fir_rects]) and all(
		[not fir_sprite.rect.collidepoint(lb[0], lb[1]) for lb in lobby_players_coords]):
		lobby_screen_sprites.add(fir_sprite)
		fir_rects.append(fir_sprite.rect)

home_screen_flag = True
lobby_screen_flag = False

running = True

name = ''

enter_name_flag = False

# создание кнопок
setting_button = Button('button_settings.png', 'button_settings_pressed.png', home_screen_sprites, coord=(260, 700))
play_button = Button('button_start.png', 'button_start_pressed.png', home_screen_sprites, func=entry_to_lobby,
					 coord=(750, 700))
exit_button = Button('button_exit.png', 'button_exit_pressed.png', func=exit, sprite_group=home_screen_sprites,
					 coord=(1240, 700))

ready_button = Button('button_ready.png', 'button_ready.png', sprite_group=lobby_screen_sprites,
					  coord=(1440, 880))

buttons = [setting_button, play_button, exit_button]

in_game = False
name_text_lobby = None

clock = pygame.time.Clock()  # Создать объект Clock (Требуется только один раз в коде!)

FPS = 60

skin_path = choice(skins)
skin = load_sprite(skin_path, coord=lobby_players_coords[0])
lobby_screen_sprites.add(skin)

nicks_text = []
nicks_coord = []

while running:
	start_time = time.time()  # start time of the loop
	
	'''Сообщение с сервером'''
	#  считываем команды
	
	# проверка на вход игрока в лобби
	if in_game:
		message = f'{skin_path}, {name};'
		sock.send(message.encode())
		
		data = sock.recv(1024)
		data = data.decode()
		try:
			data = list(map(lambda x: eval(x), data[1:-1].split(', ')))
			print(data)
			print(load_sprite('campfire.png', coord=(600, 540)))
			
			nicks = data[0]
			another_skins = data[1]
			# another_skins = pygame.sprite.Sprite(data[1])
			
			# отрисовка скинов других игроков в лобби
			for i in range(len(nicks)):
				print(nicks[i])
				another_nick = pixel_font_48.render(nicks[i], True, (40, 44, 60))
				nicks_text.append(another_nick)
				nicks_coord.append(name_text_lobby.get_rect(
					center=(lobby_players_coords[i + 1][0] + 150, lobby_players_coords[i + 1][1])))
				
				print(type(another_skins[i]))
				lobby_screen_sprites.add(load_sprite(another_skins[i], coord=lobby_players_coords[i + 1]))
		
		except ValueError:
			print('ex')
		# except RuntimeError:
		# 	print('run')
		except SyntaxError:
			pass
	
	'''.....................'''
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		#
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
		
		# проверка удаление никнейма и на ввод никнейма
		if enter_name_flag and event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				name = name[:-1]
			elif event.key == pygame.K_RETURN:
				enter_name_flag = False
				lobby_screen_flag = True
			else:
				name += event.unicode
				name_text_lobby = pixel_font_48.render(name, True, (40, 44, 60))
	
	# проверка нажатия кнопок
	for but in buttons:
		but.check()
	
	screen.fill((0, 0, 0))
	
	# отрисовка спрайтов начального меню
	if home_screen_flag:
		home_screen_sprites.draw(screen)
	
	# отрисовка спрайтов ввода текста
	if enter_name_flag:
		name_text = pixel_font_56.render(name, True, (40, 44, 60))
		
		enter_name_screen_sprites.draw(screen)
		screen.blit(enter_name_text, (800, 420))
		screen.blit(name_text, (660, 575))
	
	# отрисовка спрайтов лобби
	if lobby_screen_flag:
		in_game = True
		lobby_screen_sprites.draw(screen)
		place = name_text_lobby.get_rect(center=(lobby_players_coords[0][0] + 150, lobby_players_coords[0][1]))
		screen.blit(name_text_lobby, place)
		
		for i in range(len(nicks_text)):
			screen.blit(nicks_text[i], nicks_coord[i])
			print(nicks_coord[i], nicks_text[i])
	
	print("FPS: ", 1.0 / (time.time() - start_time))  # сколько фпс
	
	# clock.tick(FPS)
	
	pygame.display.flip()

pygame.quit()
