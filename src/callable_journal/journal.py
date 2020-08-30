"""
Public interface to the journal decorator.
"""
import functools
import logging.config
from pathlib import Path
from typing import Any, List, Optional, Mapping, Union

import yaml
from pydantic.main import BaseModel
from toolz import curry

from callable_journal.exception_msg import ExceptionMsg
from callable_journal.param_arg_mapper import ParamArgMapper

logger = logging.getLogger("journal")


ANY_JSON_SERIALIZABLE = Any


class JournalContent(BaseModel):
    """
    Collection of context, arguments and results to be formatted into the message.
    """

    objective: str
    context: Optional[ANY_JSON_SERIALIZABLE] = None
    arguments: Optional[Mapping[str, Any]] = None
    results: Optional[Mapping[str, Any]] = None
    exception: Optional[ExceptionMsg] = None


# Context of prepended to all messages.   Normally some version information.
ctx = None


def journal_init(logging_cfg_fpath: Path, context: Optional[ANY_JSON_SERIALIZABLE] = None):
    """
    Initialize the journalling subsystem.

    :param context: Context to prepend to all messages.
    :param logging_cfg_fpath: Path to logging configuration file.
    """
    global ctx
    ctx = context

    with logging_cfg_fpath.open("rt") as fp:
        logging_cfg = yaml.safe_load(fp)

    logging.config.dictConfig(logging_cfg)


@curry
def journal(
    callable,
    *,
    objective: Optional[str] = None,
    result_names: Optional[Union[str, List[str]]] = None,
    copy_args: Optional[Union[str, List[str]]] = None,
    drop_args: Optional[Union[str, List[str]]] = None
):
    """
    Callable journal decorator.   Decorating a callable will generate a log message containing
    the journalling context, callable arguments and callable results.  Results can be named by
    passing a list of positional names for each of the results.

    :param callable: Callable being decorated.
    :param objective: Object of the callable used to identify what callable a message applies to.
        Defaults to the callable name if not provided.
    :param result_names: Names for the results.  Names are mapped positionally.  Results
        can be skipped by passing  ParamArgMapper.DROP_RESULT as a result name.
    :param copy_args: Name or list of names of arguments that should be copied to prevent
        mutation by the callable.
    :param drop_args: Name or list of names of arguments that should be dropped from the message.  Useful for
        large objects or arguments that contain sensitive data.

    :return: Callable wrapping the callable.
    """

    @functools.wraps(callable)
    def wrapper(*args, **kwargs):
        objective_name = objective or callable.__name__
        args_data = ParamArgMapper.map_args(
            callable, args, kwargs, copy_args=copy_args, drop_args=drop_args
        )
        msg = JournalContent(
            context=ctx,
            objective=objective_name,
            arguments=args_data,
        )
        try:
            results = callable(*args, **kwargs)
            results_data = ParamArgMapper.map_results(
                results, result_names=result_names
            )
            msg.results = results_data
            logger.info(msg="", extra={"journal_content": msg})
            return results
        except Exception as exc:
            msg.exception = ExceptionMsg.from_exception(exc)
            logger.exception(msg="", extra={"journal_content": msg})
            raise

    return wrapper
