class JournalError(Exception):
    """Base error for all accumulator functionality."""


class ResultNameMappingError(JournalError):
    """Error mapping results."""


class FormatterError(JournalError):
    """Unable to format log message."""


class EncoderError(JournalError):
    """Error dictionary encoding object."""
