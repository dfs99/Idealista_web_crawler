"""
The following file only contains general purpose functions for the program 
"""

import json
import os 
import pandas as pd 

def get_name(url: str) -> str:

    """ 
    It's expected to be a url that contains several properties.
    Given an URL like "https://www.idealista.com/venta-viviendas/puerto-de-sagunto-valencia/pagina-1.htm"
    
    we would return: "puerto-de-sagunto-valencia_pagina-1"
    """
    data = url.split("/")
    page_num = data[-1]
    location = data[-2]
    return f"{location}_{page_num.split('.')[0]}"


def get_name_property(url: str) -> str:

    """ 
    It's expected to be a url contains a single property.
    URL: "https://www.idealista.com/inmueble/26708492/"
    
    we would return: "inmueble_26708492"
    """

    data = url.split("/")
    id = data[-2]
    type = data[-3]
    return f"{type}_{id}"


def data_json_to_csv_file(json_path, output_path):
    """
    The function does not extract all features. However those extracted are the most representative. 
    For instance, whether the house has energy certification is not currently extracted.
    """

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Input path is not defined: {json_path}")
    
    # initialise variables to store data.
    properties = []
    data = None

    # fetch raw json data.
    with open(json_path, "r") as file:
        data = json.load(file)
    
    # for each property.
    for propiedad in data:
        
        datablock = propiedad.get("data")
        # variables to get.
        variables = {
            "property_id": propiedad.get("id"),
            "tipology": datablock.get("tipology"),
            "price": datablock.get("price"),
            "currency": datablock.get("currency"),
            "squared_meter_price": datablock.get("squared_meter_price"),
            "location": datablock.get("location"),
            "address": datablock.get("address"),
            "is_new_building": False if datablock.get("is_new_building") is None else True,
            "floor": None,
            "has_elevator": False,
            # variables de características básicas.
            "year_built": None,
            "state": None,
            "squared_meters_constructed": None,
            "squared_meters_useful": None,
            "num_rooms": None,
            "num_bathrooms": None,
            "has_terrace": False,
            "has_parking": False,
            "has_storage_room": False,
            "has_heating": False,
            "heating_type": None,
            "housing_direction": None, # orientacion de la vivienda.
            # Otras variables.
            "last_ad_update": datablock.get("updated"),
            "webcrawler_date": propiedad.get("created_timestamp"),
            "property_url": propiedad.get("url"),
            "property_page_url": propiedad.get("parent_url"),
        }

        
        if datablock:
            basic_features = datablock.get("Características básicas")
            for b in basic_features:
                b= b.lower()
                if "m²" in b:
                    variables["squared_meters_constructed"] = b.split(" ")[0]
                    if "útil" in b:
                        variables["squared_meters_useful"] = b.split(", ")[1].split(" ")[0]
                elif "habitaci" in b:
                    variables["num_rooms"] = b.split(" ")[0]
                elif "bañ" in b:
                    variables["num_bathrooms"] = b.split(" ")[0]
                elif "terraza" in b:
                    variables["has_terrace"] = True
                elif "garaje" in b:
                    variables["has_parking"] = True
                elif "calefacción" in b:
                    # comprobar si tiene o no tiene.
                    if "no dispone de" in b:
                        variables["heating_type"]=None
                    elif "individual" in b:
                        variables["has_heating"]=True 
                        try:
                            variables["heating_type"]=f"individual: {b.split(':')[1]}"
                        except IndexError as err:
                            variables["heating_type"] = "individual"   
                elif "construido" in b:
                    variables["year_built"] = b.split(" ")[-1]
                elif "trastero" in b:
                    variables["has_storage_room"]=True
                elif "orientación" in b:
                    variables["housing_direction"] = b.replace("orientación", "").rstrip().lstrip()
                elif "segunda mano" in b:
                    variables["state"] = b.split('/')[1]

            building_features = datablock.get("Edificio")            
            if building_features:
                for b in building_features:
                    b = b.lower()
                    if "planta" in b or "bajo" in b:
                        variables["floor"] = b 
                    elif "con ascensor" in b:
                        variables["has_elevator"]=True
            
        properties.append(variables)
    
    # once all the data has been formated. It will be stored.
    pd.DataFrame(properties).to_csv(output_path, index=False)

