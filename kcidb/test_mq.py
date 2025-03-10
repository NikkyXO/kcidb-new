"""kcdib.mq module tests"""

import re
import textwrap
import json
import kcidb
from kcidb.unittest import assert_executes


def test_io_publisher_main_init():
    """Check kcidb-mq-io-publisher init works"""
    argv = ["kcidb.mq.io_publisher_main",
            "-p", "project", "-t", "topic", "init"]
    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        publisher = Mock()
        publisher.init = Mock()
        with patch("kcidb.mq.IOPublisher", return_value=publisher) as \
                Publisher:
            status = function()
        Publisher.assert_called_once_with("project", "topic")
        publisher.init.assert_called_once()
        return status
    """)
    assert_executes("", *argv, driver_source=driver_source)


def test_io_publisher_main_cleanup():
    """Check kcidb-mq-io-publisher cleanup works"""
    argv = ["kcidb.mq.io_publisher_main",
            "-p", "project", "-t", "topic", "cleanup"]
    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        publisher = Mock()
        publisher.cleanup = Mock()
        with patch("kcidb.mq.IOPublisher", return_value=publisher) as \
                Publisher:
            status = function()
        Publisher.assert_called_once_with("project", "topic")
        publisher.cleanup.assert_called_once()
        return status
    """)
    assert_executes("", *argv, driver_source=driver_source)


def test_io_publisher_main_publish():
    """Check kcidb-mq-io-publisher publish works"""
    argv = ["kcidb.mq.io_publisher_main",
            "-p", "project", "-t", "topic", "publish"]
    empty = kcidb.io.SCHEMA.new()

    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        import json

        publisher = Mock()
        publisher.init = Mock()
        publisher.schema = kcidb.io.SCHEMA
        def publish_iter(data_iter, done_cb=None):
            for data in data_iter:
                done_cb(json.dumps(data))
        publisher.publish_iter = publish_iter

        with patch("kcidb.mq.IOPublisher", return_value=publisher) as \
                Publisher:
            status = function()
        Publisher.assert_called_once_with("project", "topic")
        return status
    """)

    assert_executes('{', *argv, driver_source=driver_source,
                    status=1, stderr_re=".*JSONParseError.*")
    assert_executes('{}', *argv, driver_source=driver_source,
                    status=1, stderr_re=".*ValidationError.*")

    assert_executes(json.dumps(empty), *argv,
                    driver_source=driver_source,
                    stdout_re=re.escape(json.dumps(empty) + "\n"))

    assert_executes(json.dumps(empty) + json.dumps(empty), *argv,
                    driver_source=driver_source,
                    stdout_re=re.escape(json.dumps(empty) + "\n" +
                                        json.dumps(empty) + "\n"))


def test_io_subscriber_main_init():
    """Check kcidb-mq-io-subscriber init works"""
    argv = ["kcidb.mq.io_subscriber_main",
            "-p", "project", "-t", "topic", "-s", "subscription", "init"]
    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        subscriber = Mock()
        subscriber.init = Mock()
        with patch("kcidb.mq.IOSubscriber", return_value=subscriber) as \
                Subscriber:
            status = function()
        Subscriber.assert_called_once_with("project", "topic",
                                           "subscription")
        subscriber.init.assert_called_once()
        return status
    """)
    assert_executes("", *argv, driver_source=driver_source)


