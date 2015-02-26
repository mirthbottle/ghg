import pandas as pd

# 2014 - sheet 12, col14 
# 2013 - sheet 10, col14

goalcols = { 2014: 14, 2013: 14 }

def get_vcounts(p, year):
    pcols = p.columns.values
    return p[pcols[goalcols[2014]]].value_counts()

def summary(vcounts, p):
    # stats about emissions targets in 2014
    # generate for every year

    hasintensity = vcounts['Intensity target'] + 350
    hasabs = vcounts['Absolute target'] + 350
    neg = len(p) - vcounts.values.sum() + vcounts['No']
    return {"total":len(p),
            "neg":neg,
            "intensity":hasintensity,
            "absolute":hasabs}

