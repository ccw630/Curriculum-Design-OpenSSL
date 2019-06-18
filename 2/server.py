import socket
import ssl
import time
sock = socket.socket()
sock.bind(("127.0.0.1", 4443))
print("Socket binded")
sock.listen(1)
def input_pro(connstream,data):
	print(time.asctime(time.localtime(time.time())), "[INFO] Server Received:", data.decode("utf-8") )
	return True
def doclient(connstream):
	data = connstream.recv(1024)
	while data:
		if not input_pro(connstream,data):
			break
		connstream.send(b'Server Received')
		data = connstream.recv(1024)
	return True
while True:
	try:
		conn,addr = sock.accept()
		connstream = ssl.wrap_socket(conn, "server.key", "server.crt", server_side=True)
		try:
			doclient(connstream)
		finally:
			connstream.close()
	except:
		break