def test_io_subscriber_main_cleanup():
    """Check kcidb-mq-io-subscriber cleanup works"""
    argv = ["kcidb.mq.io_subscriber_main",
            "-p", "project", "-t", "topic", "-s", "subscription",
            "cleanup"]
    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        subscriber = Mock()
        subscriber.cleanup = Mock()
        with patch("kcidb.mq.IOSubscriber", return_value=subscriber) as \
                Subscriber:
            status = function()
        Subscriber.assert_called_once_with("project", "topic",
                                           "subscription")
        subscriber.cleanup.assert_called_once()
        return status
    """)
    assert_executes("", *argv, driver_source=driver_source)


def test_io_subscriber_main_pull():
    """Check kcidb-mq-io-subscriber pull works"""
    argv = ["kcidb.mq.io_subscriber_main",
            "-p", "project", "-t", "topic", "-s", "subscription",
            "pull", "--timeout", "123", "--indent=0"]
    empty = kcidb.io.SCHEMA.new()
    driver_source = textwrap.dedent(f"""
        from unittest.mock import patch, Mock
        subscriber = Mock()
        subscriber.pull_iter = \
            Mock(return_value=[("ID", {repr(empty)})])
        subscriber.ack = Mock()
        with patch("kcidb.mq.IOSubscriber", return_value=subscriber) as \
                Subscriber:
            status = function()
        Subscriber.assert_called_once_with("project", "topic",
                                           "subscription")
        subscriber.pull_iter.assert_called_once_with(1, timeout=123)
        subscriber.ack.assert_called_once_with("ID")
        return status
    """)
    assert_executes("", *argv, driver_source=driver_source,
                    stdout_re=re.escape(json.dumps(empty) + "\n"))


def test_pattern_publisher_main_init():
    """Check kcidb-mq-pattern-publisher init works"""
    argv = ["kcidb.mq.pattern_publisher_main",
            "-p", "project", "-t", "topic", "init"]
    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        publisher = Mock()
        publisher.init = Mock()
        with patch("kcidb.mq.ORMPatternPublisher",
                   return_value=publisher) as Publisher:
            status = function()
        Publisher.assert_called_once_with("project", "topic")
        publisher.init.assert_called_once()
        return status
    """)
    assert_executes("", *argv, driver_source=driver_source)


def test_pattern_publisher_main_cleanup():
    """Check kcidb-mq-pattern-publisher cleanup works"""
    argv = ["kcidb.mq.pattern_publisher_main",
            "-p", "project", "-t", "topic", "cleanup"]
    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        publisher = Mock()
        publisher.cleanup = Mock()
        with patch("kcidb.mq.ORMPatternPublisher",
                   return_value=publisher) as Publisher:
            status = function()
        Publisher.assert_called_once_with("project", "topic")
        publisher.cleanup.assert_called_once()
        return status
    """)
    assert_executes("", *argv, driver_source=driver_source)


def test_pattern_publisher_main_publish():
    """Check kcidb-mq-pattern-publisher publish works"""
    argv = ["kcidb.mq.pattern_publisher_main", "-lDEBUG",
            "-p", "project", "-t", "topic", "publish"]

    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        with patch("kcidb.mq.ORMPatternPublisher.__init__",
                   return_value=None) as init, \
             patch("kcidb.mq.ORMPatternPublisher.future_publish") \
             as future_publish:
            status = function()
            init.assert_called_once_with("project", "topic")
        return status
    """)
    assert_executes("\n", *argv, driver_source=driver_source,
                    status=1, stderr_re=".*Exception.*")
    assert_executes(">", *argv, driver_source=driver_source,
                    status=1, stderr_re=".*Exception.*")

    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        future = Mock()
        future.done = lambda: True
        future.add_done_callback = lambda cb: cb(future)
        future.result = Mock(return_value="id")
        with patch("kcidb.mq.ORMPatternPublisher.__init__",
                   return_value=None) as init, \
             patch("kcidb.mq.ORMPatternPublisher.future_publish",
                   return_value=future) as future_publish:
            status = function()
            init.assert_called_once_with("project", "topic")
            future_publish.assert_called_once_with(set())
        return status
    """)
    assert_executes("", *argv,
                    driver_source=driver_source,
                    stdout_re="id\n")

    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock, call
        from kcidb.orm import Pattern, SCHEMA
        future = Mock()
        future.done = lambda: True
        future.add_done_callback = lambda cb: cb(future)
        future.result = Mock(return_value="id")
        with patch("kcidb.mq.ORMPatternPublisher.__init__",
                   return_value=None) as init, \
             patch("kcidb.mq.ORMPatternPublisher.future_publish",
                   return_value=future) as future_publish:
            status = function()
            init.assert_called_once_with("project", "topic")
            future_publish.assert_called_once_with({
                Pattern(
                    Pattern(
                        Pattern(
                            Pattern(None, True, SCHEMA.types["checkout"],
                                    {("kernelci:1",)}),
                            False, SCHEMA.types["revision"]
                        ),
                        True, SCHEMA.types["checkout"]
                    ),
                    True, SCHEMA.types["build"]
                ),
                Pattern(
                    Pattern(
                        Pattern(None, True, SCHEMA.types["test"],
                                {("kernelci:1",)}),
                        False, SCHEMA.types["build"]
                    ),
                    True, SCHEMA.types["test"]
                )
            })
        return status
    """)
    assert_executes(">checkout[kernelci:1]<revision>checkout>build#\n"
                    ">test[kernelci:1]<build>test#",
                    *argv,
                    driver_source=driver_source,
                    stdout_re="id\n")


