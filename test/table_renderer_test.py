import unittest

from csv_table.csv_table import CsvTable
from table_renderer.table_renderer import _calculate_column_widths, _render_header, _render_data, draw_table


SHORT_CSV = [["h1", "h2", "h 3"],
             ["1", "ä", "text space"],
             ["2", "b", "c"],
             ["3", "d", "e"]]


class TableRenderer(unittest.TestCase):

    def test_calculate_columns_width(self):
        caption, body = SHORT_CSV[0], SHORT_CSV[1:]

        width = _calculate_column_widths(caption, body=body)

        self.assertEqual(3, len(width))
        self.assertEqual(2, width[0])
        self.assertEqual(2, width[1])
        self.assertEqual(10, width[2])

    def test_render_header(self):
        caption, body = SHORT_CSV[0], SHORT_CSV[1:]

        table_str = draw_table(caption, body)

        caption = table_str.split("\n")[0]
        seperator = table_str.split("\n")[1]
        self.assertEqual("h1|h2|h 3       |", caption)
        self.assertEqual("--+--+----------+", seperator)

    def test_draw_table(self):
        caption, body = SHORT_CSV[0], SHORT_CSV[1:]

        table_str = draw_table(caption, body)

        self.assertEqual("h1|h2|h 3       |\n" +
                         "--+--+----------+\n" +
                         "1 |ä |text space|\n" +
                         "2 |b |c         |\n" +
                         "3 |d |e         |\n", table_str)


if __name__ == '__main__':
    unittest.main()
