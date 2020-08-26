from logging import LogRecord, Logger

from callable_journal.encoders import ObjectDictEncoder
from callable_journal.formatter import JournalFormatter
from callable_journal.journal import JournalContent, SimpleCtx

journal_content = JournalContent(
    context=dict(
        service_ctx=SimpleCtx(name="Test Service", version="0.1.0"),
        implementation_ctx=SimpleCtx(name="Base Implementation", version="0.1.0"),
    ),
    objective="formatting",
    arguments={"a": 10, "b": 20},
    results={"c": 200},
    exception=None,
)


def test_json_formatter():
    formatter = JournalFormatter(
        tag="JOURNAL_MSG", format_mode="JSON", encoder=ObjectDictEncoder
    )
    record = Logger("test_logger").makeRecord(
        "name", 0, "fn", 0, "msg", [], None, extra={"journal_content": journal_content}
    )
    msg = formatter.format(record)
    print(msg)


def test_stringy_formatter():
    formatter = JournalFormatter(
        tag="JOURNAL_MSG", format_mode="STRINGY", encoder=ObjectDictEncoder
    )
    record = Logger("test_logger").makeRecord(
        "name", 0, "fn", 0, "msg", [], None, extra={"journal_content": journal_content}
    )
    msg = formatter.format(record)
    print(msg)