def test_pattern_subscriber_main_init():
    """Check kcidb-mq-pattern-subscriber init works"""
    argv = ["kcidb.mq.pattern_subscriber_main",
            "-p", "project", "-t", "topic", "-s", "subscription", "init"]
    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        subscriber = Mock()
        subscriber.init = Mock()
        with patch("kcidb.mq.ORMPatternSubscriber",
                   return_value=subscriber) as Subscriber:
            status = function()
        Subscriber.assert_called_once_with("project", "topic",
                                           "subscription")
        subscriber.init.assert_called_once()
        return status
    """)
    assert_executes("", *argv, driver_source=driver_source)


def test_pattern_subscriber_main_cleanup():
    """Check kcidb-mq-pattern-subscriber cleanup works"""
    argv = ["kcidb.mq.pattern_subscriber_main",
            "-p", "project", "-t", "topic", "-s", "subscription",
            "cleanup"]
    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        subscriber = Mock()
        subscriber.cleanup = Mock()
        with patch("kcidb.mq.ORMPatternSubscriber",
                   return_value=subscriber) as Subscriber:
            status = function()
        Subscriber.assert_called_once_with("project", "topic",
                                           "subscription")
        subscriber.cleanup.assert_called_once()
        return status
    """)
    assert_executes("", *argv, driver_source=driver_source)


def test_pattern_subscriber_main_pull():
    """Check kcidb-mq-pattern-subscriber pull works"""
    argv = ["kcidb.mq.pattern_subscriber_main",
            "-p", "project", "-t", "topic", "-s", "subscription",
            "pull", "--timeout", "123"]
    driver_source = textwrap.dedent("""
        from unittest.mock import patch, Mock
        from kcidb.orm import Pattern, SCHEMA
        subscriber = Mock()
        subscriber.pull_iter = Mock(return_value=[("ID", {
            Pattern(
                Pattern(
                    Pattern(
                        Pattern(None, True, SCHEMA.types["checkout"],
                                {("kernelci:1",)}),
                        False, SCHEMA.types["revision"]
                    ),
                    True, SCHEMA.types["checkout"]
                ),
                True, SCHEMA.types["build"]
            ),
            Pattern(
                Pattern(
                    Pattern(None, True, SCHEMA.types["test"],
                            {("kernelci:1",)}),
                    False, SCHEMA.types["build"]
                ),
                True, SCHEMA.types["test"]
            )
        })])
        subscriber.ack = Mock()
        with patch("kcidb.mq.ORMPatternSubscriber",
                   return_value=subscriber) as Subscriber:
            status = function()
        Subscriber.assert_called_once_with("project", "topic",
                                           "subscription")
        subscriber.pull_iter.assert_called_once_with(1, timeout=123)
        subscriber.ack.assert_called_once_with("ID")
        return status
    """)
    assert_executes(
        "", *argv, driver_source=driver_source,
        stdout_re=re.escape(
            ">checkout[kernelci:1]<revision>checkout>build#\n"
            ">test[kernelci:1]<build>test#\n"
        ) + "|" + re.escape(
            ">test[kernelci:1]<build>test#\n"
            ">checkout[kernelci:1]<revision>checkout>build#\n"
        )
    )
