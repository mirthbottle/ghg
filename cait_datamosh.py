'''
For the CAIT historical data
'''
import pandas as pd
import traceback

total_col = "Total GHG Emissions Excluding Land-Use Change and Forestry (MtCO2e)"

sector_names = {
    "Energy (MtCO2e)":"energy", "Industrial Processes (MtCO2e)": "industrial processes", "Agriculture (MtCO2e)": "agriculture", 
    "Waste (MtCO2e)": 'waste'}

e_subsectors = {
    "Electricity/Heat (MtCO2)": "electricity", "Manufacturing/Construction (MtCO2)": "manufacturing", 
    "Transportation (MtCO2)": "transportation", "Other Fuel Combustion (MtCO2e)": "other fuels", 
    "Fugitive Emissions (MtCO2e)": "fugitive"}

def format_sectors(g):
    country = g["country"].values[0]
    print(country)
    record = {}
    if country not in ["World", "European Union (27)"]:
        try:
            total = g[total_col].values[0]
            sonly = g["Emissions by Sector"][list(sector_names)].to_frame(name="size").reset_index()
            sonly.loc[:, "name"] = sonly["Year"].apply(lambda s: sector_names.get(s, s))
            sonly.loc[:, "size"] = sonly["size"].apply(lambda s: round(s,2))

            if abs(sonly["size"].sum() - total) > 1:
                print("total not equal to sector total")
                print("total: {total} sum: {sum}".format(total=total, sum=sonly["size"].sum()))
                print(sonly)
            else:
                print(sonly["size"].sum())

            esubsectors = g["Energy Emissions by Sub-Sector"][
                list(e_subsectors)].to_frame(name="size").reset_index()
            esubsectors.loc[:, "name"] = esubsectors["Year"].apply(lambda s: e_subsectors.get(s, s))
            esubsectors.loc[:, "size"] = esubsectors["size"].apply(lambda s: round(s, 2))

            record = {"name": country, "size": round(total, 2), "children": []}
            srecords = list(sonly[["name", "size"]].T.to_dict().values())
            if len(esubsectors)>0:
                set_subsectors = False
                erecords = list(esubsectors[["name", "size"]].T.to_dict().values())
                for s in srecords:
                    if s["name"] == "energy":
                        
                        if abs(s["size"] - esubsectors["size"].sum()) > 1:
                            print("energy not equal to subsector total")
                            print("energy: {total} subsectors: {sum}".format(total=s["size"], sum=esubsectors["size"].sum()))
                            print(esubsectors)
                        else:
                            print(esubsectors["size"].sum())
                        set_subsectors = True
                        s["children"] = erecords
                if not set_subsectors:
                    etotal = esubsectors["size"].sum()
                    srecords.append({"name": "energy", "size": round(etotal,2), "children": erecords})
            record["children"] = srecords
        except Exception as e:
            record = {"error": e}
    return record

def other_record(world_g, top9ghg):
    record = {}
    try:
               
        total = world_g[total_col].values[0]
        ototal = total - top9ghg[total_col].sum()

        sonly = world_g["Emissions by Sector"][list(sector_names)].T
        sonly.columns = ["size"]
        sonly = sonly.reset_index()
        sonly.loc[:, "name"] = sonly["Year"].apply(lambda s: sector_names.get(s, s))
    
        sonly.loc[:, "size"] = sonly.apply(
            lambda r: r["size"] - top9ghg["Emissions by Sector"][r["Year"]].sum(), axis=1)
        sonly.loc[:, "size"] = sonly["size"].apply(lambda s: round(s, 2))
        
        esubsectors = world_g["Energy Emissions by Sub-Sector"][list(e_subsectors)].T
        esubsectors.columns = ["size"]
        esubsectors = esubsectors.reset_index()
        esubsectors.loc[:, "name"] = esubsectors["Year"].apply(lambda s: e_subsectors.get(s, s))
        esubsectors.loc[:, "size"] = esubsectors.apply(
            lambda r: r["size"] - top9ghg["Energy Emissions by Sub-Sector"][r["Year"]].sum(), axis=1)
        
        esubsectors.loc[:, "size"] = esubsectors["size"].apply(lambda s: round(s, 2))
        
        record = {"name": "Other", "size": round(ototal,2), "children": []}
        srecords = list(sonly[["name", "size"]].T.to_dict().values())
        if len(esubsectors)>0:
            set_subsectors = False
            erecords = list(esubsectors[["name", "size"]].T.to_dict().values())
            for s in srecords:
                if s["name"] == "energy":
                    set_subsectors = True
                    s["children"] = erecords
            if not set_subsectors:
                etotal = esubsectors["size"].sum()
                srecords.append({"name": "energy", "size": round(etotal,2), "children": erecords})
        record["children"] = srecords
    except Exception as e:
        traceback.print_exc()
        record = {"error": e}
    return record