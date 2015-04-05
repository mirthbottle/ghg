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
