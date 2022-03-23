import requests
from bs4 import BeautifulSoup


# Send an XHR-request and returns the response object
def get_url(url):
    return requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})


# Extract the html content as text out of the response object
def get_soup(http_response):
    return BeautifulSoup(http_response.text, 'html.parser')


# Extract the data byte
def get_data_byte(http_res):
    return http_res.content


# Clean the name of each product
def clean_title(title_list):
    clean_list = [title.replace(" ", "_") for title in title_list]
    return clean_list


# Match anchors with href containing the given string
def clean_href_string(string_literal):
    return string_literal.lower().replace(" ", "-")
