"""Dictionary encoders to convert objects to primitive dictionaries."""
import datetime
from abc import abstractmethod, ABC
from pathlib import Path
from typing import Mapping, Iterable, Any, Union

PRIMITIVE = Union[bool, float, int, str, Iterable, Mapping]


class DictEncoder(ABC):
    """Base dictionary encoder with logic to traverse str, Iterable and Mapping."""

    @classmethod
    def _mapping_encode(cls, map_: Mapping[str, Any]) -> Mapping:
        """
        Encode a object that implements the Mapping protocol.
        """
        output = dict()
        for key, value in map_.items():
            output[key] = cls.encode(value)
        return output

    @classmethod
    @abstractmethod
    def encode(cls, obj: Any) -> PRIMITIVE:
        """
        Encode common container primitives

        :param obj: Object to encode
        :return: Primitive encoding of object.
        """
        if isinstance(obj, str):
            return obj
        if isinstance(obj, Mapping):
            return cls._mapping_encode(obj)
        if isinstance(obj, Iterable):
            return [cls.encode(v) for v in obj]
        return obj


class ObjectDictEncoder(DictEncoder):
    """
    Encoder for additional common object types and protocols that have a dict() method.
    """

    @classmethod
    def encode(cls, obj):
        try:
            # Try converting with dict() method first.
            return cls.encode(obj.dict())
        except AttributeError as exc:
            pass
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        if isinstance(obj, Path):
            return str(obj)
        return super().encode(obj)
