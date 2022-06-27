from typing import List

from csv_table.csv_table import CsvTable


def _render_header(caption: List[str], column_width: List[int]) -> str:
    header = ""
    seperator = ""
    for i, ele in enumerate(caption):
        padding = _calculate_padding(column_width[i] - len(ele))
        header += ele + padding + "|"
        seperator += "-" * column_width[i] + "+"
    return header + "\n" + seperator


def _render_data(data: List[List[str]], column_width: List[int]) -> str:
    table_body = ""
    for row in data:
        padded_row = ""
        for i, ele in enumerate(row):
            padding = _calculate_padding(column_width[i] - len(ele))
            padded_row += ele + padding + "|"
        table_body += padded_row + "\n"
    return table_body


def draw_table(table: CsvTable) -> str:
    column_width = _calculate_column_width(table)
    table_string = _render_header(table.caption, column_width)
    table_string = table_string + "\n" + _render_data(table.get_data(), column_width)
    return table_string


def _calculate_column_width(table: CsvTable):
    column_widths = [len(ele) for ele in table.caption]
    for row in table.data_raw:
        for i, ele in enumerate(row):
            column_widths[i] = len(ele) if len(ele) > column_widths[i] else column_widths[i]
    return column_widths


def _calculate_padding(amount: int, padding_symbol=" ") -> str:
    return padding_symbol * amount
