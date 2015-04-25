import pandas as pd

# CPI's for a given year, take the CPI of jan the next year
USDcpi = {2014: 233.707, 2013: 233.916, 2012: 230.280, 2011: 226.665, 2010: 220.223, 2009: 216.687, 2008:211.143}

def adjust_inflation2014(s, colname):
    s[colname] = s.apply(lambda row: float(row[colname])*USDcpi[2014]/USDcpi[row["year"]], axis =1)
    return s

FINCOLS = ["Revenues", "COGS", "Equity", "PPE", "Assets", "Income"]

def adjust_inflation_all(s):
    for fc in FINCOLS:
        s = adjust_inflation2014(s, fc)
    return s


def compute_finvars(s):
    s["pCOGS"] = s["COGS"]/s["Revenues"]
    s["pPPE"] = s["PPE"]/s["Assets"]
    s["ROE"] = s["Income"]/s["Equity"]
    return s
