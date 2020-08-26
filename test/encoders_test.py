import datetime
from pathlib import Path
from typing import Union, Iterable, Mapping

from pydantic import BaseModel

from callable_journal.encoders import ObjectDictEncoder

PRIMITIVE = Union[
    bool, float, int, str, Iterable, Mapping, datetime.datetime, datetime.date, datetime.time,
]


def test_primitive_dict():
    data = {"a": 1, "d": datetime.date(2020, 1, 1), "s": "string"}
    encoded = ObjectDictEncoder.encode(data)
    expected = {"a": 1, "d": "2020-01-01", "s": "string"}
    assert encoded == expected


class DateTimeHolderBaseModel(BaseModel):
    d: datetime.date


def test_object_base_model():
    d = datetime.date(2020, 1, 1)
    obj = DateTimeHolderBaseModel(d=d)
    encoded = ObjectDictEncoder.encode(obj)
    expected = {"d": "2020-01-01"}
    assert encoded == expected


def test_list_object():
    d = datetime.date(2020, 1, 1)
    expected = []
    obj = []
    for _ in range(2):
        obj.append(DateTimeHolderBaseModel(d=d))
        expected.append({"d": "2020-01-01"})
    encoded = ObjectDictEncoder.encode(obj)
    assert encoded == expected


def test_dict_object():
    d = datetime.date(2020, 1, 1)
    expected = {}
    obj = {}
    for i in range(2):
        obj[i] = DateTimeHolderBaseModel(d=d)
        expected[i] = {"d": "2020-01-01"}
    encoded = ObjectDictEncoder.encode(obj)
    assert encoded == expected


def test_path_object():
    p = Path("/tmp")
    obj = {"p": p}
    expected = {"p": "/tmp"}
    encoded = ObjectDictEncoder.encode(obj)
    assert encoded == expected
