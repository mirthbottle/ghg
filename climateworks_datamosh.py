import pandas as pd
import requests
import traceback

def get_cw_data(payload):
    r = requests.get("https://www.climatewatchdata.org/api/v1/data/historical_emissions", params=payload)
    last_page = round(int(r.headers["Total"])/50)+1

    print(last_page)

    dts = []
    error_pages = []
    for i in range(last_page):
        payload["page"] = i+1
        try:
            r = requests.get("https://www.climatewatchdata.org/api/v1/data/historical_emissions", params=payload)
            rdata = r.json()
            datatable = pd.DataFrame(rdata["data"])
            dts.append(datatable)
        except:
            error_pages.append(i+1)
    datatable = pd.concat(dts)

    datatable.loc[:, "size"] = datatable["emissions"].apply(lambda em: em[0]["value"])
    return datatable, error_pages
    
sector_names = {
    "Energy":"energy", "Industrial Processes": "industrial processes", "Agriculture": "agriculture", 
    "Waste": 'waste'}

e_subsectors = {
    "Electricity/Heat": "electricity", "Building": "building", "Manufacturing/Construction": "manufacturing", 
    "Transportation": "transportation", "Other Fuel Combustion": "other fuels", 
    "Fugitive Emissions": "fugitive"}

def format_sectors(g):
    country = g["country"].values[0]
    print(country)
    record = {}
    if country not in ["World", "European Union (27)"]:
        names_map = {**sector_names, **e_subsectors}
        try:
            g.loc[:, "name"] = g["sector"].apply(lambda s: names_map.get(s, s))
            g.loc[:, "size"] = g["size"].apply(lambda s: round(s, 2))
            total = g.loc[g["name"] == "Total excluding LUCF", "size"].values[0]
            # g.loc[:, "size"] = g["size"].apply(round)
            sonly = g.loc[g["name"].isin(list(sector_names.values())), ["name", "size"]].copy()
            if abs(sonly["size"].sum() - total) > 1:
                print("total not equal to sector total")
                print("total: {total} sum: {sum}".format(total=total, sum=sonly["size"].sum()))
                print(sonly)
            else:
                print(sonly["size"].sum())
            esubsectors = g.loc[g["name"].isin(list(e_subsectors.values())), ["name", "size"]].copy()
            
            record = {"name": country, "size": total, "children": []}
            srecords = list(sonly.T.to_dict().values())
            if len(esubsectors)>0:
                set_subsectors = False
                erecords = list(esubsectors.T.to_dict().values())
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
                    srecords.append({"name": "energy", "size": etotal, "children": erecords})
            record["children"] = srecords
        except Exception as e:
            record = {"error": e}
    return record

def other_record(world_g, top9ghg):
    record = {}
    names_map = {**sector_names, **e_subsectors}
    try:
        world_g.loc[:, "name"] = world_g["sector"].apply(lambda s: names_map.get(s, s))
        top9ghg.loc[:, "sector"] = top9ghg["sector"].apply(lambda s: names_map.get(s, s))
        
        total = world_g.loc[world_g["name"] == "Total excluding LUCF", "size"].values[0]
        ototal = total - top9ghg.loc[top9ghg["sector"] == "Total excluding LUCF"]["size"].sum()

        sonly = world_g.loc[world_g["name"].isin(list(sector_names.values())), ["name", "size"]].copy()
        sonly.loc[:, "size"] = sonly.apply(
            lambda r: r["size"] - top9ghg.loc[top9ghg["sector"] == r["name"]]["size"].sum(), axis=1)
        sonly.loc[:, "size"] = sonly["size"].apply(lambda s: round(s, 2))
        esubsectors = world_g.loc[world_g["name"].isin(list(e_subsectors.values())), ["name", "size"]].copy()
        esubsectors.loc[:, "size"] = esubsectors.apply(
            lambda r: r["size"] - top9ghg.loc[top9ghg["sector"] == r["name"]]["size"].sum(), axis=1)
        
        esubsectors.loc[:, "size"] = esubsectors["size"].apply(lambda s: round(s, 2))
        
        record = {"name": "Other", "size": round(ototal,2), "children": []}
        srecords = list(sonly.T.to_dict().values())
        if len(esubsectors)>0:
            set_subsectors = False
            erecords = list(esubsectors.T.to_dict().values())
            for s in srecords:
                if s["name"] == "energy":
                    set_subsectors = True
                    s["children"] = erecords
            if not set_subsectors:
                etotal = esubsectors["size"].sum()
                srecords.append({"name": "energy", "size": etotal, "children": erecords})
        record["children"] = srecords
    except Exception as e:
        traceback.print_exc()
        record = {"error": e}
    return record