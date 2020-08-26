import copy
from inspect import getcallargs
from typing import Iterable, Mapping, Callable, Optional, List, Union, Tuple, Any

from callable_journal.exceptions import ResultNameMappingError


class ParamArgMapper:
    """
    Map the argument values and parameters.
    """

    COPY_ALL = ["*"]
    IGNORE = "_"

    @classmethod
    def map_args(
        cls,
        callable: Callable,
        args: Iterable,
        kwargs: Mapping,
        copy_args: Optional[List[str]] = None,
    ) -> Mapping:
        """
        Map the argument values onto the parameters.  Remove self or cls if they
        exist in the parameters.  Make copies of any arguments that are mutable
        and my be changed by the wrapped callable.

        :param callable: Callable to map the arguments to the parameter signature.
        :param args: List of positional arguments.
        :param kwargs: Dictionary of keyword arguments.
        :param copy_args: List of argument names to make deep copies of.  ParamArgMap.copy_all
            to map all arguments.
        :return: Dictionary of the mapped arguments.
        """
        arg_map = getcallargs(callable, *args, **kwargs)
        for k in ["self", "cls"]:
            try:
                del arg_map[k]
            except KeyError:
                pass

        if copy_args:
            if "*" in copy_args:
                copy_args = arg_map.keys()
            for k in copy_args:
                arg_map[k] = copy.deepcopy(arg_map[k])
        return arg_map

    @classmethod
    def map_results(
        cls,
        results: Union[Any, Tuple[Any]],
        result_names: Optional[Union[str, List[str]]] = None,
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

        # Make sure the results and names are lists.
        results = results if isinstance(results, (list, tuple)) else [results]
        result_names = (
            result_names if isinstance(result_names, (list, tuple)) else [result_names]
        )
        if len(result_names) != len(results):
            raise ResultNameMappingError(
                f"Results names: {len(result_names)}, Results: {len(results)}."
            )

        # Map everything together and throw out the "_".
        mapped_results = {
            n: r for n, r in zip(result_names, results) if n != cls.IGNORE
        }
        return mapped_results
