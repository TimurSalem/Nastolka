import socket
import pygame

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
main_socket.bind(('localhost', 8080))  # локальный сервер, порт
main_socket.setblocking(False)  # Отсутсвие ожидания комманд подключивсихся (сервер работает постоянно)
main_socket.listen(4)  # максимум сколько людей могут одновреиенно пытаться войти
print('Создался сокет')
players_sockets = []
clock = pygame.time.Clock()

FPS = 150

skins = {}
nicks = {}

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
			if data:
				skins[sock], nicks[sock] = data.split(', ')
			print('получил', data)
		except BlockingIOError:
			pass  # нечего считывать
		except ConnectionError:
			pass
	
	for sock in players_sockets:
		message_nicks = nicks.copy()
		print(nicks)
		try:
			print(list(message_nicks.keys())[0] == sock)
		except IndexError:
			pass
		# message_nicks.pop(sock)
		#
		# print(list(nicks.values()), list(message_nicks.values()))
		# print(sock, nicks.keys())
		try:
			skins_message = skins.pop(sock)
			nicks_message = nicks.pop(sock)
			print(nicks_message)
		except KeyError:
			pass
		message = f'{len(players_sockets), }'
		try:
			sock.send(str(message).encode())
		except BrokenPipeError:
			players_sockets.remove(sock)
			sock.close()
			print('отключился игрок')
		# невозможно отправить игроку (отключение и тд.)
		except BlockingIOError:
			players_sockets.remove(sock)
			sock.close()
			print('отключился игрок')
