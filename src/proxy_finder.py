import requests
import json 
import os
from typing import List
from datetime import datetime
import logging



class ProxyFinder:

    def __init__(self, url, test_url, path, logger, proxy_protocol_type="http", testing_timeout=20):
        self._url = url
        self._test_url = test_url
        self._proxy_protocol_type = proxy_protocol_type
        self._testing_timeout = testing_timeout
        self.path = path 
        self.logger = logger
        
        try:
            # perform the request to get a list of free proxies.
            result = requests.get(self._url)
            # get data to be able to check it out.
            self._data = json.loads(result.text )
            # store the data.
            with open(os.path.join(self.path, f"proxy_list_{datetime.now().strftime('%Y-%m-%d')}.json"), "w", encoding='utf-8') as file:
                json.dump(self._data, file, ensure_ascii=False, indent=3)
        except Exception as err:
            self.logger.error("Unable to extract the proxy list right now.")
            self.logger.error(f"It was triggered by: {err}")

    def validate_proxies(self, max_number) -> List[str]:
        # A request is done to check the validity of a proxy.
        available_proxies = []
        for proxy in self._data["proxies"]:
            if len(available_proxies)==max_number: 
                self.logger.info("Maximum number of proxies reached. Return the list of valid proxies.")
                break
            if proxy["protocol"]==self._proxy_protocol_type:
                try:    
                    res = requests.get(self._test_url, proxies={self._proxy_protocol_type: proxy["ip"]}, timeout=self._testing_timeout)
                    if res.status_code == 200:
                        available_proxies.append(proxy["proxy"])
                        self.logger.info(f"[OK] Proxy: {proxy['proxy']}")
                except Exception:
                    self.logger.error(f"[KO] Proxy: {proxy['proxy']}")
        return available_proxies
    





