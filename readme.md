# Python Web Crawler for Extracting Data from Idealista:

Idealista is an online real estate platform serving the Spanish, Portuguese, and Italian markets. The primary goal of this web crawler is to extract data from the Idealista marketplace, specifically for buying and selling properties.

## Overview  
The crawler begins by visiting an initial page and extracting all relevant links to continue its journey through the site. As it navigates through each link, it first retrieves the links for subsequent pages and stores them in a Set. This Set will be used to queue up links to be visited after all property-related links have been processed.

Once all links have been visited or an error occurs, the crawler process will terminate, saving all the gathered data in a JSON file.

## 1-. Setup. 

To get started, the crawler operates within a specific filesystem structure. However, this structure can be customized as long as the `.env` file is appropriately updated.

## 1.1-. Filesystem.

data/  
├── clean/  
├── raw/  
│   ├── pages/  
│   ├── properties/  
│   └── proxies/  
└── structured/  

- raw/: Stores all raw data, including the proxies used and the raw HTML files crawled.  
- pages/: Contains HTML files with up to 30 properties each.
- properties/: Contains HTML files for each individual property crawled.
- proxies/: Stores the proxies used during the crawling process.
- structured/: Stores JSON data parsed from the HTML files.
- clean/: Stores CSV files generated after processing the JSON data.


## 1.2-. Configuring the `.env` File.  

After setting up the filesystem structure, you must configure the .env file to specify the properties data you wish to extract.

To avoid duplicating data, it's crucial to set both the INITIAL_URLS and TO_BE_EXCLUDED_URLS variables.

- INITIAL_URLS: Specifies the starting URLs for the crawler.
- TO_BE_EXCLUDED_URLS: Lists URLs that should not be visited.

This setup is essential because the first page can sometimes be targeted with and without /pagina-1.htm. By using the TO_BE_EXCLUDED_URLS, the crawler ensures that already visited pages are flagged and skipped to prevent data duplication.

## 2-. Execute the crawler. 

To run the crawler, execute the following command in your terminal:
``` 
python main_crawler.py
```

## 3-. Expected output in csv:


