from tap_loopreturns.streams import Stream, Returns
from tap_loopreturns.discover import discover_streams
from tap_loopreturns.loop import Loop

from nose import tools


def test_load_return_schema():
    stream = Stream()
    returns = Returns(stream)
    returns.load_schema()
    tools.assert_equals(returns.name, "returns", "Check schema loaded successfully.")


def test_schema_discovery():
    client = Loop("apiKey", "startDate")
    streams = discover_streams(client)
    tools.assert_true(isinstance(streams, list))
    tools.assert_true(isinstance(streams[0], dict))
    tools.assert_equal(streams[0]["stream"], "returns")
    tools.assert_equal(streams[0]["tap_stream_id"], "returns")
