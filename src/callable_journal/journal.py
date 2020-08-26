import functools
import logging.config
import traceback
from pathlib import Path
from typing import Any, List, Optional, Mapping, Union, Dict

import yaml
from pydantic.main import BaseModel
from toolz import curry

from callable_journal.param_arg_mapper import ParamArgMapper

logger = logging.getLogger("journal")


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


class SimpleCtx(BaseModel):
    name: str
    version: str


class JournalContent(BaseModel):
    context: Dict[str, SimpleCtx]
    objective: str
    arguments: Mapping[str, Any]
    results: Optional[Mapping[str, Any]] = None
    exception: Optional[ExceptionMsg] = None


class JournalCtx(BaseModel):
    context: Dict[str, SimpleCtx]


ctx = None


def journal_init(journal_ctx: JournalCtx, logging_cfg_fpath: Path):
    global ctx
    ctx = journal_ctx

    with logging_cfg_fpath.open("rt") as fp:
        logging_cfg = yaml.safe_load(fp)

    logging.config.dictConfig(logging_cfg)


@curry
def journal(
    func,
    *,
    objective: str,
    results_names: Optional[Union[str, List[str]]] = None,
    copy_args: Optional[List[str]] = None
):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_data = ParamArgMapper.map_args(func, args, kwargs, copy_args=copy_args)
        msg = JournalContent(
            context=ctx.context,
            objective=objective,
            arguments=args_data,
        )
        try:
            results = func(*args, **kwargs)
            results_data = ParamArgMapper.map_results(
                results, result_names=results_names
            )
            msg.results = results_data
            logger.info(msg="", extra={"journal_content": msg})
            return results
        except Exception as exc:
            msg.exception = ExceptionMsg.from_exception(exc)
            logger.exception(msg="", extra={"journal_content": msg})
            raise

    return wrapper
