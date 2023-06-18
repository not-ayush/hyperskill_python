import argparse
import socket

parser = argparse.ArgumentParser(description="suppa hackka")
parser.add_argument('ip',  help='ip address', type=str)
parser.add_argument('port',  help='port', type=int)
parser.add_argument('msg',  help='message to send', type=str)
args = parser.parse_args()

client = socket.socket()
client.connect((args.ip, args.port))
client.send(args.msg.encode())
print(client.recv(1024).decode())
client.close()