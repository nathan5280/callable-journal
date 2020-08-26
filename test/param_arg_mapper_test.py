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
    mapped_args = ParamArgMapper.map(
        unbound_param_arg_map,
        ["p1", "pkw1", "pkw2", "pkw3"],
        {"kw1": "kw1", "kw2": "kw2", "kw3": "kw3"},
    )
    assert actual_args == mapped_args


class BoundMethod:
    def obj_method(self, p1):
        return {
            "self": self,
            "p1": p1,
        }

    @classmethod
    def cls_method(cls, p1):
        return {
            "cls": cls,
            "p1": p1,
        }

    @staticmethod
    def static_method(p1):
        return {
            "p1": p1
        }


def test_bound_obj():
    obj = BoundMethod()
    actual_args = obj.obj_method("p1")
    mapped_args = ParamArgMapper.map(obj.obj_method, ["p1"], {})
    assert actual_args == mapped_args


def test_bound_cls():
    actual_args = BoundMethod.cls_method("p1")
    mapped_args = ParamArgMapper.map(BoundMethod.cls_method, ["p1"], {})
    assert actual_args == mapped_args


def test_bound_static():
    actual_args = BoundMethod.static_method("p1")
    mapped_args = ParamArgMapper.map(BoundMethod.static_method, ["p1"], {})
    assert actual_args == mapped_args
