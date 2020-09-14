#!/usr/bin/env python3
import os
import json
import sys
import singer

from singer import utils, metadata

from tap_loopreturns.streams import STREAMS
from tap_loopreturns.context import Context
from tap_loopreturns.loop import Loop
from tap_loopreturns.discover import discover_streams
from tap_loopreturns.sync import sync_stream

REQUIRED_CONFIG_KEYS = [
    "start_date",
    "api_key",
    "end_date",
]
LOGGER = singer.get_logger()

def discover(client):
    catalog = {"streams": discover_streams(client)}
    return catalog


def stream_is_selected(mdata):
    return mdata.get((), {}).get('selected', False)


def get_selected_streams(catalog):
    selected_stream_names = []
    for stream in catalog.streams:
        selected_stream_names.append(stream.tap_stream_id)
    return selected_stream_names


def sync(client, catalog, state):
    selected_stream_names = get_selected_streams(catalog)

    for stream in catalog.streams:
        stream_name = stream.tap_stream_id
        mdata = metadata.to_map(stream.metadata)

        if stream_name not in selected_stream_names:
            LOGGER.info("%s: Skipping - not selected", stream_name)
            continue

        key_properties = metadata.get(mdata, (), 'table-key-properties')
        singer.write_schema(stream_name, stream.schema.to_dict(), key_properties)
        LOGGER.info("%s: Starting sync", stream_name)

        instance = STREAMS[stream_name](client)
        instance.stream = stream
        counter_value = sync_stream(state, instance)
        singer.write_state(state)

        LOGGER.info("%s: Completed sync (%s rows)", stream_name, counter_value)

    singer.write_state(state)
    LOGGER.info("Finished sync")


@singer.utils.handle_top_exception(LOGGER)
def main():
    parsed_args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    creds = {
        "start_date": parsed_args.config['start_date'],
        "api_key": parsed_args.config['api_key'],
        "end_date": parsed_args.config['end_date'],
    }

    client = Loop(**creds)
    Context.config = parsed_args.config

    if parsed_args.discover:
        catalog = discover(client)
        json.dump(catalog, sys.stdout, indent=2)
    else:
        state = parsed_args.state or {}
        # If we have state - we need to unset the end_date in the config file.
        if len(state) > 0:
            client.end_date = None
        catalog = parsed_args.catalog
        sync(client, catalog, state)
