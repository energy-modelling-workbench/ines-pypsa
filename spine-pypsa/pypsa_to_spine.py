import sys
import pypsa
import spinedb_api as api
from spinedb_api import purge

def main(input, output):
    print("load nc file")
    n = pypsa.Network(input)

    # Set icons for PyPSA components in spine, default is None
    iconmap = {
        #"Network":,
        #"SubNetwork":,
        "Bus":280683380142637,
        #"Carrier":,
        "GlobalConstraint":281246450775340,
        "Line":280462687073079,
        #"LineType":,
        #"Transformer":,
        #"TransformerType":,
        #"Link":,
        #"Load":,
        "Generator":280740537364493,
        #"StorageUnit":,
        #"Store":,
        #"ShuntImpedance":,
        #"Shape":,
    }

    with api.DatabaseMapping(output) as spinedb:
        datadict = {
            "alternatives": [[
                "PyPSA",
                ""
            ]]
        }
        purge.purge(spinedb, purge_settings=None)
        spinedb.refresh_session()
        api.import_data(spinedb,**datadict)

        # the data is streamed to the database in pieces, alternatively all data could be collected in a dictionary first and then imported in its entirety.
        # check https://pypsa.readthedocs.io/en/latest/user-guide/components.html for the structure of n
        for component,table in n.components.items():
            spinedb.refresh_session()

            print("add " + component + " class and parameter definitions")

            datadict = {
                "entity_classes":[[
                    component, # class name
                    [], # connected entities
                    table["description"], # description?
                    iconmap.get(component), # icon
                    False
                ]],
                "parameter_definitions":[],
            }
            parameters = table["attrs"].to_dict(orient='index')
            for parametername, dataframe in parameters.items():
                datadict["parameter_definitions"].append([
                    component, # entity class
                    parametername, # parameter name
                    dataframe["default"], # default value
                    None, # parameter value list
                    dataframe["description"] # description
                ])
            api.import_data(spinedb,**datadict)
            spinedb.commit_session(component + " entity class and parameter definition")

            if hasattr(n, table["list_name"]):

                print("add " + component + " entities and parameter values")

                n_component = getattr(n, table["list_name"]).to_dict("index")
                # correct dictionary for empty keys
                n_component = {k: v for k, v in n_component.items() if k}
                for name,parameters in n_component.items():
                    #Exception for shape
                    if component == "Shape":
                        parameters["geometry"] = str(parameters["geometry"])
                    
                    datadict = {
                        "entities":[[
                            component,
                            name,
                            None
                        ]],
                        "parameter_values":[],
                    }
                    for parametername,value in parameters.items():
                        datadict["parameter_values"].append([
                            component,
                            name,
                            parametername,
                            value,
                            "PyPSA"
                        ])
                    #print(datadict) # debug line
                    api.import_data(spinedb,**datadict)
                    spinedb.commit_session(component + " entities and parameter values")

if __name__ == "__main__":
    input = sys.argv[1] # nc file
    output = sys.argv[2] # spine db

    main(input, output)