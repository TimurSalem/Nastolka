import socket
import pygame
from random import randint

# подключение к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('45.67.58.176', 8080))

pygame.init()
size = width, height = 1200, 600
screen = pygame.display.set_mode(size)

x, y = randint(0, width), randint(0, height)

x_speed, y_speed = 0, 0

x_speed_a, x_speed_d = 0, 0
y_speed_w, y_speed_s = 0, 0

speed = 5

message = ''
players_coords = []

while True:
	
	'''Сообщение с сервером'''
	#  считываем команды
	
	if f'{x}, {y}' != message:
		message = f'{x}, {y}'
		sock.send(message.encode())
	
	data = sock.recv(1024)
	data = data.decode()
	recv_coords = data
	
	try:
		players_coords = eval(recv_coords)
		print(type(players_coords))
	except SyntaxError:
		print(recv_coords)
	except TypeError:
		print(recv_coords)
	
	'''.....................'''
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == 769 and event.key == pygame.K_w:
			y_speed_w = 0
			y_speed = y_speed_s
		
		if event.type == 768 and event.key == pygame.K_w:
			y_speed_w = -speed
			y_speed = y_speed_w
		
		if event.type == 769 and event.key == pygame.K_d:
			x_speed_d = 0
			x_speed = x_speed_a
		
		if event.type == 768 and event.key == pygame.K_d:
			x_speed_d = speed
			x_speed = x_speed_d
		
		if event.type == 769 and event.key == pygame.K_s:
			y_speed_s = 0
			y_speed = y_speed_w
		
		if event.type == 768 and event.key == pygame.K_s:
			y_speed_s = speed
			y_speed = y_speed_s
		
		if event.type == 769 and event.key == pygame.K_a:
			x_speed_a = 0
			x_speed = x_speed_d
		
		if event.type == 768 and event.key == pygame.K_a:
			x_speed_a = -speed
			x_speed = x_speed_a
	
	x += x_speed
	y += y_speed
	
	print(players_coords)
	
	screen.fill((0, 0, 0))
	
	for pcd in players_coords:
		
		coords = tuple(list(map(int, pcd.split(', ')))[:2])
		
		pygame.draw.circle(surface=screen, color=(200, 150, 0), center=coords, radius=40)
	
	pygame.display.flip()

pygame.quit()
