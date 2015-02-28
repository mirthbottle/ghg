import pandas as pd

# 2014 - sheet 12, col14 
# 2013 - sheet 10, col14
# 2012 - sheet 10, col12
# 2011 - sheet 9, col12
# 2010 - sheet 23, col12

goalcols = { 2014: 14, 2013: 14, 2012: 12, 2011: 12, 2010: 12 }

def get_targets(p, year):
    # years 2010 and 2011 don't have ISIN, boooo
    pcols = p.columns.values
    targets = p[p["Organisation"].notnull()][["Organisation",pcols[goalcols[year]]]]
    targets.rename(columns = {pcols[goalcols[year]]: "target type"}, inplace=True)
    targets["year"] = year
    targets["has absolute"] = targets["target type"].apply(lambda x: "solute" in unicode(x).encode('utf-8'))
    targets["has intensity"] = targets["target type"].apply(lambda x: "ntensity" in unicode(x).encode('utf-8'))
    return targets

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

