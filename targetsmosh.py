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

def get_hadtarget(targetorgs):
    # shift had target
    to_gs = targetorgs.groupby(level=0)
    companies = to_gs.indices.keys()
    pieces = []
    for c in companies:
        g = to_gs.get_group(c)
        g_tseries = np.array(g["has target"].tolist())
        g_aseries = np.array(g["has absolute"].tolist())
        g_iseries = np.array(g["has intensity"].tolist())
        g_tseries = g_tseries[:-1]
        g_aseries = g_aseries[:-1]
        g_iseries = g_iseries[:-1]
        g = g[1:]
        g['had target last year'] = g_tseries
        g['had absolute last year'] = g_aseries
        g['had intensity last year'] = g_iseries
        # g["ISIN"] = c
        pieces.append(g)
    new_to = pd.concat(pieces).reset_index().set_index("ISIN")
    return new_to

# targetorgs is the join of the table of targets,
# Scope 1 and 2 emissions, and orginfos
def get_targetorgs(to):
    to = to.reset_index().set_index("ISIN")
    to = to[['year','Country', 'GICS Sector',
             'GICS Industry Group', 'GICS Industry',
             'cogs', 'revt', 
             'has target', 'has absolute', 
             'has intensity',
             'Scope 1', 'Scope 2',
             '1and2 total', '1and2 intensity', 
             'percent change 1and2 intensity',
             'percent change 1and2 total']]
    return to

# target details
deets = { 2014: { 'abs info': 
                  { 'sheet': 13, 'scope': 15, 'target': 17,
                    'base year': 18, 'base ghg': 19,
                    'target year': 20},
                  'int info':
                  { 'sheet': 14, 'scope': 15, 'target': 17,
                    'metric': 18,
                    'base year': 19, 'base ghg int': 20,
                    'target year': 21},
                  'progress':
                  { 'sheet': 16, 'target id': 14},
                  'initiatives':
                  { 'sheet': 18, 'type': 14,
                    'monetary savings': 17, 'monetary cost': 18 }
              },
          2013: { 'abs info':
                  { 'sheet': 11, 'scope': 15, 'target': 17,
                    'base year': 18, 'base ghg': 19,
                    'target year': 20 },
                  'int info': 
                  { 'sheet': 12, 'scope': 15, 'target': 17,
                    'metric': 18,
                    'base year': 19, 'base ghg int': 20,
                    'target year': 21},
                  'progress': { 'sheet': 14 },
                  'initiatives': { 'sheet': 16, 'type': 14 }
              },
          2012: { 'abs info':
                  { 'sheet': 11, 'scope': 13, 'target': 15,
                    'base year': 16, 'base ghg': 17,
                    'target year': 18 },
                  'int info':
                  { 'sheet': 12, 'scope' 13, 'target': 15,
                    'metric': 16, 'base year': 17, 'base ghg int': 18,
                    'target year': 19 },
                  'progress': { 'sheet': 14 },
                  'initiatives': { 'sheet': 16, 'type': 12 }
              }
      }


# scopes need cleaning...
