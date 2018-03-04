import socket

# Секретный ключ
skey = 'qweqweqweq123456'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Напишите свой адрес и порт !!!!
server_address = ('192.168.1.38', 5555)

print('starting up on {} port {}'.format(*server_address))

sock.bind(server_address)
sock.listen(1)

print('Shutdown service started.')
print('Waiting for request.')

while True:
    connection, client_address = sock.accept()
    try:
        while True:
            data = connection.recv(16)
            if data:
                data = str(data, 'utf-8')
                if data == skey:
                    print('now shutdown...')
                    # ---------------------
                    # do shutdown here !!!
                    # Допишите чтоб выключалось!!!
                    # ---------------------
                elif data == '\r\n':
                    pass
                else:
                    print('wrong key. skipping...')
            else:
                break
    finally:
        connection.close()
