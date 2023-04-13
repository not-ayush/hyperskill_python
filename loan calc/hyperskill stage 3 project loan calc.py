import math
    
mode = input('''What do you want to calculate?
type "n" for number of monthly payments,
type "a" for annuity monthly payment amount,
type "p" for loan principal:''')

if mode == "n":
    p = float(input("Enter the loan principal:"))
    a = float(input("Enter the monthly payment:"))
    r = float(input("Enter the loan interest:")) / 100
    i = r/12
    x = a / (a - i*p)
    n = math.ceil(math.log(x, 1 + i))
    # months to year month notation
    if n < 12: 
        print(f'It will take {"month" if n == 1 else "months"} to repay this loan!') # month only notation
    elif n%12 == 0 : 
        print(f'It will take {n/12} {"year" if int(n/12) == 1 else "years"} to repay this loan!') # year only notation
    else: 
        print(f'It will take {int(n//12)} {"year" if n//12 == 1 else "years"} and {int(n%12)} {"month" if n/12 == 1 else "months"} to repay this loan!')

elif mode == "a":
    p = float(input("Enter the loan principal:"))
    n = float(input("Enter the number of periods:")) 
    i = float(input("Enter the loan interest:"))/(12*100)
    a = math.ceil(p * ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))
    print(f"Your monthly payment = {str(a)}!")
    
elif mode == "p":
    a = float(input("Enter the monthly payment:"))
    n = float(input("Enter the number of periods:")) 
    i = float(input("Enter the loan interest:")) / (100*12)
    p = a / ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1))
    print(f"Your loan principal = {int(p)}!")