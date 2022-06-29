import re
import sys
import unittest

from csv_table.csv_table import CsvTable
import csv_table.csv_table as cvt

SHORT_CSV = ["h1;h2;h 3",
             "1;ä;text space",
             "2;b;c",
             "3;d;e",
             "4;f;g"]


class CsvData(unittest.TestCase):

    def test_init_csv_with_data(self):
        # arrange
        raw_csv = ["h1;h2;h 3", "1;ä;text space"]
        # act
        table = CsvTable(raw_csv)
        # assert
        self.assertEqual("h1", table.caption[0], "caption incorrect")
        self.assertEqual("h2", table.caption[1], "caption incorrect")
        self.assertEqual("h 3", table.caption[2], "caption incorrect")

        self.assertEqual("1", table.data_raw[0][0], "data incorrect")
        self.assertEqual("ä", table.data_raw[0][1], "data incorrect")
        self.assertEqual("text space", table.data_raw[0][2], "data incorrect")

    def test_init_csv_without_data(self):
        # arrange
        raw_csv = ["h1;h2;h 3"]
        # act
        table = CsvTable(raw_csv)
        # assert
        self.assertEqual("h1", table.caption[0], "caption incorrect")
        self.assertEqual("h2", table.caption[1], "caption incorrect")
        self.assertEqual("h 3", table.caption[2], "caption incorrect")
        self.assertEqual(0, len(table.data_raw), "data is to long")

    def test_init_csv__max_page(self):
        # act
        table = CsvTable(SHORT_CSV, page_length=1)
        # assert
        self.assertEqual(3, table.last_page_index)

    def test_init_empty_csv(self):
        # arrange
        raw_csv = ""
        # act
        table = CsvTable(raw_csv.split("\n"))
        # assert
        self.assertEqual(0, len(table.caption), "caption is to long")
        self.assertEqual(0, len(table.data_raw), "data is to long")

    def test_get_first_page(self):
        table = CsvTable(SHORT_CSV, page_length=1)

        data = table.get_body()

        self.assertEqual(1, len(data), "amount of returned rows is wrong")
        self.assertEqual(3, len(data[0]), "amount of returned columns is wrong")
        self.assertEqual("1", data[0][0], "data is wrong")
        self.assertEqual("ä", data[0][1], "data is wrong")
        self.assertEqual("text space", data[0][2], "data is wrong")

    def test_set_page(self):
        table = CsvTable(SHORT_CSV, page_length=1)

        table.set_page_index(2)

        self.assertEqual(2, table.get_current_page_index())

    def test_set_page__negative_value(self):
        table = CsvTable(SHORT_CSV, page_length=1)

        table.set_page_index(-88)

        self.assertEqual(0, table.get_current_page_index())

    def test_set_page__large_value(self):
        table = CsvTable(SHORT_CSV, page_length=1)

        table.set_page_index(10 ** 100)

        self.assertEqual(3, table.get_current_page_index())

    def test_get_first_visible_index(self):
        table = CsvTable(SHORT_CSV, page_length=1)

        index_0 = table.get_first_visible_item_index()
        table.set_page_index(2)
        index_2 = table.get_first_visible_item_index()

        self.assertEqual(0, index_0)
        self.assertEqual(2, index_2)

    def test_increment_page(self):
        table = CsvTable(SHORT_CSV, page_length=1)

        table.increment_page()
        data = table.get_body()

        self.assertEqual(1, len(data), "amount of returned rows is wrong")
        self.assertEqual(3, len(data[0]), "amount of returned columns is wrong")
        self.assertEqual("2", data[0][0], "data is wrong")
        self.assertEqual("b", data[0][1], "data is wrong")
        self.assertEqual("c", data[0][2], "data is wrong")

    def test_set_to_first_page(self):
        table = CsvTable(SHORT_CSV, page_length=2)
        table.set_page_index(2)

        data = table.set_page_to_first()

        self.assertEqual(2, len(data), "amount of returned rows is wrong")
        self.assertEqual(3, len(data[0]), "amount of returned columns is wrong")
        self.assertEqual("1", data[0][0], "data is wrong")
        self.assertEqual("ä", data[0][1], "data is wrong")
        self.assertEqual("text space", data[0][2], "data is wrong")
        self.assertEqual("2", data[1][0], "data is wrong")
        self.assertEqual("b", data[1][1], "data is wrong")
        self.assertEqual("c", data[1][2], "data is wrong")


    def test_set_to_last_page(self):
        table = CsvTable(SHORT_CSV, page_length=2)
        table.set_page_index(0)

        data = table.set_page_to_last()

        self.assertEqual(2, len(data), "amount of returned rows is wrong")
        self.assertEqual(3, len(data[0]), "amount of returned columns is wrong")
        self.assertEqual("3", data[0][0], "data is wrong")
        self.assertEqual("d", data[0][1], "data is wrong")
        self.assertEqual("e", data[0][2], "data is wrong")
        self.assertEqual("4", data[1][0], "data is wrong")
        self.assertEqual("f", data[1][1], "data is wrong")
        self.assertEqual("g", data[1][2], "data is wrong")



    def test_decrement_page(self):
        table = CsvTable(SHORT_CSV, page_length=1)
        table.set_page_index(1)

        table.decrement_page()
        data = table.get_body()

        self.assertEqual(1, len(data), "amount of returned rows is wrong")
        self.assertEqual(3, len(data[0]), "amount of returned columns is wrong")
        self.assertEqual("1", data[0][0], "data is wrong")
        self.assertEqual("ä", data[0][1], "data is wrong")
        self.assertEqual("text space", data[0][2], "data is wrong")

    def test_first_page(self):
        table = CsvTable(SHORT_CSV, page_length=2)
        table.set_page_index(2)

    def test_load_csv_from_file(self):
        path = "resources/testData.csv"

        table = cvt.load_csv(path)

        self.assertEqual(2, len(table.data_raw))
        self.assertEqual(3, len(table.caption))
        self.assertEqual([["1", "ÄÖß", ""], ["2", "ÄÖß", "B"]], table.get_body(), "wrong data loaded")
        self.assertEqual(["NR", "h1", "h 2"], table.caption, "wrong caption loaded")


if __name__ == '__main__':
    unittest.main()
