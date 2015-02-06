import pandas as pd

# CDPdata

def write_json(p, filename):
    
    return "well ill be"


# 2014 book
# sheet 35 has scope 1 and scope 2 emissions totals per company
# levels of verification, uncertainty, are available

def get_scope1or2(parsedsheet, scope):
    pcols = parsedsheet.columns.values
    if (scope == 1):
        pscope = pcols[17]
    elif (scope == 2):
        pscope = pcols[18]
    p = parsedsheet[[pcols[0]]+pcols[2:7].tolist()+pcols[14:17].tolist() +[pscope]]
    p = p.rename(columns={pcols[17]:"Scope 1", pcols[18]:"Scope 2"}).fillna(0)
    return p

## totals by country headquarters...
## and GICS Sector or GICS Industry Group

def get_totals(pscope1or2, index1, index2, n):
    top = toplist(pscope1or2, index1, n)
    ptop = pscope1or2[pscope1or2[index1].isin(top)]
    toptotals = ptop.groupby([index1,index2]).sum()
    pother = pscope1or2[~pscope1or2[index1].isin(top)]
    pother[index1] = "Other"
    ototals = pother.groupby([index1,index2]).sum()
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

# sheet 68 has scope3 emissions by category per company
# col14 has category, col16 has total

def get_scope3(parsedsheet):
    pcols = parsedsheet.columns.values
    p = parsedsheet[pcols[0:7].tolist()+pcols[14:17].tolist()]
    return p
