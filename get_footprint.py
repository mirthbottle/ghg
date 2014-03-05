# scripts for manipulating the data tables from CDP
# 

# from numpy import genfromtxt
# for numbers
# g500 = genfromtxt('G500 Appendix update 2011.csv', delimiter=',') 

import csv



def get_g500_data():
    dict_reader = csv.DictReader(open('G500 Appendix update 2011.csv'))
    companies = []
    for row in dict_reader:
        keys = row.keys()
        clean_row = {}
        for key in keys:
            clean_row[key] = row[key].strip()
        companies.append(clean_row)
    return companies

# cs = get_g500_data()
def retrieve_record(cs, c_name):
    return (item for item in cs if item["Company"] == c_name).next()

def filter_by_sector(cs, sector):
    companies = []
    for item in cs:
        if item['Sector'] == sector:
            companies.append(item)
    return companies

def filter_has_all_scopes(cs):
    companies = []
    for item in cs:
        try:
            float(item['Scope 1'])
            float(item['Scope 2'])
            float(item['Scope 3'])
            companies.append(item)
        except ValueError:
            print 'not all scopes'
    return companies
            
