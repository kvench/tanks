# импортируем библиотеку
import socket
import json
# создаем сокет
sock = socket.socket()
# выбираем ip по-умолчанию и порт 9090 (можно и другой)
sock.bind(('', 9090))
# максимальное количество ожидающих подключений
sock.listen(1)
# ждем, пока к нам кто то подключится
conn, addr = sock.accept()

# когда к нам кто-то подключился - печатаем его адрес
print('Connected: ', addr)

# ждем, пока что-нибудь придет от клиента, а затем забираем это из буфера (но не больше 1024 байт)
client_data = conn.recv(1024)
# превращаем байты в строку - декодируем utf-8
client_string = client_data.decode('utf-8')

print("Получили строку:", client_string)

words = client_string.split(' ')
for word in words[:]:
    if word [0]!='а' and word[0]!= 'А':
        words.remove(word)
print("Отправляем строку:", words)
s = json.dumps(words)
# отправляем ответ клиенту


conn.send(s.encode('utf-8'))

# в конце - закрываем соединение
conn.close()