| property_id | tipology |  price | currency | squared_meter_price | location                   | address                                                                                                 | is_new_building | floor              | has_elevator | year_built | state         | squared_meters_constructed | squared_meters_useful | num_rooms | num_bathrooms | has_terrace | has_parking | has_storage_room | has_heating | heating_type                  | housing_direction | last_ad_update                   | webcrawler_date       | property_url                                                 | property_page_url                                                                 |
|-------------|----------|--------|----------|---------------------|----------------------------|--------------------------------------------------------------------------------------------------------|-----------------|-------------------|--------------|------------|---------------|----------------------------|-----------------------|-----------|---------------|-------------|-------------|------------------|--------------|--------------------------------|-------------------|----------------------------------|-----------------------|-------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| 104105870   | piso     | 196000 | €        | 2063                | Centro Puerto, Puerto de Sagunto | Calle Pablo Iglesias  Distrito Centro Puerto  Puerto de Sagunto  Camp de Morvedre, València            | False           | bajo exterior      | False        | 1950       | buen estado   | 95                         | 86                    | 3         | 1             | False       | False       | False            | False        |                                | oeste             | Anuncio actualizado el 31 de julio | 2024-08-27 11:16:33  | [link](https://www.idealista.com/inmueble/104105870/)       | [link](https://www.idealista.com/venta-viviendas/puerto-de-sagunto-valencia/)                                        |
| 105202418   | piso     | 159500 | €        | 2246                | Puerto de Sagunto          | Distrito Avda de Abril - 9 de Octubre  Puerto de Sagunto  Camp de Morvedre, València                    | False           | planta 3ª exterior | True         | 2010       | buen estado   | 71                         | 47                    | 2         | 1             | True        | True        | True             | True         | individual: bomba de frío/calor | sur               | Anuncio actualizado el 26 de agosto | 2024-08-27 11:16:33  | [link](https://www.idealista.com/inmueble/105202418/)       | [link](https://www.idealista.com/venta-viviendas/puerto-de-sagunto-valencia/)                                        |
| 105818560   | piso     | 132000 | €        | 1100                | Centro Puerto, Puerto de Sagunto | Calle Alacant, 7  Distrito Centro Puerto  Puerto de Sagunto  Camp de Morvedre, València                | False           | planta 5ª exterior | True         | 1973       | para reformar | 120                        | 108                   | 4         | 2             | False       | False       | False            | False        |                                | oeste             | Anuncio actualizado el 27 de agosto | 2024-08-27 11:16:33  | [link](https://www.idealista.com/inmueble/105818560/)       | [link](https://www.idealista.com/venta-viviendas/puerto-de-sagunto-valencia/)                                        |
| 103438857   | piso     | 89900  | €        | 1183                | Puerto de Sagunto          | Distrito Nuevo Centro  Puerto de Sagunto  Camp de Morvedre, València                                   | False           | bajo exterior      | False        | 1970       | buen estado   | 76                         | 73                    | 3         | 1             | False       | False       | False            | False        |                                | sur               | Anuncio actualizado el 27 de agosto | 2024-08-27 11:16:33  | [link](https://www.idealista.com/inmueble/103438857/)       | [link](https://www.idealista.com/venta-viviendas/puerto-de-sagunto-valencia/)                                        |


## 4-. Expected output in JSON:

```json 

[
    {
      "id": "104105870",
      "parent_url": "https://www.idealista.com/venta-viviendas/puerto-de-sagunto-valencia/",
      "url": "https://www.idealista.com/inmueble/104105870/",
      "created_timestamp": "2024-08-27 11:16:33",
      "updated_timestamp": null,
      "data": {
         "price": "196000",
         "currency": "€",
         "squared_meter_price": "2063",
         "location": "Centro Puerto, Puerto de Sagunto",
         "description_short": "piso de 95 m², Piso en venta en calle Pablo Iglesias, Centro Puerto, Puerto de Sagunto, Centro Puerto",
         "description_long": "your long description",
         "tipology": "piso",
         "updated": "Anuncio actualizado el 31 de julio",
         "address": "Calle Pablo Iglesias  Distrito Centro Puerto  Puerto de Sagunto  Camp de Morvedre, València",
         "ad_reference": "V2620",
         "advertiser_name": "Callaghan Inmobiliaria",
         "is_new_building": null,
         "Características básicas": [
            "95 m² construidos, 86 m² útiles",
            "3 habitaciones",
            "1 baño",
            "Segunda mano/buen estado",
            "Orientación oeste",
            "Construido en 1950",
            "No dispone de calefacción",
            "Solo interior de la vivienda adaptado para personas con movilidad reducida"
         ],
         "Edificio": [
            "Bajo exterior",
            "Sin ascensor"
         ],
         "Certificado energético": [
            "En trámite"
         ]
      }
   },
   {
      "id": "105202418",
      "parent_url": "https://www.idealista.com/venta-viviendas/puerto-de-sagunto-valencia/",
      "url": "https://www.idealista.com/inmueble/105202418/",
      "created_timestamp": "2024-08-27 11:16:33",
      "updated_timestamp": null,
      "data": {
         "price": "159500",
         "currency": "€",
         "squared_meter_price": "2246",
         "location": "Puerto de Sagunto",
         "description_short": "Ático de 71 m², Ático en venta en Avda de Abril - 9 de Octubre, Puerto de Sagunto, Avda de Abril - 9 de Octubre",
         "description_long": "your long description",
         "tipology": "piso",
         "updated": "Anuncio actualizado el 26 de agosto",
         "address": "Distrito Avda de Abril - 9 de Octubre  Puerto de Sagunto  Camp de Morvedre, València",
         "ad_reference": "24160",
         "advertiser_name": "Inmobiliaria MON",
         "is_new_building": null,
         "Características básicas": [
            "71 m² construidos, 47 m² útiles",
            "2 habitaciones",
            "1 baño",
            "Terraza y balcón",
            "Plaza de garaje incluida en el precio",
            "Segunda mano/buen estado",
            "Armarios empotrados",
            "Trastero",
            "Orientación sur",
            "Construido en 2010",
            "Calefacción individual: Bomba de frío/calor",
            "Solo acceso exterior adaptado para personas con movilidad reducida"
         ],
         "Edificio": [
            "Planta 3ª exterior",
            "Con ascensor"
         ],
         "Equipamiento": [
            "Aire acondicionado"
         ],
         "Certificado energético": [
            "En trámite"
         ]
      }
   },
   {
      "id": "105818560",
      "parent_url": "https://www.idealista.com/venta-viviendas/puerto-de-sagunto-valencia/",
      "url": "https://www.idealista.com/inmueble/105818560/",
      "created_timestamp": "2024-08-27 11:16:33",
      "updated_timestamp": null,
      "data": {
         "price": "132000",
         "currency": "€",
         "squared_meter_price": "1100",
         "location": "Centro Puerto, Puerto de Sagunto",
         "description_short": "piso de 120 m², Piso en venta en calle Alacant, 7, Centro Puerto, Puerto de Sagunto, Centro Puerto",
         "description_long": "your long description",
         "tipology": "piso",
         "updated": "Anuncio actualizado el 27 de agosto",
         "address": "Calle Alacant, 7  Distrito Centro Puerto  Puerto de Sagunto  Camp de Morvedre, València",
         "ad_reference": "HY-ALICANTE7/LJ",
         "advertiser_name": "medina&co",
         "is_new_building": null,
         "Características básicas": [
            "120 m² construidos, 108 m² útiles",
            "4 habitaciones",
            "2 baños",
            "Balcón",
            "Segunda mano/para reformar",
            "Armarios empotrados",
            "Orientación oeste",
            "Construido en 1973"
         ],
         "Edificio": [
            "Planta 5ª exterior",
            "Con ascensor"
         ],
         "Certificado energético": [
            "Consumo: 176 kWh/m² año",
            "Emisiones: 43 kg CO2/m² año"
         ]
      }
   }, ...
]

```