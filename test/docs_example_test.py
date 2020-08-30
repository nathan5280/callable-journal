import copy
import logging
from pathlib import Path
from typing import List, Tuple

from callable_journal import journal, journal_init, DROP_RESULT

logger = logging.getLogger()


def motivation(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied


"""
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "basic",
    "arguments": {"a": 2, "b": [1, 2]},
    "results": [6, [2, 4]],
}
"""


def motivation_with_logging(a: int, b: List[int]) -> Tuple[int, List[int]]:
    b_copy = copy.deepcopy(b)
    multiplied = [a * b_item for b_item in b]
    sum_result = sum(multiplied)
    msg = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "basic",
        "arguments": {"a": a, "b": b_copy},
        "results": [sum_result, multiplied],
    }
    logger.info(msg)
    return sum(multiplied), multiplied


@journal()
def basic(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied


def run_basic():
    journal_init(Path(__file__).parent / "journal-cfg.yml")
    a, b = 2, [1, 2]
    basic(a, b)

    output = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "basic",
        "arguments": {"a": 2, "b": [1, 2]},
        "results": [6, [2, 4]],
    }


def test_basic(capsys):
    run_basic()
    captured = capsys.readouterr()
    # print(captured[0])


@journal(result_names=["total_sum", "multiplied_values"])
def named_results(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied


def run_named_results():
    journal_init(Path(__file__).parent / "journal-cfg.yml")
    a, b = 2, [1, 2]
    named_results(a, b)

    output = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "named_results",
        "arguments": {"a": 2, "b": [1, 2]},
        "results": {"total_sum": 6, "multiplied_values": [2, 4]},
    }


def test_named_results(capsys):
    run_named_results()
    captured = capsys.readouterr()
    # print(captured[0])


@journal(result_names=["total_sum", DROP_RESULT])
def named_ignore_results(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied


def run_named_ignore_results():
    journal_init(Path(__file__).parent / "journal-cfg.yml")
    a, b = 2, [1, 2]
    named_ignore_results(a, b)

    output = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "named_results",
        "arguments": {"a": 2, "b": [1, 2]},
        "results": {"total_sum": 6},
    }


def test_named_ignore_results(capsys):
    run_named_ignore_results()
    captured = capsys.readouterr()
    # print(captured[0])


@journal(copy_args="b")
def copy_args(a: int, b: List[int]) -> Tuple[int, List[int]]:
    # Modify the mutable argument.
    b[0], b[1] = -b[0], -b[1]
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied


def run_copy_args():
    journal_init(Path(__file__).parent / "journal-cfg.yml")
    a, b = 2, [1, 2]
    copy_args(a, b)

    output = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "copy_args",
        "arguments": {"a": 2, "b": [1, 2]},
        "results": [-6, [-2, -4]],
    }


def test_copy_args(capsys):
    run_copy_args()
    captured = capsys.readouterr()
    # print(captured[0])


@journal(drop_args=["b"])
def drop_args(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied


def run_drop_args():
    journal_init(Path(__file__).parent / "journal-cfg.yml")
    a, b = 2, [1, 2]
    drop_args(a, b)

    output = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "drop_args",
        "arguments": {"a": 2},
        "results": [6, [2, 4]],
    }


def test_drop_args(capsys):
    run_drop_args()
    captured = capsys.readouterr()
    # print(captured[0])


@journal()
def add_context(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied


def run_add_context():
    context = {"app_version": "0.1.0"}
    journal_init(Path(__file__).parent / "journal-cfg.yml", context=context)
    a, b = 2, [1, 2]
    add_context(a, b)

    output = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "add_context",
        "context": {"app_version": "0.1.0"},
        "arguments": {"a": 2, "b": [1, 2]},
        "results": [6, [2, 4]],
    }


def test_add_context(capsys):
    run_add_context()
    captured = capsys.readouterr()
    # print(captured[0])


@journal(result_names=["x", "y"])
def exception(a: int, b: List[int]) -> Tuple[int, List[int]]:
    # Raise ZeroDivisionError
    1 / 0


def run_exception():
    journal_init(Path(__file__).parent / "journal-cfg.yml")
    a, b = 2, [1, 2]
    try:
        exception(a, b)
    except ZeroDivisionError:
        pass

    output = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "exception",
        "arguments": {"a": 2, "b": [1, 2]},
        "exception": {
            "type": "ZeroDivisionError",
            "msg": "division by zero",
            "file": "/home/nate/projects/callable-journal/test/docs_example_test.py",
            "line": "170",
        },
    }


def test_exception(capsys):
    run_exception()
    captured = capsys.readouterr()
    # print(captured[0])


@journal()
def log_format(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied


def run_log_format():
    context = {"app_version": "0.1.0"}
    journal_init(Path(__file__).parent / "journal-log-format-cfg.yml", context=context)
    a, b = 2, [1, 2]
    log_format(a, b)

    output = """2020-08-30 15:54:11,813 - journal - INFO - {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "log_format",
        "context": {"app_version": "0.1.0"},
        "arguments": {"a": 2, "b": [1, 2]},
        "results": [6, [2, 4]],
    }"""


def test_log_format(capsys):
    run_log_format()
    captured = capsys.readouterr()
    # print(captured[0])
