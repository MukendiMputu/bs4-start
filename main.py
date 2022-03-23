import re
import crawler_functions as crawler
import csv_file_reader as xls_reader
import data_formatter as formatter
import helpers


def main():
    base_url = "https://www.wollplatz.de/wolle/"
    brand_urls = []
    billets_info_list = []  # create a list to hold billets

    billets = xls_reader.get_billets_infos("billets_collection.csv")

    try:
        base_url_soup = crawler.get_soup(base_url)
        brand_urls = [anchor.attrs['href'] for anchor in
                      base_url_soup.find_all('a', {'href': re.compile(base_url)})]
        print(f"Brand urls :{brand_urls}")
    except AttributeError as err:
        print(f"Error: could not retrieve a soup from URL [{base_url}]!")

    for brand, name in billets.items():
        # construct specific url and send request
        brand_url_regex = base_url + helpers.clean_href_string(brand)
        # extract the needed brand url(s)
        found_name_urls = [link for link in brand_urls if re.match(helpers.clean_href_string(brand_url_regex), link)]
        print(f"Brand urls :{found_name_urls}")
        # billets dictionary
        collected_billets_infos = {
            "brand": brand,
            "name": name,
            "url": found_name_urls
        }

        billets_info_list.append(collected_billets_infos)

    # for each brand-name url found get the html soup and search for
    # TODO: Refactor from O(n^2) to O(n)
    for billet in billets_info_list:
        if not billet["url"]:
            print(f"Skipping {billet['brand']} - {billet['name']} [no URL found]")
            continue
        print(f"Processing {billet['brand']} - {billet['name']} [{billet['url'][0]}]")
        brand_html_soup = crawler.get_soup(billet["url"][0])

        # extract the product urls from the html soup
        # TODO: refactor list comprehension
        product_url = [anchor.attrs['href'] for anchor in brand_html_soup.find_all('a') if
                       helpers.clean_href_string(billet["name"]) in anchor['href'].split('/')[-1]]
        product_url = list(dict.fromkeys(product_url))  # remove duplicates

        # if there's a link to the product, get the information needed
        if product_url:
            print(product_url[0])
            product_html_soup = crawler.get_soup(product_url[0])
            # find the price
            price_span = product_html_soup.find('span', class_='product-price', itemprop='price')
            billet["price"] = float(price_span["content"])
            # find out whether in stock or not
            in_stock_div = product_html_soup.find('div', id=re.compile(r'ContentPlaceHolder1_upStockInfoDescription'))
            billet["in_stock"] = in_stock_div.text.strip() if in_stock_div is not None else ''
            # find the needle size
            needle_size = product_html_soup.find('td', text='Nadelstärke').find_next_sibling()
            billet["needle_size"] = needle_size.text.strip() if needle_size is not None else ''
            # find the composition
            composition = product_html_soup.find('td', text='Zusammenstellung').find_next_sibling()
            billet["composition"] = composition.text.strip() if composition is not None else ''

    # save diction as a csv file with price, delivery time, needle size and composition column
    formatter.save_as_csv(file_name="billets_info.csv", dictionary=billets_info_list)
    formatter.save_as_json(file_name="billets_info.json", dictionary=billets_info_list)


if __name__ == '__main__':
    main()
