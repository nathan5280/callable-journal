import json
from pathlib import Path

import pytest
from ndl_tools import Differ, PathNormalizer, EndsWithSelector

from callable_journal.journal import journal, journal_init

context = dict(
    context=dict(
        service_ctx=dict(name="Test Service", version="0.1.0"),
        implementation_ctx=dict(name="Simple Model", version="0.1.0"),
    )
)
JOURNAL_CFG_FPATH = Path(__file__).parent / "journal-cfg.yml"


@journal(result_names=["sum"])
def int_add(a: int, b: int) -> int:
    return a + b


def test_default(capsys):
    journal_init(JOURNAL_CFG_FPATH, context)
    a, b = 10, 20
    c = int_add(a, b)
    assert c == a + b
    captured = capsys.readouterr()
    msg = captured[0]

    expected = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "int_add",
        "context": {
            "service_ctx": {"name": "Test Service", "version": "0.1.0"},
            "implementation_ctx": {"name": "Simple Model", "version": "0.1.0"},
        },
        "arguments": {"a": 10, "b": 20},
        "results": {"sum": 30},
    }

    msg = json.loads(msg)
    result = Differ().diff(expected, msg)
    if not result:
        print(result.support)
        assert False


@journal(objective="int_add_objective", result_names=["div"])
def div_zero():
    x = 1 / 0


def test_exception(capsys):
    journal_init(JOURNAL_CFG_FPATH, context)
    with pytest.raises(ZeroDivisionError):
        div_zero()

    captured = capsys.readouterr()
    # Clean up the output as logging subsystem adds exception information to the output.
    msg = captured[0].split("\n")[0]

    expected = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "int_add_objective",
        "context": {
            "service_ctx": {"name": "Test Service", "version": "0.1.0"},
            "implementation_ctx": {"name": "Simple Model", "version": "0.1.0"},
        },
        "arguments": {},
        "exception": {
            "type": "ZeroDivisionError",
            "msg": "division by zero",
            "file": "/home/some_user/projects/callable-journal/test/journal_test.py",
            "line": "52",
        },
    }

    msg = json.loads(msg)
    selector = EndsWithSelector("exception/file")
    normalizer = PathNormalizer(num_components=3, selectors=selector)
    result = Differ().diff(expected, msg, normalizers=normalizer, max_col_width=50)
    print(result.support)
    if not result:
        print(result.support)
        assert False
