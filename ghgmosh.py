import pandas as pd
import json
import datetime as dt

# CDPdata

# starting 2012, GICS Sector Banks was renamed to Financials, ughh
# emissions in tons CO2e
# year 2010, 2011, and 2012 doesn't have isins, only organisation and ticker

# 2014 sheet 43 has Scope 1 data breakdown by country
# column 16 has country, 17 has tons

def write_json(p, filename):
    index1s = p.index.levels[0]
    index2s = p.index.levels[1]
    data = {}
    data["name"] = p.columns[0]
    data["children"] = []
    for i1 in index1s:
        group = p.loc[i1]
        itotal = round(group.sum().values[0], 3)
        child1 = {"name": i1.encode("ascii","ignore"), "size": itotal, "children": []}
        # there must be children
        index2s = p.loc[i1].index
        for i2 in index2s:
            s = round(group.loc[i2].values[0], 3)
            child2 = {"name": i2.encode("ascii","ignore"), "size": s}
            child1["children"].append(child2)
        data["children"].append(child1)
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()
    return data


# YR 2014 sheet 35
# levels of verification, uncertainty, are available
# YR 2013 sheet 33
# YR 2012 sheet 32
# YR 2011 sheet 30
# YR 2010 sheet 33 has scope 1, sheet 40 has scope 2
# YR 2009 sheet 2
scopecols = { 2014: {"sheet": 35, 1:17, 2:18, 3:{'cat':14, 'amount':16}},
              2013: {"sheet": 33, 1:17, 2:18, 3:{'cat':14, 'amount':16}},
              2012: {"sheet": 32, 1:15, 2:19, 3:{'cat':12, 'amount':13}},
              2011: {"sheet": 30, 1:15, 2:19, 3:{'cat':12, 'amount':13}},
              2010: {"sheets": {1: 33, 2: 40},
                     1:14, 2:14, 3:{'cat':12, 'amount':13}},
              2009: {"sheet": 2, 1:28, 2:44, 3:{'cat':12, 'amount':13}}}

def get_scope1or2(scope, year):
    if "sheet" in scopecols[year].keys():
        sheetnum = scopecols[year]["sheet"]
    else:
        sheetnum = scopecols[year]["sheets"][scope]
    filename = "../CDPdata/sheet"+ str(sheetnum) + "_" + str(year)+".pkl"
    parsedsheet = pd.read_pickle(filename)
    pcols = parsedsheet.columns.values
    pscope = pcols[scopecols[year][scope]]
    newname = "scope" + str(scope)
    p = parsedsheet[[pcols[0]]+pcols[2:7].tolist()+
                    ['Reporting Period\nFrom', 'Reporting Period\nTo']+
                    [pscope]]
    p = p.rename(columns={pscope:newname})
    # delete all rows with amount == NaN
    p = p[p[newname].notnull()]
    p = p.set_index(pcols[0])
    return p

def getscope_allyears(scope):
    pyrs={}
    for iyr in range(2010, 2015): 
        p = get_scope1or2(scope,iyr)
        p["reporting period to"] = pd.to_datetime(p['Reporting Period\nTo'])
        ptemp = {}
        for jyr in range(2009,2016):
            ptemp[jyr] = get_yrsdata(p, jyr)
            ptemp[jyr]["year"] = jyr
        pyrs[iyr] = pd.concat(ptemp.values())
    pall = pd.concat(pyrs.values())
    # delete duplicates
    pall = pall.reset_index().drop_duplicates(["Organisation","year"])
    pall = pall.set_index(['Organisation','year']).sort_index()
    return pall

def get_yrsdata(p, yr):
    ## use to column because the difference is always one year
    ## 2013, june 29 2013 to june 30 2014
    pyr = p[(p["reporting period to"] < dt.date(yr+1,6,30)) &
            (p["reporting period to"] > dt.date(yr, 6,29))]
    return pyr

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
# YR 2013 sheet 65 
# YR 2012 sheet 69
# YR 2011 sheet 67
# YR 2010 sheet 49
# YRs 2009 and older have different scope3 categories reported in separate columns
# mixed blessing...
# i use the organisation as the index, but they could differ by year
# maybe i should use account to index
# YRs 2009 and older don't have account numbers

# i think i need to put the categories in separate columns...  
def get_scope3(parsedsheet, year):
    pcols = parsedsheet.columns.values
    catcol = pcols[scopecols[year][3]["cat"]]
    amtcol = pcols[scopecols[year][3]["amount"]]
    p = parsedsheet[pcols[0:7].tolist()+[catcol, amtcol]]
    # delete all rows with amount == NaN
    p = p[p[amtcol].notnull()]
    p = p.set_index(pcols[0])
    return p


def drop_dups(p):
    name = p.index.name
    p[name] = p.index
    p = p.drop_duplicates(name)
    p = p.set_index(name)
    return p

def add_yearindex(p, year):
    p['year'] = year
    p.set_index('year', append=True, inplace=True)
    return p


def compute_percent_changes(p, colname):
    companies = p.index.levels[0].tolist()
    pieces = []
    for c in companies:
        try:
            f = p.loc[c]
            f = percent_change(f, colname)
            f["Organisation"] = c
            pieces.append(f)
        except Exception:
            print c
            pass
    newp = pd.concat(pieces).reset_index().set_index(["Organisation", "year"])
    return newp

# compute annual percent change...
def percent_change(f, colname):
    newcolname = "percent change " + colname
    f[newcolname] = 0
    yearswithdata = f.index.tolist()
    for i in range(2010, 2014):
        if i in yearswithdata and i-1 in yearswithdata:
            f.loc[i, newcolname] = f.loc[i,colname]/f.loc[i-1,colname] - 1
    return f

###### separate out companies with different emissions profiles

## # get companies that overall reduced emissions by 2014, and separate them into systemic vs large emissions reductions

## identify plateaus 
# yr 1 emissions reduction, <.5 std? or <5%  guess it depends what the std is
# yr 2, no reduction
# yr 3, no reduction
