import os
from typing import Set, ClassVar
from pydantic import HttpUrl
from bs4 import BeautifulSoup
from datetime import datetime
import json
import requests 
import itertools
from pathlib import Path
from utils.request_metadata import RequestsMetadata
from utils.properties.property import PropertyData
from utils.properties.property_storage import PropertyStorage
from tenacity import retry, stop_after_attempt


class IdealistaWebCrawler:

    HEADERS: ClassVar[str] = {
        "User-Agent": None,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US;en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    } 

    REQUEST_METADATA: ClassVar[RequestsMetadata] 

    def __init__(self, core_url, logger, url=None, path=None):
        self.is_pagination: bool = True
        self._core_url = core_url
        self.initial_url: HttpUrl = url  
        self._soup: BeautifulSoup = path
        self.storage: PropertyStorage = PropertyStorage()
        self.logger = logger

    @property
    def soup(self):
        return self._soup
    
    @soup.setter
    def soup(self, new_path: str | None):
        if new_path is None:
            self._soup = None
        else:
            self._soup: BeautifulSoup = BeautifulSoup(open(new_path, "r", encoding='utf-8'), 'html.parser')

    def _extract_properties_ids(self):
        # si no tenemos soup, lanzamos una excepcion.
        if self.soup is None:
            raise ValueError("Please asign a proper soup before extracting properties ids.")
        if self.initial_url is None:
            raise Warning("If no initial_url set up, PropertyData object won't have parent url")
        # Encontrar el artículo que tiene el atributo data-element-id
        articles = self._soup.find_all("article", {"data-element-id": True})
        if len(articles):
            for article in articles:
                curr_id = article.get('data-element-id')
                # generamos un nuevo objeto.
                new_property = PropertyData(
                    id=curr_id,
                    parent_url=self.initial_url,
                    url=self._core_url + f"/inmueble/{curr_id}/"
                )
                # añadirlo.
                result = self.storage.add(new_property)
                if result: self.logger.info(f"[OK] Propiedad {curr_id:12} añadida con éxito al storage.")
                else: self.logger.info(f"[ERROR] Propiedad {curr_id:12} dio error al intentar añadirse.")


    def get_next_urls(self)-> Set[str]:
        # si no tenemos soup, lanzamos una excepcion.
        if self.soup is None:
            raise ValueError("Please asign a proper soup before extracting next urls")
        if not self.is_pagination:
            raise ValueError("Impossible to get next urls since pagination is set to False")

        pagination = self._soup.find("div", class_='pagination')
        if pagination is not None:
            return {self._core_url + link.get('href') for link in pagination.find_all('a')}
        return {}
    

    def get_property_data(self):
        # si no tenemos soup, lanzamos una excepcion.
        if self.soup is None:
            raise ValueError("Please asign a proper soup before extracting next urls")
        
        property_data = {
            "price": None,
            "currency": None,
            "squared_meter_price": None,
            "location": None,
            "description_short": None,
            "description_long": None,
            "tipology": None,
            "updated": None,
            "address": None,
            "ad_reference": None,
            "advertiser_name": None,
            "is_new_building": None
        }
        # precio y moneda
        price_data = self._soup.find("span", class_="info-data-price")
        if price_data is not None:
            price_data = price_data.get_text().split(" ")
            property_data["price"] = price_data[0].replace(".", "")
            property_data["currency"] = price_data[1]
        # precio por metro cuadrado.
        squared_meter_price_data = self._soup.find("p", class_="flex-feature squaredmeterprice")
        if squared_meter_price_data is not None:
            squared_meter_price_data = squared_meter_price_data.get_text().replace("\n", "").split(":")[-1].split(" ")[0].replace(".", "")
            property_data["squared_meter_price"] = squared_meter_price_data
        # localizacion
        location_data = self._soup.find("span", class_="main-info__title-minor")
        if location_data is not None:
            property_data["location"] = location_data.get_text()
        # descripcion corta
        description_data_short = self._soup.find("meta", {"name": "description"})
        if description_data_short is not None:
            property_data["description_short"] = description_data_short.get('content')
        # descripcion larga
        description_data_long = self._soup.find("div", class_="comment")
        if description_data_long is not None:
            property_data["description_long"] = description_data_long.get_text().replace("\n", "")
        # tipologia
        tipologia_data = self._soup.find("strong", class_="typology")
        if tipologia_data is not None:
            property_data["tipology"]= tipologia_data.get_text().replace("\n", "")
        # last updated
        updated_data = self._soup.find("p", class_="stats-text")
        if updated_data is not None:
            property_data["updated"]= updated_data.get_text()
        # address
        address_data = self._soup.find("div", id="headerMap")
        if address_data is not None:
            property_data["address"] = "".join([x.get_text() for x in address_data.find_all("li")]).replace("\n", " ").rstrip().lstrip()
        # datos del anuncio
        advert_reference_data = self._soup.find("div", class_="ad-reference-container")
        if advert_reference_data is not None:
            advert_reference_data = advert_reference_data.find("p", class_="txt-ref")
            property_data["ad_reference"] = advert_reference_data.get_text().replace("\n", "")
        # datos del anunciante.
        advertiser_data = self._soup.find("div", class_="professional-name")
        if advertiser_data is not None:
            advertiser_data = advertiser_data.find("span")
            property_data["advertiser_name"] = advertiser_data.get_text().replace("\n", "")
        # is new building.
        new_building_data = self._soup.find("strong", class_="info-urgent")
        if new_building_data is not None:
            property_data["is_new_building"] = new_building_data.get_text().replace("\n", "")
                
        features_data = self._soup.find_all("div", class_="details-property_features")
        label_name_data = self._soup.find_all("h2", class_="details-property-h2", id=False)
        # labels might be greater than features. 
        assert len(features_data) == len(label_name_data)
        if features_data is not None:
            for i in range(len(label_name_data)):
                curr_label_name = label_name_data[i].get_text()
                feature_list = []
                curr_feature_data = features_data[i].find_all("li")
                for data in curr_feature_data:
                    feature_list.append(data.get_text().replace("\n", ""))
                # add into dict.
                property_data[curr_label_name] = feature_list
        return property_data

    def _update_proxy_and_user_agent(cls):
        # Cambia el proxy y el user-agent antes de cada reintento
        IdealistaWebCrawler.HEADERS["User-Agent"] = next(IdealistaWebCrawler.REQUEST_METADATA.user_agents)
        IdealistaWebCrawler.REQUEST_METADATA.curr_proxy = next(IdealistaWebCrawler.REQUEST_METADATA.proxies)

    @retry(stop=stop_after_attempt(5))
    def get_source_data(self, url, output_path, name) -> str | None:
        # actualizamos los header y proxies antes de ejecutar de nuevo la request.
        self._update_proxy_and_user_agent()

        with requests.Session() as session:
            try:
                name = f"{datetime.now().strftime('%Y%m%d')}_{name}"
                response = session.get(url, headers=IdealistaWebCrawler.HEADERS, proxies={'http://': IdealistaWebCrawler.REQUEST_METADATA.curr_proxy})
                # raise HTTPError por bad requests.
                response.raise_for_status()
                
                if response.status_code == 200:
                    target_path = os.path.join(output_path, f"{name}.html")
                    with open(target_path, "w", encoding='utf-8') as file:
                        file.write(response.text)
                    self.logger.info(f"{name} saved successfully")
                    return target_path
            except Exception as err:
                self.logger.error(f"Error {type(err)} trying to extract: {url}")
                return None
            
