from typing import List

from src.callable_journal.param_arg_mapper import ParamArgMapper


def unbound_param_arg_map(p1, /, pkw1, pkw2="dpkw2", *args, kw1, kw2="dkw2", **kwargs):
    return {
        "p1": p1,
        "pkw1": pkw1,
        "pkw2": pkw2,
        "args": args,
        "kw1": kw1,
        "kw2": kw2,
        "kwargs": {"kw3": "kw3"},
    }


def test_unbound():
    actual_args = unbound_param_arg_map(
        "p1", "pkw1", "pkw2", "pkw3", kw1="kw1", kw2="kw2", kw3="kw3"
    )
    mapped_args = ParamArgMapper.map_args(
        unbound_param_arg_map,
        ["p1", "pkw1", "pkw2", "pkw3"],
        {"kw1": "kw1", "kw2": "kw2", "kw3": "kw3"},
    )
    assert actual_args == mapped_args


class BoundMethod:
    def obj_method(self, p1):
        return {
            "p1": p1,
        }

    @classmethod
    def cls_method(cls, p1):
        return {
            "p1": p1,
        }

    @staticmethod
    def static_method(p1):
        return {"p1": p1}


def test_bound_obj():
    obj = BoundMethod()
    actual_args = obj.obj_method("p1")
    mapped_args = ParamArgMapper.map_args(obj.obj_method, ["p1"], {})
    assert actual_args == mapped_args


def test_bound_cls():
    actual_args = BoundMethod.cls_method("p1")
    mapped_args = ParamArgMapper.map_args(BoundMethod.cls_method, ["p1"], {})
    assert actual_args == mapped_args


def test_bound_static():
    actual_args = BoundMethod.static_method("p1")
    mapped_args = ParamArgMapper.map_args(BoundMethod.static_method, ["p1"], {})
    assert actual_args == mapped_args


def copy_fn(a: List[int], b: List[int]):
    pass


def test_copy_all():
    a = [1]
    b = [2]
    mapped_args = ParamArgMapper.map_args(
        copy_fn, args=[a, b], kwargs={}, copy_args=ParamArgMapper.COPY_ALL
    )

    a.append(10)
    b.append(10)

    assert mapped_args["a"] == [1]
    assert mapped_args["b"] == [2]


def test_copy_some():
    a = [1]
    b = [2]
    mapped_args = ParamArgMapper.map_args(copy_fn, args=[a, b], kwargs={}, copy_args=["a"])

    a.append(10)
    b.append(10)

    assert mapped_args["a"] == [1]
    assert mapped_args["b"] == [2, 10]
