import math
import os
from typing import List


class CsvTable(object):
    caption: List[str]
    data_raw: List[List[str]]
    _page_index: int
    page_length: int
    last_page: int
    page_length: int

    def __init__(self, csv_raw: List[str], page_length=3):
        self.page_length = page_length
        self._initialize_data(csv_raw)

    def _initialize_data(self, csv_raw: List[str]):
        self.caption = convert_csv_line(csv_raw[0])
        self.data_raw = []
        self._page_index = 0
        for line in csv_raw[1:]:
            if len(line) > 0:
                self.data_raw.append(convert_csv_line(line))
        self.last_page = _calculate_last_page(self.data_raw, self.page_length)

    def get_body(self) -> List[List[str]]:
        start_index = self.get_first_visible_item_index()
        return self.data_raw[start_index: start_index + self.page_length]

    def get_first_visible_item_index(self):
        return self._page_index * self.page_length

    def set_page_index(self, new_page: int):
        if 0 <= new_page <= self.last_page:
            self._page_index = new_page

        if new_page < 0:
            self._page_index = 0

        if new_page > self.last_page:
            self._page_index = self.last_page

    def get_last_page(self):
        return self.last_page

    def get_next_page(self):
        self.increment_page()
        return self.get_body()

    def get_previous_page(self):
        self.decrement_page()
        return self.get_body()

    def get_current_page_index(self):
        return self._page_index

    def increment_page(self):
        self.set_page_index(self._page_index + 1)

    def decrement_page(self):
        self.set_page_index(self._page_index - 1)

    def set_page_length(self, page_length: int):
        self.page_length = page_length
        self.last_page = _calculate_last_page(self.data_raw, page_length)


def convert_csv_line(csv_line: str) -> List[str]:
    seperator = ";"
    if len(csv_line) == 0:
        return []
    return csv_line.split(seperator)


def load_csv(path: str) -> CsvTable:
    lines = _read_data_from_file(path)
    lines = _drop_new_line_symbol(lines)
    lines = _drop_empty_lines(lines)
    return CsvTable(lines)


def _read_data_from_file(path: str):
    with open(path, 'r') as f:
        data = f.readlines()
    return data


def _drop_new_line_symbol(lines):
    return [line.replace("\n", "") for line in lines]


def _drop_empty_lines(lines: list[str]):
    return [line for line in lines if len(line.replace("\n", "")) > 0]


def _calculate_last_page(data_raw: List[List[str]], page_length):
    return math.ceil(len(data_raw) / page_length)
