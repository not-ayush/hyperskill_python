''' 
prompt user for principal, ask what they want to calc, no of months or monthly payment.
if monthly payment:
    ask no of months over which they want to pay
    check if payment comes float
    if float, use ceil to find monthly payment, and lastpayment using the formula:
    lastpayment = prncpl - (periods -1) * payment
    eg: 1000 prnicnispal,  9 months, find omnthyl payment
    1000 - 8 * 112 = 104
    in case lastpyament different from monthly payment display both
if months, 
    ask what monthly payment they want to do
    then just divide and round
exact format:
It will take 1 month to repay the loan
It will take 7 months to repay the loan

'''
import math
principal = int(input("Enter the loan principal: \n"))
mode = input('What do you want to calculate?\ntype \"m\" for number of months,\ntype "p" for the monthly payment:\n')

def m_period():
    mp_amount = int(input("Enter the monthly payment: \n"))
    period = int(math.ceil(principal / mp_amount))
    tense_edit = ["month","months"]
    if period == 1:
        print(f'It will take {period} {tense_edit[0]} to repay the loan')
    if period > 1:
        print(f'It will take {period} {tense_edit[1]} to repay the loan')

def m_payment():
    months = int(input("Enter the number of months: \n"))
    payment = int(math.ceil(principal / months))
    lastpayment = principal - (months - 1) * payment
    lastpayment_edit = ["", f"and the last payment = {lastpayment}."]
    message = f"Your monthly payment = {payment}"
    if payment != lastpayment:
        print(message, lastpayment_edit)
    else:
        print(message)

if mode == "m":
    m_period()
elif mode =="p":
    m_payment()
        

    