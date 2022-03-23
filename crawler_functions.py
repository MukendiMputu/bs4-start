import requests
from bs4 import BeautifulSoup

html_soup = None


# Extract the html content as text out of the response object
def get_soup(url):
    global html_soup
    url_response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if url_response.status_code in range(200, 400):
        # get soup from url_response object
        return BeautifulSoup(url_response.text, 'html.parser')
    else:
        print(f"Requested URL [{url_response.url}] failed with code: {url_response.status_code}")


# Extract the data byte
def get_data_byte(http_res):
    return http_res.content
