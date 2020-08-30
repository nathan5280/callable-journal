import copy
from inspect import getcallargs
from typing import Iterable, Mapping, Callable, Optional, List, Union, Tuple, Any

from callable_journal.exceptions import ResultNameMappingError


class CopyAllArgs:
    """Sentry class to indicate that all arguments should be copied."""
    pass


COPY_ALL_ARGS = CopyAllArgs()


class DropResult:
    """Sentry class to indicate that a result should be dropped."""
    pass


DROP_RESULT = DropResult()


class ParamArgMapper:
    """
    Map the argument values and parameters.
    """

    @staticmethod
    def to_iterable(value: Optional[Union[str, List[str]]] = None) -> List[str]:
        """Convert argument to a iterable if it isn't already iterable list of names."""
        if not value:
            return list()
        value = value if isinstance(value, (list, tuple)) else [value]
        return value

    @classmethod
    def map_args(
        cls,
        callable: Callable,
        args: Iterable,
        kwargs: Mapping,
        copy_args: Optional[Union[str, List[str], CopyAllArgs]] = None,
        drop_args: Optional[Union[str, List[str]]] = None,
    ) -> Mapping:
        """
        Map the argument values onto the parameters.  Remove self or cls if they
        exist in the parameters.  Make copies of any arguments that are mutable
        and my be changed by the wrapped callable.

        :param callable: Callable to map the arguments to the parameter signature.
        :param args: List of positional arguments.
        :param kwargs: Dictionary of keyword arguments.
        :param copy_args: Name or list of names of arguments that should be copied to prevent
            mutation by the callable.
        :param drop_args: Name or list of names of arguments that should be dropped from the message.  Useful for
            large objects or arguments that contain sensitive data.
        :return: Dictionary of the mapped arguments.
        """
        copy_args = cls.to_iterable(copy_args)
        drop_args = cls.to_iterable(drop_args)
        arg_map = getcallargs(callable, *args, **kwargs)
        for k in ["self", "cls"]:
            try:
                del arg_map[k]
            except KeyError:
                pass

        if copy_args:
            if copy_args == [COPY_ALL_ARGS]:
                copy_args = arg_map.keys()
            for k in copy_args:
                arg_map[k] = copy.deepcopy(arg_map[k])

        for drop_arg in drop_args:
            del arg_map[drop_arg]

        return arg_map

    @classmethod
    def map_results(
        cls,
        results: Union[Any, Tuple[Any]],
        result_names: Optional[Union[str, List[str], DropResult]] = None,
    ) -> Mapping:
        """
        Map results based on list of names.  Result names "_" are ignored and not
        mapped into the results dictionary.

        :param results:  Result values to map.
        :param result_names: Name or list of result names.
        :return: Dictionary of named results.
        """
        if not result_names:
            return results

        # Make sure the results and names are iterable.
        results = results if isinstance(results, (list, tuple)) else [results]
        result_names = cls.to_iterable(result_names)
        if len(result_names) != len(results):
            raise ResultNameMappingError(
                f"Results names: {len(result_names)}, Results: {len(results)}."
            )

        # Map everything together and throw out the "_".
        mapped_results = {n: r for n, r in zip(result_names, results) if n != DROP_RESULT}
        return mapped_results
