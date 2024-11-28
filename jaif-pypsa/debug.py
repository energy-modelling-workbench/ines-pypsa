from pprint import pprint
import csv

data_path='/home/u0102409/MyApps/pypsa/pypsa-eur data/'
tdr={
    '2020':data_path+'costs_2020.csv',
    '2030':data_path+'costs_2030.csv',
    '2040':data_path+'costs_2040.csv',
    '2050':data_path+'costs_2050.csv',
}

unit_types={}
for year,path in tdr.items():
    with open(path, 'r') as file:
        unit_types[year]={}
        for line in csv.reader(file):
            if line[0] not in unit_types[year]:
                unit_types[year][line[0]]={}
            unit_types[year][line[0]][line[1]]=line[2]
            #unit_types[year][line[0]][line[1]+'_description']=line[3]+' '+line[4]+' '+line[5]
#pprint(unit_types)

# check consistency
for unit_type in unit_types.values():
    for key in unit_type.keys():
        for year,unit_type_year in unit_types.items():
            if key not in unit_type_year.keys():
                print(key+' is not in '+year)

ppm=data_path+'powerplants.csv'

with open(ppm, mode='r') as file:
    unit_instances = list(csv.DictReader(file))
unitlist=[]
otherlist=[]
for unit in unit_instances:
    if unit["Technology"] not in unitlist:
        unitlist.append(unit["Technology"])
    if unit["Fueltype"] == 'Other' and (unit["Technology"],unit["Set"]) not in otherlist:
        otherlist.append((unit["Technology"],unit["Set"]))
print(unitlist)
print()
pprint(otherlist)

# from print statement in ppmtdr_to_jaif
# used to identify elements for the 'exclude' list
# and the map for powerplants (ppm) to costs (tdr)
fuel_type_costkey = [
    "Hard Coal Steam Turbine {'2020': 'coal'}",
    "Nuclear Steam Turbine {'2020': 'nuclear'}",
    "Hard Coal CCGT {'2020': 'coal'}",
    "Lignite Steam Turbine {'2020': 'lignite'}",
    "Natural Gas CCGT {'2020': 'CCGT'}",
    "Solid Biomass Steam Turbine {'2020': 'solid biomass boiler steam'}",
    "Oil Steam Turbine {'2020': 'oil'}",
    "Natural Gas Steam Turbine {'2020': 'gas boiler steam'}",
    "Hard Coal  {'2020': 'coal'}",
    "Lignite  {'2020': 'lignite'}",
    "Oil  {'2020': 'oil'}",
    "Oil CCGT {'2020': 'oil'}",
    "Biogas  {'2020': 'biogas'}",
    "Biogas CCGT {'2020': 'biogas'}",
    "Natural Gas  {'2020': 'CCGT'}",
    "Solid Biomass  {'2020': 'solid biomass boiler steam'}",
    "Biogas Steam Turbine {'2020': 'biogas'}",
    "Natural Gas Combustion Engine {'2020': 'direct firing gas'}",
    "Biogas Combustion Engine {'2020': 'biogas'}"
]