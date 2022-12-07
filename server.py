import socket
import logging
from threading import *

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler("server.log"),
                logging.StreamHandler(),
            ],
        )
with open('settings.txt') as f:
    for line in f:
        HOST = line.split(';')[0]
        PORT = int(line.split(';')[1])
        max_size = int(line.split(';')[2])
with open('error.png', 'rb') as file:
    x = file.read()
    y = len(x)

sock = socket.socket()
with open('temp/index.html') as file:
    htm1 = file.read()
error404header = 'HTTP/1.1 404 Not Found'
error403header = 'HTTP/1.1 403 Forbidden Error'
picture_resp = f"""HTTP/1.1 404 Not Found
Server: SelfMadeServer v0.0.1
Content-type: image/png
Content-Length: {y}
Connection: close
""".encode()
try:
    sock.bind((HOST, PORT))
    print("Using port ", PORT)
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

def new_client(conn, addr):
    print("Connected", addr)

    data = conn.recv(max_size)
    msg = data.decode()

    try:
        msg1 = msg.split(" ")[1]
        msg = msg1.split('.')
    except:
        pass

    if len(msg) == 1 or msg[1] == 'html' or msg[1] == 'js' or msg[1] == 'css':
        response(msg,msg1)
    else:
        resp = (f"""{error403header}
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close
""" + error403header).encode()
        logging.error(f'{addr[1]}, {msg1[1:]} raised Error 403 ')
        conn.send(resp)
    conn.close()

def response(msg,msg1):
    try:
#         if msg1 == '/index.html':
#             with open('temp/' + msg1[1:]) as file:
#                 htm = file.read()
#             resp = f"""HTTP/1.1 200 OK
# Server: SelfMadeServer v0.0.1
# Content-type: image/png
# Content-Length: {y}
# Connection: close
#
# """.encode() + x
        with open('temp/' + msg1[1:]) as file:
            htm = file.read()
        resp = ("""HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close
"""+htm).encode()
#         print('msg', msg)
#         print('msg1', msg1)
    except:
        resp = resp = f"""{error404header}
Server: SelfMadeServer v0.0.1
Content-type: image/png
Content-Length: {y}
Connection: close
""".encode() + x

        logging.error(f"{addr[1]}, {msg1[1:]} raised Error 404 ")
    finally:
        if msg1[1:] == "":
            resp = ("""HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close
"""+htm1).encode()

    print(msg)
    conn.send(resp)
    conn.close()


while True:
	conn, addr = sock.accept()
	Thread(target=new_client, args=(conn, addr)).start()

conn.close()
