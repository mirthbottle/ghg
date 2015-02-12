import pandas as pd
import json

# CDPdata

def write_json(p, filename):
    index1s = p.index.levels[0]
    index2s = p.index.levels[1]
    data = {}
    data["name"] = p.columns[0]
    data["children"] = []
    for i1 in index1s:
        group = p.loc[i1]
        itotal = round(group.sum().values[0], 3)
        child1 = {"name": str(i1), "size": itotal, "children": []}
        # there must be children
        index2s = p.loc[i1].index
        for i2 in index2s:
            s = round(group.loc[i2].values[0], 3)
            child2 = {"name": str(i2), "size": s}
            child1["children"].append(child2)
        data["children"].append(child1)
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()
    return data


# YR 2014 sheet 35 has scope 1 and scope 2 emissions totals per company
# levels of verification, uncertainty, are available
# YR 2013 sheet 34, pcols[17] is scope1 and pcols[18] is scope2

def get_scope1or2(parsedsheet, scope):
    pcols = parsedsheet.columns.values
    if (scope == 1):
        pscope = pcols[17]
    elif (scope == 2):
        pscope = pcols[18]
    p = parsedsheet[[pcols[0]]+pcols[2:7].tolist()+pcols[14:17].tolist() +[pscope]]
    p = p.rename(columns={pcols[17]:"Scope 1", pcols[18]:"Scope 2"})
    p = p.set_index(pcols[0])
    return p

## totals by country headquarters...
## and GICS Sector or GICS Industry Group

def get_totals(pscope1or2, index1, index2, n):
    top = toplist(pscope1or2, index1, n)
    ptop = pscope1or2[pscope1or2[index1].isin(top)]
    toptotals = ptop.groupby([index1,index2]).sum()/1000000
    pother = pscope1or2[~pscope1or2[index1].isin(top)]
    pother[index1] = "Other"
    ototals = pother.groupby([index1,index2]).sum()/1000000
    totals = pd.concat([toptotals, ototals])
    return totals

# identify top20
def toplist(p, index1, n):
    # assume last column is what should be totaled
    pcols = p.columns.values
    scope = pcols[len(pcols)-1]
    # eg. index1 = "Country"
    ptotals = p.groupby(index1).sum()
    topn = ptotals.sort(scope, ascending = 0)[0:n].index
    return topn

# sheet 43 has scope 1 breakdown by country per company
# sheet 50 has scope 2 breakdown by country per company

def get_scope1or2country(parsedsheet):
    pcols = parsedsheet.columns.values
    p = parsedsheet[pcols[0:7].tolist()+pcols[16:18].tolist()]
    return p

# YR 2014 sheet 68 has scope3 emissions by category per company
# col14 has category, col16 has total
# YR 2013 sheet 65 has scope3 emissions, col14 and col16 have category and total

# i think i need to put the categories in separate columns...  
def get_scope3(parsedsheet):
    pcols = parsedsheet.columns.values
    p = parsedsheet[pcols[0:7].tolist()+[pcols[14], pcols[16]]]
    # delete all rows with col16 == NaN
    p = p[p[pcols[16]].notnull()]
    p = p.set_index(pcols[0])
    return p

def combine_scopes(pscope1, pscope2, pscope3):
    pcols = pscope3.columns.values
    # drop duplicates by account number
    has_scope1 = pscope1.drop_duplicates(pcols[1])
    has_scope2 = pscope2.drop_duplicates(pcols[1])
    has_scope3 = pscope3.drop_duplicates(pcols[1])
    has_scope1['has Scope 1']  = True
    has_scope2['has Scope 2']  = True
    has_scope3['has Scope 3']  = True
    p = has_scope1
    p = p.join(has_scope2[['has Scope 2']], how="outer")
    p = p.join(has_scope3[['has Scope 3']], how="outer")
    p['has Scope 1'] = p['has Scope 1'].fillna(False)
    p['has Scope 2'] = p['has Scope 2'].fillna(False)
    p['has Scope 3'] = p['has Scope 3'].fillna(False)
    p = p.drop(['Scope 1', 'Scope 2'], 1)
    return p

