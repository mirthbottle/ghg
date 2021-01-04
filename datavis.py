import numpy as np
from collections import OrderedDict
from bokeh.charts import Scatter

def prep_groups(g):
    pdict = OrderedDict()

    for i in g.groups.keys():
        labels = g.get_group(i).columns
        xname = labels[0]
        yname = labels[1]
        x = getattr(g.get_group(i), xname)
        y = getattr(g.get_group(i), yname)
        pdict[i] = zip(x, y)
    return pdict

def scatter_groups(xyvalues, fname, title, xlabel, ylabel):
    TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,previewsave"
    scatter = Scatter(xyvalues, filename=fname, title=title,
                      legend ="top_left", tools=TOOLS,
                      xlabel=xlabel, ylabel=ylabel) 
    return scatter


def prep_stacked_bar(df, cats):
    # show max 10 categories (out of colors)
    pdict = OrderedDict()
    i = 0
    for c in cats:
        if i < 10:
            pdict[c] = df[c].values.tolist() + [0.0, 0.0]
            df = df.drop(c, 1)
            i=i+1
        else:
            pdict["Other"] = df.sum(1).values.tolist() + [0.0, 0.0]
            break
    return pdict

def stacked_cols(df, categories):
    # where data for a category is in a separate column
    areas = OrderedDict()
    last = np.zeros(len(df[categories[0]]))
    for cat in categories:
        next = last + df[cat]
        areas[cat] = np.hstack((last[::-1], next))
        last = next
    return areas

def separate_cats(df, catcol, categories, valcol):
    # data for dategories are in one column
    # need to extract them into dataframe columns
    isnew = True
    newdf = 0
    for cat in categories:
        if isnew:
            newdf = df[df[catcol]==cat][[valcol]]
            isnew = False
        else:
            newdf = newdf.join(df[df[catcol]==cat][[valcol]], how="outer")
        newdf.rename(columns={valcol: cat}, inplace = True)
    return newdf

def prep_forhist(p, colname, low, high):
    prepped = p[(p[colname].isnull()==False) &
                (p[colname]<high) & (p[colname]>low)]
    return prepped

