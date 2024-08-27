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