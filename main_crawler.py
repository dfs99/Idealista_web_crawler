from utils.webcrawler import IdealistaWebCrawler
from utils.functions import get_name, get_name_property, data_json_to_csv_file
from utils.request_metadata import RequestsMetadata
from typing import Set, List, Dict
import json
from datetime import datetime
import time 
import logging
from dotenv import load_dotenv
import os
import itertools
from pathlib import Path
from utils.proxy_finder import ProxyFinder


# logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# environment variables setup and loaded.
load_dotenv()

# get data from env vars.
_SET_TO_EXTRACT: Set[str]        = set(os.getenv("INITIAL_URLS").split(","))
_SET_ALREADY_EXTRACTED: Set[str] = set(os.getenv("TO_BE_EXCLUDED_URLS").split(","))
_ROOT_URL: str                   = os.getenv("ROOT_URL")
_RESULTS_PATH: str               = os.getenv("DIRECTORY_OUTPUT")
_RESULTS_CSV_PATH: str           = os.getenv("DIRECTORY_CSV_OUTPUT")
_RESULTS_FILENAME: str           = os.getenv("FILENAME_OUTPUT")
_RESULTS_FILENAME_EXTENSION: str = os.getenv("FILENAME_OUTPUT_EXTENSION")
_DIR_RAW_PROPERTIES: Path        = Path(os.getenv("DIRECTORY_TO_STORE_PROPERTIES"))
_DIR_RAW_PAGES: Path             = Path(os.getenv("DIRECTORY_TO_STORE_PAGES"))

# for proxy finder config.
_NUM_PROXIES_TO_USE              = int(os.getenv("MAX_NUMBER_PROXIES"))
_DIR_STORE_PROXY_LIST            = os.getenv("DIR_TO_STORE_PROXIES")
_URL_PROXIES                     = os.getenv("URL_PROXIES")
_URL_TEST_PROXIES                = os.getenv("URL_TEST_PROXIES")
_MY_PROXY_LIST: List[str] = []


# variable where data is stored dynamically.
_RESULTS: List[Dict] = []


_MY_USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
]

if __name__ == "__main__":
    logger.info("---------- Job started ----------")
    logger.info("Start checking input parameters through `.env` file")

    # First off, check if directory is valid.
    if not os.path.exists(_RESULTS_PATH):
        raise FileNotFoundError(f"Directory output is not defined: {_RESULTS_PATH}")
    
    # Check if the extension is `json`
    if _RESULTS_FILENAME_EXTENSION != "json":
        raise ValueError(f"Up to now, only `json` is valid for output filename extensions.") 

    # Since the path is valid, create the output file name.
    OUTPUT_FULLPATH_NAME = os.path.join(_RESULTS_PATH, f"{_RESULTS_FILENAME}_{datetime.now().strftime('%Y-%m-%d')}.{_RESULTS_FILENAME_EXTENSION}")
    logger.info(f"Path where JSON data will be stored: {OUTPUT_FULLPATH_NAME}")
    OUTPUT_FULLPATH_CSV_FILE = os.path.join(_RESULTS_CSV_PATH, f"{_RESULTS_FILENAME}_{datetime.now().strftime('%Y-%m-%d')}.csv")
    logger.info(f"Path where csv data will be stored: {OUTPUT_FULLPATH_CSV_FILE}")
    
    logger.info("Initial Target urls to be extracted:")
    for target_url in _SET_TO_EXTRACT:
        logger.info(f"-> {target_url}")

    logger.info("Getting the free proxy list to extract the information.")
    proxy_finder = ProxyFinder(
        url = _URL_PROXIES,
        test_url=_URL_TEST_PROXIES,
        path=_DIR_STORE_PROXY_LIST,
        logger=logger
    )
    _MY_PROXY_LIST = proxy_finder.validate_proxies(_NUM_PROXIES_TO_USE)
    logger.info("Proxies extracted correctly.")

    # inicio del script.
    start_t = time.time()

    request_metadata = RequestsMetadata(
        proxies=itertools.cycle(_MY_PROXY_LIST),
        curr_proxy=None,
        user_agents= itertools.cycle(_MY_USER_AGENT_LIST),
        odir_pages=_DIR_RAW_PAGES,
        odir_properties=_DIR_RAW_PROPERTIES
    )
    crawler = IdealistaWebCrawler(_ROOT_URL, logger=logger)
    # asignamos las variables de clase que tiene el crawler.
    IdealistaWebCrawler.REQUEST_METADATA = request_metadata

    logger.info(f"Crawler initialised.")

    try:
        # mientras existan urls que extraer.
        while _SET_TO_EXTRACT:
            target_url = _SET_TO_EXTRACT.pop()
            # le indicamos al crawler la url a explorar.
            crawler.initial_url = target_url

            # extraer la información de la página. Nota. Tiene política de retries.         
            data_path = crawler.get_source_data(target_url, IdealistaWebCrawler.REQUEST_METADATA.odir_pages, get_name(target_url))
            # si nos devuelve el path en donde hemos almacenado la información.
            if data_path is not None: 
                # no hubo problema, lo añadimos para trackear.
                _SET_ALREADY_EXTRACTED.add(target_url)
                # inicializamos con Beautiful Soup para extraer la informacion
                crawler.soup = data_path
                
                # si tenemos la paginación activada, extraemos los links siguientes.
                if crawler.is_pagination:
                    
                    next_links: Set[str] = crawler.get_next_urls()

                    # sacamos los nuevos enlaces a seguir explorando.
                    for new_url in next_links.difference(_SET_ALREADY_EXTRACTED):
                        logger.info(f"New url to be crawled: {new_url}")
                        _SET_TO_EXTRACT.add(new_url)

                # del dato extraido, sacar los inmuebles.
                crawler._extract_properties_ids()

                for property in crawler.storage.retrieve():
                    # extraemos la información de las propiedades de la página. Tiene retries.
                    #logger.info(f"property id to be extracted: {property.id}")
                    data_path = crawler.get_source_data(property.url, IdealistaWebCrawler.REQUEST_METADATA.odir_properties, get_name_property(property.url))
                    # si hemos obtenido la información.
                    if data_path is not None:
                        # actualizamos el soup.
                        crawler.soup = data_path
                        # extraemos la información.
                        property.data = crawler.get_property_data()
                        # Almacenamos el resultado.
                        _RESULTS.append(property.model_dump())
                        logger.info(f"[OK] Property: {property.id} added successfully to _Results")
                    else:
                        logger.error(f"[KO] Url property failed: {property.url}")
                     
 
        
    except Exception as err:
        logger.info(f"An error has been risen. Storing already extracted data.")
        logger.info(f"Traceback: {type(err)}")
        logger.info(f"Traceback: {err}")
    
    finally:
        with open(OUTPUT_FULLPATH_NAME, "w", encoding='utf-8') as file:
           json.dump(_RESULTS, file, ensure_ascii=False, indent=3)

        logger.info(f"Elapsed time webcrawler working: {time.time() - start_t} seconds")

        logger.info("Transform json data into a csv file")
        try:
            data_json_to_csv_file(
                OUTPUT_FULLPATH_NAME,
                OUTPUT_FULLPATH_CSV_FILE
            )
            logger.info("Transformation done successfully.")
        except Exception as err:
            logger.error("An error ocurred while performing the transformation. Unable to transform data into csv file.")
        

        logger.info("----------  Job ended  ----------")