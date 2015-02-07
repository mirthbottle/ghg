import pandas as pd

def get_vcounts(parsedsheet):
    acol = 'CC3.1. Did you have an emissions reduction target that was active (ongoing or reached completion) in the reporting year?'
    return parsedsheet[acol].value_counts()

def summary(vcounts, parsedsheet):
    # stats about emissions targets in 2014
    # generate for every year
    
    hasintensity = vcounts['Intensity target'] + 350
    hasabs = vcounts['Absolute target'] + 350
    neg = len(parsedsheet) - vcounts.values.sum() + vcounts['No']
    return {"total":len(parsedsheet),
            "neg":neg,
            "intensity":hasintensity,
            "absolute":hasabs}
