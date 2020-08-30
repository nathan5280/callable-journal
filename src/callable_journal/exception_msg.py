import traceback

from pydantic.main import BaseModel


class ExceptionMsg(BaseModel):
    type: str
    msg: str
    file: str
    line: str

    @classmethod
    def from_exception(cls, exc: Exception) -> "ExceptionMsg":
        """
        Extract the subset of the exception information that will be saved in the exceptions list.

        :param exc:  Exception to extract
        """
        exc_type = exc.__class__.__name__
        exc_msg = str(exc)
        exc_frame = traceback.extract_tb(exc.__traceback__)[-1]
        exc_file = exc_frame.filename
        exc_line = exc_frame.lineno
        return ExceptionMsg(type=exc_type, msg=exc_msg, file=exc_file, line=exc_line)
