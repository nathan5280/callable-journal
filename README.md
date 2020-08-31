# callable-journal
[![CI](https://github.com/nathan5280/callable-journal/workflows/Test/badge.svg)](https://github.com/nathan5280/callable-journal/actions)
[![coverage](https://codecov.io/gh/nathan5280/callable-journal/master/graph/badge.svg)](https://codecov.io/gh/nathan5280/callable-journal)
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
```json
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "basic",
    "arguments": {"a": 2, "b": [1, 2]},
    "results": [6, [2, 4]]
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
        "results": [sum_result, multiplied]
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
journal message to your favorite sink.  

## Naming Results
If you have a callable that returns multiple values, you can assign names to them using
the `result_names` parameter.

```python
from typing import List, Tuple
from callable_journal import journal

@journal(result_names=["total_sum", "multiplied_values"])
def named_results(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied
```

Log Message:
```json
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "named_results",
    "arguments": {"a": 2, "b": [1, 2]},
    "results": {"total_sum": 6, "multiplied_values": [2, 4]}
}
```

### Dropping Results
If the result contains sensitive data or not of interest it can be dropped using `DROP_RESULT`.

```python
from typing import List, Tuple
from callable_journal import journal, DROP_RESULT

@journal(result_names=["total_sum", DROP_RESULT])
def named_ignore_results(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied
```

Log Message:
```json
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "named_results",
    "arguments": {"a": 2, "b": [1, 2]},
    "results": {"total_sum": 6}
}
```

### Copying Arguments
Sometimes a callable mutates its arguments for good or bad reasons.  If the arguments
aren't copied the mutated version will show up in the log message.  Because copying some
arguments is costly, you can specify which arguments to copy with the `copy_args` parameter.

```python
from typing import List, Tuple
from callable_journal import journal

@journal(copy_args="b")
def copy_args(a: int, b: List[int]) -> Tuple[int, List[int]]:
    # Modify the mutable argument.
    b[0], b[1] = -b[0], -b[1]
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied
```

Log Message with the correct mutable argument:
```json
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "copy_args",
    "arguments": {"a": 2, "b": [1, 2]},
    "results": [-6, [-2, -4]]
}
```

You can use the `COPY_ALL` value for the `copy_args` parameter to copy all the args.

### Dropping Arguments
In the same way that sometimes you want to drop results you may want to drop arguments.
This is accomplished with the `drop_args` parameter.

```python
from typing import List, Tuple
from callable_journal import journal

@journal(drop_args=["b"])
def drop_args(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied
```

Log Message:
```json
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "drop_args",
    "arguments": {"a": 2},
    "results": [6, [2, 4]]
}
```

### Context
If you want information about the context of the application the log message was run in you
can add context information to the log messages.

```python
from pathlib import Path
from typing import List, Tuple
from callable_journal import journal, journal_init

@journal()
def add_context(a: int, b: List[int]) -> Tuple[int, List[int]]:
    multiplied = [a * b_item for b_item in b]
    return sum(multiplied), multiplied


def run_add_context():
    context = {"app_version": "0.1.0"}
    journal_init(Path(__file__).parent / "journal-cfg.yml", context=context)
    a, b = 2, [1, 2]
    add_context(a, b)
```

```json
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "add_context",
    "context": {"app_version": "0.1.0"},
    "arguments": {"a": 2, "b": [1, 2]},
    "results": [6, [2, 4]]
}
```

### Exceptions
Uncaught exceptions are going to be raised and reported, but it is nice to get some amount
of information about the exception in the log message.  An example is shown here.

```json
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "exception",
    "arguments": {"a": 2, "b": [1, 2]},
    "exception": {
        "type": "ZeroDivisionError",
        "msg": "division by zero",
        "file": "/home/some_user/projects/callable-journal/test/docs_example_test.py",
        "line": "170"
    }
}
```

### Logging Configuration
Logging configuration uses the standard library logging configuration.  Here is an example
that configures two loggers. One the generates pure JSON log messages and one that generates
STRINGY log messages. 

```yaml
---
version: 1
disable_existing_loggers: false
formatters:
  journal-json:
    (): callable_journal.formatter.JournalFormatter
    tag: JOURNAL_MSG_JSON
    format_mode: json
  journal-stringy:
    (): callable_journal.formatter.JournalFormatter
    tag: JOURNAL_MSG_STRINGY
    format_mode: stringy
handlers:
  journal-json-console:
    class: logging.StreamHandler
    level: INFO
    formatter: journal-json
    stream: ext://sys.stdout
  journal-stringy-console:
    class: logging.StreamHandler
    level: INFO
    formatter: journal-stringy
    stream: ext://sys.stdout
loggers:
  journal:
    level: INFO
    handlers:
      - journal-json-console
      - journal-stringy-console
    propagate: false
...
```

JSON Log Message:
```json
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "log_format",
    "context": {"app_version": "0.1.0"},
    "arguments": {"a": 2, "b": [1, 2]},
    "results": [6, [2, 4]],
}
```

STRINGY Log Message:
```json
{
    "tag": "JOURNAL_MSG_JSON",
    "format": "0.2.0",
    "objective": "log_format",
    "context": "{\"app_version\": \"0.1.0\"}",
    "arguments": "{\"a\": 2, \"b\": [1, 2]}",
    "results": "[6, [2, 4]]"
}
```

Why the STRINGY format?  If you have many different messages all flowing through to something
like BigQuery it is nice to keep BigQuery from exploding the nested JSON in the context, 
arguments and results.   It could wind up with a large number of confusingly named columns.
By using the STRINGY format all the arguments from different journals go into one column
and you can use the JSON extract functionality of BigQuery to get what you want out of that
column's JSON.

### Logging Format
The loggers are derived from `logging.Formatter` and pass any unused `args` and `kwargs` on to
the default Formatter.  By adding a `format` entry to the configuration you can add all
the other log message content you are used to seeing by default.

Configuration:
```yaml
---
version: 1
disable_existing_loggers: false
formatters:
  journal-json:
    (): callable_journal.formatter.JournalFormatter
    tag: JOURNAL_MSG_JSON
    format_mode: json
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  journal-json-console:
    class: logging.StreamHandler
    level: INFO
    formatter: journal-json
    stream: ext://sys.stdout
loggers:
  journal:
    level: INFO
    handlers:
      - journal-json-console
    propagate: false
...
```

Log Message:
```text
2020-08-30 15:54:11,813 - journal - INFO - {
        "tag": "JOURNAL_MSG_JSON",
        "format": "0.2.0",
        "objective": "log_format",
        "context": {"app_version": "0.1.0"},
        "arguments": {"a": 2, "b": [1, 2]},
        "results": [6, [2, 4]],
    }
```

