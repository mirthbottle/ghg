import pandas as pd
import numpy as np

# 2014 - sheet 12, col14 
# 2013 - sheet 10, col14
# 2012 - sheet 10, col12
# 2011 - sheet 9, col12
# 2010 - sheet 23, col12

goalcols = { 2014: 14, 2013: 14, 2012: 12, 2011: 12, 2010: 12 }

def get_targets(p, year):
    # years 2010 and 2011 and 2012 don't have ISIN, boooo
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

def get_companies_by_target(p):
    # get by levels[0] should be ISIN
    companies = p.index.levels[0].tolist()
    pieces_targets = []
    pieces_none = []
    for c in companies:
        try:
            f = p.loc[c]
            fhas_target = f[f["has target"]]
            f["ISIN"] = c
            yearswithtarget = fhas_target.index.tolist()
            if len(yearswithtarget) > 2:
                pieces_targets.append(f)
            else:
                pieces_none.append(f)
        except Exception:
            print c
            pass
    ptargets = pd.concat(pieces_targets).reset_index().set_index(["ISIN", "year"])
    pnotargets = pd.concat(pieces_none).reset_index().set_index(["ISIN", "year"])
    return ptargets, pnotargets

def get_hadtarget(targetorgs, target_col):
    # shift had target
    to_gs = targetorgs.groupby(level=0)
    companies = to_gs.indices.keys()
    pieces = []
    for c in companies:
        g = to_gs.get_group(c)
        g_series = np.array(g[target_col].tolist())
        g_series = g_series[:-1]
        g = g[1:]
        g[target_col + 'last year'] = g_series
        pieces.append(g)
    new_to = pd.concat(pieces).reset_index().set_index("ISIN")
    return new_to
