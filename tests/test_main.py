from tap_loopreturns import discover
from tap_loopreturns.loop import Loop

from nose import tools


def test_discover():
    client = Loop("apiKey", "startDate")
    streams = discover( client )
    tools.assert_is_instance( streams, dict, "Check that streams exist.")
    tools.assert_in( 'streams', streams, 'We have the right structure' )
