import socket
import threading
import datetime

nickname = input("Choose a nickname: ")
password = input("Pass: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

def recieve():
	while True:
		try:
			message = client.recv(1024).decode('utf-8')
			if message == 'NICK':
				client.send(nickname.encode('utf-8'))
			else:
				#for i in range(len(nickname+1)):
				index = len(nickname) + 2
				message = message[index:]
				#print(message)
				enc_nick = ""
				for i in range(len(nickname)):
					enc_nick += message[i]
				#print("enc ",enc_nick)
				norm_nick = decrypt(enc_nick)
				#print("dec ",norm_nick)
				if nickname == enc_nick:
					print(nickname, ":", decrypt(message))
		except Exception as e:
			print('An error occurred: ', e)
			client.close()
			break


def crypt(message):
	password_big = ""
	enc = ""
	temp = True
	while len(password_big) < len(message):
		if temp == True:
			password_big += password
			temp = False
		if temp == False:
			password_big += password[::-1]
			temp = True
	for i in range(len(message)):
		enc += chr(ord(message[i]) - len(password))

	return enc

def decrypt(message):
	password_big = ""
	dec = ""
	temp = True
	while len(password_big) < len(message):
		if temp == True:
			password_big += password
			temp = False
		if temp == False:
			password_big += password[::-1]
			temp = True

	for i in range(len(message)):
		dec += chr(ord(message[i]) + len(password))

	return dec

def write():
	while True:
		message = f"{nickname}: {crypt(input(''))}"
		client.send(message.encode('utf-8'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
