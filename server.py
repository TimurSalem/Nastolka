import socket
import pygame

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
main_socket.bind(('0.0.0.0', 8080))  # локальный сервер, порт
main_socket.setblocking(False)  # Отсутсвие ожидания комманд подключивсихся (сервер работает постоянно)
main_socket.listen(4)  # максимум сколько людей могут одновреиенно пытаться войти
print('Создался сокет')
players_sockets = []
clock = pygame.time.Clock()

FPS = 60

skins = {}
nicks = {}

message = ''

while True:
	clock.tick(FPS)
	# проверка на желающих подключится
	try:
		new_socket, addr = main_socket.accept()
		print(f'Подключился {addr}')
		new_socket.setblocking(False)
		players_sockets.append(new_socket)
	except BlockingIOError:
		pass  # Нет запросов
	
	for sock in players_sockets:
		try:
			data = sock.recv(1024)
			data = data.decode()
			data = data.split(';')[0]
			print(data)

			skins[sock], nicks[sock] = data.split(', ')
		except BlockingIOError:
			print('ex')
		except ConnectionError:
			print('ex')
		except ValueError:
			players_sockets.remove(sock)

			print('отключился игрок')
		
	print(nicks)
	
	for sock in players_sockets:
		try:
			nicks_copy = nicks.copy()
			nicks_copy.pop(sock)
			
			nicks_list = list(nicks_copy.values())
			
			skins_copy = skins.copy()
			skins_copy.pop(sock)
			
			skins_list = list(skins_copy.values())
			
			message = f'{nicks_list, skins_list}'
		except KeyError:
			pass
			
		try:
			sock.send(str(message).encode())
		except BrokenPipeError:
			try:
				players_sockets.remove(sock)
				nicks.pop(sock)
				skins.pop(sock)
				
				sock.close()
			except KeyError:
				pass
			print('отключился игрок')
		# невозможно отправить игроку (отключение и тд.)
		except BlockingIOError:
			try:
				players_sockets.remove(sock)
				nicks.pop(sock)
				skins.pop(sock)
				
				sock.close()
			except KeyError:
				pass
			print('отключился игрок')
		except ConnectionResetError:
			try:
				players_sockets.remove(sock)
				nicks.pop(sock)
				skins.pop(sock)
				
				sock.close()
			except KeyError:
				pass
			print('отключился игрок')
