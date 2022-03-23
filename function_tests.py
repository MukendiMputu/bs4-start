import unittest
import crawler_functions as crawler
import csv_file_reader as reader
import data_formatter as formatter
import helpers as helper
import os.path as path


class CrawlerFunctionTest(unittest.TestCase):
    def setUp(self):
        self.url = "http://google.com"
        self.dictionary = {
            "column1": ["one", "two", "3"],
            "column2": ["un", "deux", "trois"],
            "column3": ["eins", "zwei", "drei"],
        }
        self.brand_name = "Natural XL"

    def test_get_soup(self):
        self.assertIsNotNone(crawler.get_soup(self.url))

    def test_reader_get_billets_infos(self):
        self.assertIsNotNone(reader.get_billets_infos("billets_collection.csv"))

    def test_helpers_clean_href_string(self):
        self.assertEqual(helper.clean_href_string(self.brand_name), "natural-xl")

    def test_formatter_save_as_csv(self):
        formatter.save_as_csv("test.csv", self.dictionary)
        self.assertTrue(path.isfile("test.csv"))

    def test_formatter_save_as_json(self):
        formatter.save_as_json("test.json", self.dictionary)
        self.assertTrue(path.isfile("test.json"))

    def tearDown(self):
        self.url = None
        self.dictionary = None
        self.brand_name = None


if __name__ == '__main__':
    unittest.main()
