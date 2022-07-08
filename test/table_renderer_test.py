import unittest

from csv_table.csv_table import CsvTable
from table_renderer.table_renderer import _calculate_column_widths, create_table_markup_str, create_table_page_count

SHORT_CSV = [["h1", "h 2", "h 3"],
             ["1", "ä", "text space"],
             ["2", "b", "c"],
             ["3", "d", "e"]]


class TableRenderer(unittest.TestCase):

    def test_calculate_columns_width(self):
        caption, body = SHORT_CSV[0], SHORT_CSV[1:]

        width = _calculate_column_widths(caption, body=body)

        self.assertEqual(3, len(width))
        self.assertEqual(2, width[0])
        self.assertEqual(3, width[1])
        self.assertEqual(10, width[2])

    def test_render_header(self):
        caption, body = SHORT_CSV[0], SHORT_CSV[1:]

        table_str = create_table_markup_str(caption, body)

        caption = table_str.split("\n")[0]
        seperator = table_str.split("\n")[1]
        self.assertEqual("No.|h1|h 2|h 3       |", caption)
        self.assertEqual("---+--+---+----------+", seperator)

    def test_draw_table(self):
        caption, body = SHORT_CSV[0], SHORT_CSV[1:]

        table_str = create_table_markup_str(caption, body)

        self.assertEqual("No.|h1|h 2|h 3       |\n" +
                         "---+--+---+----------+\n" +
                         "1  |1 |ä  |text space|\n" +
                         "2  |2 |b  |c         |\n" +
                         "3  |3 |d  |e         |", table_str)

    def test_draw_table__no_body(self):
        caption = SHORT_CSV[0]

        table_str = create_table_markup_str(caption, [])

        self.assertEqual("No.|h1|h 2|h 3|\n" +
                         "---+--+---+---+\n"
                         , table_str)

    def test_create_table_page_count(self):
        current_page_index = 0
        max_page_index = 100

        page_count_str = create_table_page_count(current_page_index, max_page_index)

        self.assertEqual("Page 1 of 101", page_count_str)


if __name__ == '__main__':
    unittest.main()
