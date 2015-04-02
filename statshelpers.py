import pandas as pd
import numpy as np

def getvars(p, colname):
    # p is the data for a given year
    p_s = p[colname]
    v = p_s.var
    p["var"+ colname] = v.im_self
    return p

def getextremes(p, colname):
    return p[abs(p[colname])>1.5]
