import sys
try:
    from tabulate import tabulate
except ImportError as e:
    sys.exit(f"This program requires tabulate, install it with \n pip install tabulate")

import argparse
"""
Students will create a python program to process and tablet a payroll report.
The input data will be the following:
Employee Name; Pay Rate; hours worked. For hours worked over 40 hour employees will earn time and a half. Fed Tax  10%, State tax 6%, FICA 3%

The Output should look the following:

Employee Name    Hours Worked    Pay Rate      Regular Pay    OT Pay    Gross Pay   Fed Tax   State Tax   FICA                Net Pay

XXXXXXXX                   NN                     NN.NN            NN.NN         NN.NN        NN.NN     NN.NN     NN.NN       NN.NN.           NN.NN
XXXXXXXX                   NN                     NN.NN            NN.NN         NN.NN        NN.NN     NN.NN     NN.NN       NN.NN.           NN.NN
XXXXXXXX                   NN                     NN.NN            NN.NN         NN.NN        NN.NN     NN.NN     NN.NN       NN.NN.           NN.NN
XXXXXXXX                   NN                     NN.NN            NN.NN         NN.NN        NN.NN     NN.NN     NN.NN       NN.NN.           NN.NN
XXXXXXXX                   NN                     NN.NN            NN.NN         NN.NN        NN.NN     NN.NN     NN.NN       NN.NN.           NN.NN
XXXXXXXX                   NN                     NN.NN            NN.NN         NN.NN        NN.NN     NN.NN     NN.NN       NN.NN.           NN.NN
XXXXXXXX                   NN                     NN.NN            NN.NN         NN.NN        NN.NN     NN.NN     NN.NN       NN.NN.           NN.NN
XXXXXXXX                   NN                     NN.NN            NN.NN         NN.NN        NN.NN     NN.NN     NN.NN       NN.NN.           NN.NN


The program should run and be able to process 10 employees before ending.

"""

__author__ = "Viktor Korbukh"
__version__ = "0.1.1"
__license__ = "MIT"



def fixed_width_print(data):

    header = ["Employee Name" ,   
        "Hours Worked",    
        "Pay Rate",      
        "Regular Pay",    
        "OT Pay",    
        "Gross Pay",   
        "Fed Tax", 
        "State Tax",
        "FICA",
        "Net Pay"]
    print(tabulate(data, headers=header, floatfmt=".2f"))

def enter_data(num_empl):
    raw_data = []
    num_entered_records =0

    while num_entered_records < num_empl:
        """ input ends after num_empl ( default=10) records 
            or after ;; was entered 
            any errors in input do not increase num_entered_records
            just a new prompt to enter data
        """
        #record = input("Enter employee Name; Hours worked; Pay Rate ")
        record = input(": ")
        
        try:
            name, hours, pay_rate = record.split(";")
        except: 
            continue
        
        if name == "":
            break
        
        try:
            hours, pay_rate = int(hours), float(pay_rate)
        except:
            continue
        
        num_entered_records += 1
        raw_data.append([name, hours, pay_rate])
        print()
    print()
    return raw_data

def input_data(limit,tax):

    num_empl = limit
    raw_data = enter_data(num_empl)

    data = process_input(raw_data,tax)
       
    return data

def pay_calc(hours, pay_rate,tax):
    """
    For hours worked over 40 hour employees will earn time and a half. 
    Fed Tax  10%, State tax 6%, FICA 3%
    """
    hours_per_week = 40
    ot_rate = 1.5
    
    fed_rate   = tax["federal"]/100
    state_rate = tax["state"]/100
    fica_rate  = tax["fica"]/100

    ot_hours = 0
    if hours > hours_per_week:
        ot_hours = hours -hours_per_week
        hours = hours_per_week
    
    reg_pay   = hours * pay_rate
    ot_pay    = ot_rate * ot_hours * pay_rate
    gross_pay = reg_pay + ot_pay
    fed_tax   = gross_pay * fed_rate
    state_tax = gross_pay * state_rate
    fica      = gross_pay * fica_rate
    net_pay   = gross_pay - (fed_tax + state_tax + fica)
    
    return [pay_rate,reg_pay,ot_pay,gross_pay,fed_tax,state_tax,fica,net_pay]

def process_input(raw_data,tax):
    data =[]
    
    for raw in raw_data:
        hours = int(raw[1])
        pay_rate = float(raw[2])
        data.append(raw[0:2] + pay_calc(hours, pay_rate,tax))
    return data

def main(args):
    tax = {"federal": args.federal, "state": args.state, "fica": args.fica}
    data=input_data(args.limit, tax)
    fixed_width_print(data)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="""
        program to process and tablet a payroll report.
        The input data will be the following:
        Employee Name; Pay Rate; hours worked
        """)
    parser.add_argument("-l", "--limit", type=int, default=10,
                    help="number of processed records is limited by this number")
    
    parser.add_argument( "-f","--federal", type=int, default=10,
                    help="Federal tax rate   default is 10")
    parser.add_argument( "-s","--state", type=int, default=6,
                    help="State tax rate   default is 6")
    parser.add_argument( "-i","--fica", type=int, default=3,
                    help="FICA tax rate   default is 3")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    

    args = parser.parse_args()
    
    main(args)
    
    
