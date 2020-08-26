from inspect import getcallargs
from typing import Iterable, Mapping, Callable, Optional


class ParamArgMapper:
    @classmethod
    def map(
        cls, callable: Callable, args: Iterable, kwargs: Mapping, copy: Optional[bool] = False
    ) -> Mapping:
        return getcallargs(callable, *args, **kwargs)
