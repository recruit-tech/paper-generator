# -*- coding: utf-8 -*-
import sys
import pandas as pd
import random


def create_company_name(num,names_file,types_file):
    company_name = []
    names = pd.read_csv(names_file, header=None )
    types = pd.read_csv(types_file, header=None )

    for i in range(0,num):
        corporation_type = random.choices(list(types[0]),k=1,weights=list(types[1]))[0]
        company_name_1 = random.choice(list(names[0]))
        company_name_2 = random.choice(list(names[0]))
        while company_name_1 == company_name_2 :
            company_name_2 = random.choice(list(names[0]))

        if random.randint(0,1):
            company_name.append( corporation_type + company_name_1 + company_name_2)
        else:
            company_name.append( company_name_1 + company_name_2 + corporation_type)

    return company_name 


if __name__ == '__main__':
    args = sys.argv
    num = int(args[1])
    names_file = args[2]
    types_file = args[3]
    company_name = create_company_name(num, names_file, types_file)
    for c in company_name:
        print(c)

