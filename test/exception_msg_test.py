from callable_journal.exception_msg import ExceptionMsg


def test_exception_msg():
    try:
        1 / 0
    except ZeroDivisionError as exc:
        msg = ExceptionMsg.from_exception(exc)

        assert msg.type == "ZeroDivisionError"
        assert msg.msg == "division by zero"
        assert msg.file.endswith("callable-journal/test/exception_msg_test.py")
        assert msg.line == "6"
