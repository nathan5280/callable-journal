from pathlib import Path

import pytest

from callable_journal.journal import journal, JournalCtx, SimpleCtx, journal_init

JOURNAL_CTX = JournalCtx(
    context=dict(
        service_ctx=SimpleCtx(name="Test Service", version="0.1.0"),
        implementation_ctx=SimpleCtx(name="Simple Model", version="0.1.0"),
    )
)
JOURNAL_CFG_FPATH = Path(__file__).parent / "journal-cfg.yml"


@journal(objective="int_add", results_names=["sum"])
def int_add(a: int, b: int) -> int:
    return a + b


def test_default():
    journal_init(JOURNAL_CTX, JOURNAL_CFG_FPATH)
    a, b = 10, 20
    c = int_add(a, b)
    assert c == a + b


@journal(objective="int_add", results_names=["div"])
def div_zero():
    x = 1 / 0


def test_exception():
    journal_init(JOURNAL_CTX, JOURNAL_CFG_FPATH)
    with pytest.raises(ZeroDivisionError):
        div_zero()
