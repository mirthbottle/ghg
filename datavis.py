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
