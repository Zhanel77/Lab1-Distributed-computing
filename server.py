import socket

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("RPC Server listening on port 5000...")

conn, addr = server.accept()
print("Connected by", addr)

data = conn.recv(1024)
print("Received:", data.decode())

response = "Hello from RPC Server"
conn.sendall(response.encode())

conn.close()
server.close()
