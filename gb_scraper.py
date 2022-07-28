import requests, re
from bs4 import BeautifulSoup


# get soup object
def get_soup(URL):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    return BeautifulSoup(page.content, "html.parser")

# extract data from gas buddy
def get_gb_data(soup):

    # get all relative HTML elements containing gas price data
    elements = soup.find_all("div", attrs={'class': re.compile('^GenericStationListItem-module__stationListItem.*')})

    """
        data list (tuples)  # all strings
        [   
            (Station Name, Station Address, Gas Price),
            (..., ..., ...),
            (..., ..., ...)
        ]
    """
    data = []

    # loop through each HTML element to extract specific information
    for elm in elements:

        station_name = elm.find("h3", attrs={'class': re.compile('^header.*')})
        station_address = elm.find("div", attrs={'class': re.compile('^StationDisplay-module__address.*')})
        price = elm.find("div", attrs={'class': re.compile('^StationDisplayPrice-module__priceContainer.*')}).find('span')
        
        # add data to list as a tuple for each iteration
        data.append((station_name.text, station_address.text, price.text))

    return data