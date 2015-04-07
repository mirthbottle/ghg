import pandas as pd
import numpy as np

def getvars(p, colname):
    # p is the data for a given year
    p_s = p[colname]
    v = p_s.std()
    m = p_s.mean()
    p["t"+ colname] = (p_s - m)/ v
    return p

def getextremes(p, colname, threshold):
    # threshold in number of standard devs
    return p[abs(p[colname])> threshold]

def ols_everyear(p, model, filename):
    result={}
    for yr in range(2010,2014):
        result[yr] = smf.ols(formula=model, data=p.loc[yr]).fit()
        f = open("../CDPdata/" + filename + str(yr) + ".txt", 'w')
        f.write(model)
        f.write(result[yr].summary().as_text())
        f.close()
    return result
