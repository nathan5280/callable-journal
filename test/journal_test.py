from pathlib import Path

import pytest

from callable_journal.journal import journal, journal_init

context = dict(
    service_ctx=dict(name="Test Service", version="0.1.0"),
    implementation_ctx=dict(name="Simple Model", version="0.1.0"),
)
JOURNAL_CFG_FPATH = Path(__file__).parent / "journal-cfg.yml"


@journal(results_names=["sum"])
def int_add(a: int, b: int) -> int:
    return a + b


def test_default():
    journal_init(JOURNAL_CFG_FPATH, context)
    a, b = 10, 20
    c = int_add(a, b)
    assert c == a + b


@journal(objective="int_add_objective", results_names=["div"])
def div_zero():
    x = 1 / 0


def test_exception():
    journal_init(JOURNAL_CFG_FPATH, context)
    with pytest.raises(ZeroDivisionError):
        div_zero()
