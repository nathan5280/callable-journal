"""Logging formatters to convert Accumulator data to log message format."""
import importlib
import json
import logging
from enum import Enum
from logging import Formatter
from typing import Dict, Type, Optional

from .encoders import ObjectDictEncoder, DictEncoder

logger = logging.getLogger(__name__)

FORMAT_VERSION = "0.2.0"


class FormatMode(Enum):
    """Configure the formatting mode."""

    json = "JSON"
    stringy = "STRINGY"


class JournalFormatter(Formatter):
    def __init__(
        self,
        tag: str,
        format_mode: str,
        *args,
        encoder: Optional[DictEncoder] = None,
        **kwargs
    ):
        self.tag = tag
        format_mode = FormatMode(format_mode)
        if format_mode == FormatMode.json:
            self.formatter = self.format_json
        else:
            self.formatter = self.format_stringy
        self.encoder = encoder if encoder else ObjectDictEncoder
        super().__init__(*args, **kwargs)

    def format_json(self, record) -> Dict:
        msg = {
            "tag": self.tag,
            "version": FORMAT_VERSION,
            **self.encoder.encode(record.journal_content),
        }
        return msg

    def format_stringy(self, record) -> Dict:
        msg = self.format_json(record)
        # Stringy the arguments, results and exceptions.
        for field in ("arguments", "results", "exception"):
            msg[field] = json.dumps(msg[field])
        return msg

    def format(self, record) -> str:
        return json.dumps(self.formatter(record))
