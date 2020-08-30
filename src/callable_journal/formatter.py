"""Logging formatters to convert context, arguments and results data to log message format."""
import json
import logging
from enum import Enum
from logging import Formatter, LogRecord
from typing import Dict, Type, Optional

from .encoders import ObjectDictEncoder, DictEncoder

logger = logging.getLogger(__name__)

FORMAT_VERSION = "0.2.0"


class FormatMode(Enum):
    """
    Configure the formatting mode.

    Configure in logging config file.
    formatters:

      journal-json:
        (): callable_journal.formatter.JournalFormatter
        tag: JOURNAL_MSG_JSON
        format_mode: json
    """

    JSON = "json"
    STRINGY = "stringy"


class JournalFormatter(Formatter):
    """
    Formatter to either generate a complete JSON version of the message,
    or a stringy version that keeps arguments and results as JSON strings
    for each argument and result.  This keeps the arguments and results from
    getting exploded in something like BigQuery.

    JSON:
        {
            "tag": "JOURNAL_MSG_JSON",
            "version": "0.2.0",
            "context": {
                "service_ctx": {"name": "Test Service", "version": "0.1.0"},
                "implementation_ctx": {"name": "Base Implementation", "version": "0.1.0"},
            },
            "objective": "formatting",
            "arguments": {"a": 10, "b": 20},
            "results": {"c": 200},
            "exception": null,
        }

    STRINGY:
        {
            "tag": "JOURNAL_MSG_STRINGY",
            "version": "0.2.0",
            "context": {
                "service_ctx": {"name": "Test Service", "version": "0.1.0"},
                "implementation_ctx": {"name": "Base Implementation", "version": "0.1.0"},
            },
            "objective": "formatting",
            "arguments": '{"a": 10, "b": 20}',
            "results": '{"c": 200}',
            "exception": "null",
        }
    """

    def __init__(
        self,
        tag: str,
        format_mode: str,
        *args,
        encoder: Optional[Type[DictEncoder]] = None,
        **kwargs
    ):
        """
        Initialize the formatter with the JSON or STRINGY record formatter.

        :param tag: Tag to add to the message to make it easy to filter in logs.
        :param format_mode: Message format JSON or STRINGY.
        :param args: Positional arguments to pass to the logging formatter base class.
        :param encoder: Optional JSON Encoder to convert the arguments and results to
            JSON serializable primitives.
        :param kwargs: Optional key word arguments to base to the logging formatter
            base class.
        """
        self.tag = tag
        format_mode = FormatMode(format_mode)
        if format_mode == FormatMode.JSON:
            self.formatter = self.format_json
        else:
            self.formatter = self.format_stringy
        self.encoder = encoder if encoder else ObjectDictEncoder
        super().__init__(*args, **kwargs)

    def to_json(self, record: LogRecord) -> Dict:
        """
        Format the message as a pure JSON message.

        :param record: Logging record.
        :return: String representation of the context, arguments and results.
        """

        content = self.encoder.encode(record.journal_content)

        # Remove the context if none was specified.
        if not content["context"]:
            del content["context"]

        # Remove the exception if there is no exception.
        if not content["exception"]:
            del content["exception"]
        else:
            # If there is an exception there are no results.
            del content["results"]

        # record.journal_content is loaded onto the logging record from extras.
        msg = {
            "tag": self.tag,
            "format": FORMAT_VERSION,
            **content,
        }
        return msg

    def format_json(self, record) -> str:
        msg = self.to_json(record)
        return json.dumps(msg)

    def format_stringy(self, record) -> str:
        """
        Format the message as a STRINGY JSON message.

        :param record: Logging record.
        :return: String representation of the context, arguments and results.
        """
        msg = self.to_json(record)
        # Stringy the arguments, results and exceptions.
        for field in ("arguments", "results", "exception"):
            try:
                msg[field] = json.dumps(msg[field])
            except KeyError:
                pass
        return json.dumps(msg)

    def format(self, record) -> str:
        """Format the context, arguments and results in the JSON or STRINGY format."""
        msg = self.formatter(record)
        record.msg = msg
        return super().format(record)
