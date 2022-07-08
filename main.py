import logging
from enum import Enum

import csv_table.csv_table as cvt
import table_renderer.table_renderer as tr
import sys


class UserInput(Enum):
    FIRST_PAGE = 0
    PREVIOUS_PAGE = 1
    NEXT_PAGE = 2
    LAST_PATE = 3
    EXIT = 4
    JUMP = 5
    NOT_PARSED = 6


def render_menu():
    print("F)irst page, P)revious page, N)ext page, L)ast page, E)xit")


def parse_user_input(user_input: str) -> UserInput:
    if user_input in ["F", "f", "First page", "first page"]:
        return UserInput.FIRST_PAGE
    if user_input in ["P", "p", "Previous page", "previous page"]:
        return UserInput.PREVIOUS_PAGE
    if user_input in ["N", "n", "Next page", "next page"]:
        return UserInput.NEXT_PAGE
    if user_input in ["E", "e", "Exit", "exit"]:
        return UserInput.EXIT
    if user_input in ["J", "j", "Jump", "jump"]:
        return UserInput.JUMP
    else:
        return UserInput.NOT_PARSED


def main(path: str, page_length: int):
    table = cvt.load_csv(path)
    table.set_page_length(page_length)
    should_exit = False
    while not should_exit:
        render_table(table)
        render_page_count(table)
        use_input = parse_user_input(
            input("F)irst page, P)revious page, N)ext page, L)ast page, J)ump to page, E)xit \n"))

        handle_user_input(table, use_input)

        should_exit = use_input == UserInput.EXIT


def handle_user_input(table, use_input):
    if use_input == UserInput.FIRST_PAGE:
        table.set_page_to_first()
    if use_input == UserInput.LAST_PATE:
        table.set_page_to_last()
    if use_input == UserInput.NEXT_PAGE:
        table.increment_page()
    if use_input == UserInput.PREVIOUS_PAGE:
        table.decrement_page()
    if use_input == UserInput.JUMP:
        page_nr = input("jump to number: \n")
        try:
            table.set_page_index(int(page_nr))
        except ValueError:
            print(f"{page_nr} is not a number")


def render_table(table):
    output = tr.create_table_markup_str(table.caption, table.get_body())
    print(output)


def render_page_count(table):
    output = tr.create_table_page_count(table.get_current_page_index(), table.get_last_page_index())
    print(output)


def read_data(path: str) -> str:
    f = open(path)
    lines = f.readlines()
    return "".join(lines)


def parse_program_input(argv: list[str]) -> (str, int):
    path = argv[0]
    size = int(argv[1]) if (len(argv)) > 1 else 3
    return path, size


if __name__ == '__main__':
    table_path, page_size = parse_program_input(sys.argv[1:])

    main(table_path, page_size)
