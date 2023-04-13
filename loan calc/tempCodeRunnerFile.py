import math
import argparse

'''
get the arguments
check if the arguments are correct
see what mode the user chose
call the appropriate function
'''
# t p i n a (order of arguments in list)
parser = argparse.ArgumentParser(description="loan calc")
parser.add_argument("--type", choices=["diff", "annuity"])
parser.add_argument("--principal", type=int)
parser.add_argument("--interest", type=float)
parser.add_argument("--periods", type=int, help="no of months")
parser.add_argument("--payment", type=float, help="annuity mode payment")
args = parser.parse_args()
args_ = dict()
for attr, value in vars(args).items():
    args_[attr] = value
    
#check args correct or not
if args_["type"] not in ["diff", "annuity"]: print("Incorrect parameters")
if args_["type"] == "diff" and args_["payment"] != None: print("Incorrect parameters")
count_args, neg_value = 0, False

for i in args_.values():
    print(i)