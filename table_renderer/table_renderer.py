from typing import List

from csv_table.csv_table import CsvTable


def _render_header(caption: List[str], padding: list[str]) -> str:
    header = ""
    seperator = ""
    for i, ele in enumerate(caption):
        col_content = ele + padding[i]
        header += col_content + "|"
        seperator += "-" * len(col_content) + "+"
    return header + "\n" + seperator


def _render_data(data: List[List[str]],  _padding: list[list[str]]) -> str:
    table_body = ""
    for i, row in enumerate(data):
        padded_row = ""
        for j, ele in enumerate(row):
            col_content = ele + _padding[i][j]
            padded_row += col_content + "|"
        table_body += padded_row + "\n"
    return table_body


def draw_table(caption: list[str], body: list[list[str]]) -> str:
    caption_padding, column_padding = _calculate_padding_for_table(caption, body)
    table_string = _render_header(caption, caption_padding)
    table_string = table_string + "\n" + _render_data(body, column_padding)
    return table_string


def _calculate_padding_for_table(caption: list[str], body: list[list[str]]) -> tuple[list[str], list[list[str]]]:
    column_width = _calculate_column_widths(caption, body)
    caption_padding = _calculate_row_padding(caption, column_width)
    body_padding = []
    for row in body:
        body_padding.append(_calculate_row_padding(row, column_width))
    return caption_padding, body_padding


def _calculate_row_padding(row: list[str], column_width: list[int]):
    row_padding: list[str] = [""] * len(row)
    for i, ele in enumerate(row):
        row_padding[i] = _calculate_padding(amount=column_width[i] - len(ele))
    return row_padding


def _calculate_column_widths(caption: list[str], body: list[list[str]]):
    if len(caption) == len(body) == 0:
        return []
    if len(body) <= 0:
        return [len(ele) for ele in caption]
    column_widths = [len(ele) for ele in caption] if len(caption) >= len(body[0]) else [len(ele) for ele in body[0]]
    for row in body:
        for i, ele in enumerate(row):
            column_widths[i] = len(ele) if len(ele) > column_widths[i] else column_widths[i]
    return column_widths


def _calculate_padding(amount: int, padding_symbol=" ") -> str:
    return padding_symbol * amount
