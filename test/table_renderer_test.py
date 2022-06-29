import unittest

from csv_table.csv_table import CsvTable
from table_renderer.table_renderer import _calculate_column_widths, _render_header, _render_data, draw_table

SHOWRT_CSV = ["h1;h2;h 3",
              "1;ä;text space",
              "2;b;c",
              "3;d;e"]


class TableRenderer(unittest.TestCase):

    def test_calculate_columns_width(self):
        table = CsvTable(SHOWRT_CSV)

        width = _calculate_column_widths(table.caption, table.get_body())

        self.assertEqual(3, len(width))
        self.assertEqual(2, width[0])
        self.assertEqual(2, width[1])
        self.assertEqual(10, width[2])

    def test_render_header(self):
        table = CsvTable(SHOWRT_CSV)

        table_str = draw_table(table.caption, table.get_body())

        caption = table_str.split("\n")[0]
        seperator = table_str.split("\n")[1]
        self.assertEqual("h1|h2|h 3       |", caption)
        self.assertEqual("--+--+----------+", seperator)

    def test_draw_table(self):
        table = CsvTable(SHOWRT_CSV, page_length=2)

        table_str = draw_table(table.caption, table.get_body())

        self.assertEqual("h1|h2|h 3       |\n" + \
                         "--+--+----------+\n" + \
                         "1 |ä |text space|\n" + \
                         "2 |b |c         |\n", table_str)


if __name__ == '__main__':
    unittest.main()
