import re
import crawler_functions as crawler
import csv_file_reader as xls_reader
import data_formatter as formatter


def main():
    base_url = "https://www.wollplatz.de/wolle/"

    billets = xls_reader.get_billets_infos("billets_collection.csv")
    # create a list to hold billets
    billets_info_list = []

    for brand, name in billets.items():
        collected_billets_infos = {"brand": brand, "name": name}  # billets dictionary
        # construct specific url and send request
        base_url_response = crawler.get_url(base_url)
        brand_url = base_url + crawler.clean_href_string(brand)

        if base_url_response.status_code in range(200, 400):
            # get soup from base_url_response object
            html_soup = crawler.get_soup(base_url_response)

            # extract the needed brand url(s)
            collected_billets_infos["url"] = [anchor.attrs['href'] for anchor in
                                              html_soup.find_all('a', {'href': re.compile(brand_url)})]
            billets_info_list.append(collected_billets_infos)
        else:
            print(f"Base URL request failed with code: {base_url_response.status_code}")

    # for each url found get the html soup and search for
    # TODO: Refactor from O(n^2) to O(n)
    for billet in billets_info_list:
        if not billet["url"]:
            continue
        print(billet["name"], billet["url"][0])
        brand_url_response = crawler.get_url(billet["url"][0])

        if brand_url_response.status_code in range(200, 400):
            brand_html_soup = crawler.get_soup(brand_url_response)
            # extract the product urls from the html soup
            # TODO: refactor list comprehension
            product_url = [anchor.attrs['href'] for anchor in brand_html_soup.find_all('a') if
                           crawler.clean_href_string(billet["name"]) in anchor['href'].split('/')[-1]]
            product_url = list(dict.fromkeys(product_url))  # remove duplicates

            # if there's a link to the product, get the information needed
            if product_url:
                print(product_url[0])
                product_url_response = crawler.get_url(product_url[0])
                if product_url_response.status_code in range(200, 400):
                    product_html_soup = crawler.get_soup(product_url_response)
                    # find the price
                    price_span = product_html_soup.find('span', class_='product-price', itemprop='price')
                    billet["price"] = float(price_span["content"])
                    # find out whether in stock or not
                    delivery_time = product_html_soup.find('span', text=re.compile(r'lieferbar'))
                    billet["delivery_time"] = delivery_time.text if delivery_time is not None else ''
                    # find the needle size
                    needle_size = product_html_soup.find('td', text='Nadelstärke').find_next_sibling()
                    billet["needle_size"] = needle_size.text if needle_size is not None else ''
                    # find the composition
                    composition = product_html_soup.find('td', text='Zusammenstellung').find_next_sibling()
                    billet["composition"] = composition.text if composition is not None else ''
                else:
                    print(f"Product URL request failed with code: {product_url_response.status_code}")
        else:
            print(f"Brand URL request failed with code: {brand_url_response.status_code}")

    # save diction as a csv file with price, delivery time, needle size and composition column
    formatter.save_as_csv(file_name="billets_info.csv", dictionary=billets_info_list)
    formatter.save_as_json(file_name="billets_info.json", dictionary=billets_info_list)


if __name__ == '__main__':
    main()
