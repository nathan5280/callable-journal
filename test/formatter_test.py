from logging import Logger

from callable_journal.encoders import ObjectDictEncoder
from callable_journal.formatter import JournalFormatter
from callable_journal.journal import JournalContent

journal_content = JournalContent(
    context=dict(
        service_ctx=dict(name="Test Service", version="0.1.0"),
        implementation_ctx=dict(name="Base Implementation", version="0.1.0"),
    ),
    objective="formatting",
    arguments={"a": 10, "b": 20},
    results={"c": 200},
    exception=None,
)


def test_json_formatter():
    formatter = JournalFormatter(
        tag="JOURNAL_MSG_JSON", format_mode="json", encoder=ObjectDictEncoder
    )
    record = Logger("test_logger").makeRecord(
        "name", 0, "fn", 0, "msg", (), None, extra={"journal_content": journal_content}
    )
    msg = formatter.format(record)
    print(msg)


def test_stringy_formatter():
    formatter = JournalFormatter(
        tag="JOURNAL_MSG_STRINGY", format_mode="stringy", encoder=ObjectDictEncoder
    )
    record = Logger("test_logger").makeRecord(
        "name", 0, "fn", 0, "msg", (), None, extra={"journal_content": journal_content}
    )
    msg = formatter.format(record)
    print(msg)
