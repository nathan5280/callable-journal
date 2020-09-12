import json
from logging import Logger

from ndl_tools import Differ

from callable_journal.encoders import ObjectDictEncoder
from callable_journal.formatter import JournalFormatter
from callable_journal.journal import JournalContent

journal_content = JournalContent(
    context=dict(
        context=dict(
            service_ctx=dict(name="Test Service", version="0.1.0"),
            implementation_ctx=dict(name="Base Implementation", version="0.1.0"),
        )
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

    expected = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "formatting",
        "context": {
            "service_ctx": {"name": "Test Service", "version": "0.1.0"},
            "implementation_ctx": {"name": "Base Implementation", "version": "0.1.0"},
        },
        "arguments": {"a": 10, "b": 20},
        "results": {"c": 200},
    }

    msg = json.loads(msg)
    result = Differ().diff(expected, msg)
    if not result:
        print(result.support)
        assert False


def test_stringy_formatter():
    formatter = JournalFormatter(
        tag="JOURNAL_MSG_STRINGY", format_mode="stringy", encoder=ObjectDictEncoder
    )
    record = Logger("test_logger").makeRecord(
        "name", 0, "fn", 0, "msg", (), None, extra={"journal_content": journal_content}
    )
    msg = formatter.format(record)

    expected = {
        "tag": "JOURNAL_MSG_STRINGY",
        "format": "0.2.0",
        "objective": "formatting",
        "context": {
            "service_ctx": {"name": "Test Service", "version": "0.1.0"},
            "implementation_ctx": {"name": "Base Implementation", "version": "0.1.0"},
        },
        "arguments": '{"a": 10, "b": 20}',
        "results": '{"c": 200}',
    }

    msg = json.loads(msg)
    result = Differ().diff(expected, msg)
    if not result:
        print(result.support)
        assert False


def test_expanded_context():
    formatter = JournalFormatter(
        tag="JOURNAL_MSG_JSON", format_mode="json", encoder=ObjectDictEncoder
    )
    # Unnest the context to see that it is expanded.
    journal_content.context = journal_content.context["context"]
    record = Logger("test_logger").makeRecord(
        "name", 0, "fn", 0, "msg", (), None, extra={"journal_content": journal_content}
    )

    msg = formatter.format(record)

    expected = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "formatting",
        "service_ctx": {"name": "Test Service", "version": "0.1.0"},
        "implementation_ctx": {"name": "Base Implementation", "version": "0.1.0"},
        "arguments": {"a": 10, "b": 20},
        "results": {"c": 200},
    }

    msg = json.loads(msg)
    result = Differ().diff(expected, msg)
    if not result:
        print(result.support)
        assert False
