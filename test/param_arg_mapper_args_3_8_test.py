# from src.callable_journal.param_arg_mapper import ParamArgMapper
#
#
# def unbound_param_arg_map(p1, /, pkw1, pkw2="dpkw2", *args, kw1, kw2="dkw2", **kwargs):
#     return {
#         "p1": p1,
#         "pkw1": pkw1,
#         "pkw2": pkw2,
#         "args": args,
#         "kw1": kw1,
#         "kw2": kw2,
#         "kwargs": {"kw3": "kw3"},
#     }
#
#
# def test_unbound():
#     actual_args = unbound_param_arg_map(
#         "p1", "pkw1", "pkw2", "pkw3", kw1="kw1", kw2="kw2", kw3="kw3"
#     )
#     mapped_args = ParamArgMapper.map_args(
#         unbound_param_arg_map,
#         ["p1", "pkw1", "pkw2", "pkw3"],
#         {"kw1": "kw1", "kw2": "kw2", "kw3": "kw3"},
#     )
#     assert actual_args == mapped_args
