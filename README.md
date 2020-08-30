# callable-journal
[![CI](https://github.com/nathan5280/callable-journal/workflows/Test/badge.svg)](https://github.com/nathan5280/callable-journal/actions)
[![coverage](https://codecov.io/gh/nathan5280/callable-journal/develop/graph/badge.svg)](https://codecov.io/gh/nathan5280/callable-journal)
[![pypi](https://img.shields.io/pypi/v/callable-journal.svg)](https://pypi.python.org/pypi/callable-journal)
[![versions](https://img.shields.io/pypi/pyversions/callable-journal.svg)](https://github.com/nathan5280/callable-journal)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/nathan5280/callable-journal/blob/master/LICENSE)

Log message generator for a callable's argument and return values.

## Package Motivation
Do you ever start with something simple like this.
```python
from typing import List, Tuple

def motivation(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied
```
Realize you want logging like this.
```text
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "basic",
    "arguments": {"a": 2, "b": [1, 2]},
    "results": [6, [2, 4]],
}
```
Mess up your function like this.
```python
import copy
import logging
from typing import List, Tuple

logger = logging.getLogger()

def motivation_with_logging(a: int, b: List[int]) -> Tuple[int, List[int]]:
    b_copy = copy.deepcopy(b)
    multiplied = [a * b_item for b_item in b]
    sum_result = sum(multiplied)
    msg = {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "basic",
        "arguments": {"a": a, "b": b_copy},
        "results": [sum_result, multiplied],
    }
    logger.info(msg)
    return sum(multiplied), multiplied
```

Wouldn't it be nice if you could just do this!
```python
from typing import List, Tuple
from callable_journal import journal

@journal()
def basic(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied
```

The callable journal decorator does this and a bit more.  It works great on API endpoints 
where you want a nice record of what the endpoint was called with and what it returned.  By 
connecting into the standard library logging package it is easy to format and direct 
journal message to you favorite sink.  Frequently, this is stdout on a containerized cloud 
infrastructure where some sort of filter takes over from there to route you log messages to
your logging infrastructure. 