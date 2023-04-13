import math
import argparse
import sys

'''
get the arguments
check if the arguments are correct
see what mode the user chose
call the appropriate function
If you are getting the wrong overpayment value - make sure you are rounding the monthly values before adding them to the total you'll be subtracting from the principal.
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
count_args, neg_value = 0, False
for i in args_.values():
    if i != None: count_args += 1
    if ((type(i) == int) or (type(i) == float)) and (i < 0): neg_value = True
if args_["type"] not in ["diff", "annuity"]: 
    print("Incorrect parameters")
    sys.exit()
elif args_["type"] == "diff" and args_["payment"] != None: 
    print("Incorrect parameters")
    sys.exit()
elif count_args < 4: 
    print("Incorrect parameters")
    sys.exit() 
t, p, i, n, a = args_["type"],args_["principal"],args_["interest"] / (12 * 100) if args_["interest"] != None else None,args_["periods"],args_["payment"]


if t == "diff":
    payed = 0
    for m in range(1, n+1):
        # diff payment calc
        Dm = (p / n) + (i * (p - (p * (m - 1))/n))
        print(f"Month {m}: payment is {math.ceil(Dm)}")
        payed +=  math.ceil(Dm)
    print(f"Overpayment = {payed - p}")
elif t == "annuity":
    if not n:
        x = a / (a - i*p)
        n = math.ceil(math.log(x, 1 + i))
        # months to year month notation
        if n < 12: 
            print(f'It will take {n} {"month" if n == 1 else "months"} to repay this loan!') # month only notation
        elif n%12 == 0 : 
            print(f'It will take {round(n/12)} {"year" if int(n/12) == 1 else "years"} to repay this loan!') # year only notation
        else: 
            print(f'It will take {int(n//12)} {"year" if n//12 == 1 else "years"} and {int(n%12)} {"month" if n/12 == 1 else "months"} to repay this loan!')
    elif not a:
        a = math.ceil(p * ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))
        print(f"Your monthly payment = {str(a)}!")
        
    elif not p:
        p = a / ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1))
        print(f"Your loan principal = {int(p)}!")
        
    print(f"Overpayment = {round(a*n) - p}")
