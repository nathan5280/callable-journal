import pytest

from callable_journal.exceptions import ResultNameMappingError
from callable_journal.param_arg_mapper import ParamArgMapper


def test_single_name():
    results = ["a"]
    results_map = ParamArgMapper.map_results(results, "a")
    assert results_map == {"a": "a"}


def test_single_result():
    results = "a"
    results_map = ParamArgMapper.map_results(results, "a")
    assert results_map == {"a": "a"}


def test_no_names():
    results = ("a", "b")
    results_map = ParamArgMapper.map_results(results)
    assert results_map == results


def test_all_mapped():
    results = ("a", "b")
    results_map = ParamArgMapper.map_results(results, ["a", "b"])
    assert results_map == {"a": "a", "b": "b"}


def test_some_mapped():
    results = ("a", "b")
    results_map = ParamArgMapper.map_results(results, ["a", ParamArgMapper.IGNORE])
    assert results_map == {"a": "a"}


def test_mismatch():
    results = ("a", "b")
    with pytest.raises(ResultNameMappingError):
        ParamArgMapper.map_results(results, ["a"])
