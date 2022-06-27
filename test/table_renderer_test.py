import unittest

from csv_table.csv_table import CsvTable
from table_renderer.table_renderer import _calculate_column_width, _render_header, _render_data, draw_table

SHOWRT_CSV = ["h1;h2;h 3",
              "1;ä;text space",
              "2;b;c",
              "3;d;e"]


class TableRenderer(unittest.TestCase):

    def test_calculate_columns_width(self):
        table = CsvTable(SHOWRT_CSV)

        width = _calculate_column_width(table)

        self.assertEqual(3, len(width))
        self.assertEqual(2, width[0])
        self.assertEqual(2, width[1])
        self.assertEqual(10, width[2])

    def test_render_header(self):
        table = CsvTable(SHOWRT_CSV)
        width = _calculate_column_width(table)

        header = _render_header(table.caption, width)

        caption = header.split("\n")[0]
        seperation = header.split("\n")[1]
        self.assertEqual("h1|h2|h 3       |", caption)
        self.assertEqual("--+--+----------+", seperation)

    def test_render_data(self):
        table = CsvTable(SHOWRT_CSV, page_length=1)
        width = _calculate_column_width(table)

        data = _render_data(table.get_data(), width)

        self.assertEqual("1 |ä |text space|\n", data)

    def test_draw_table(self):
        table = CsvTable(SHOWRT_CSV, page_length=2)

        table_render = draw_table(table)

        self.assertEqual("h1|h2|h 3       |\n" + \
                         "--+--+----------+\n" + \
                         "1 |ä |text space|\n" + \
                         "2 |b |c         |\n", table_render)


if __name__ == '__main__':
    unittest.main()
