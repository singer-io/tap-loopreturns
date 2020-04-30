# tap-loopreturns

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from the [LoopReturns API](https://docs.loopreturns.com)
- Extracts the following resources:
  - [Returns: Detailed Returns List](https://docs.loopreturns.com/#detailed-returns-list)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

# Quickstart

### 1.  Installation
```shell
    pip install tap-loopreturns
```

### 2.  Create the configuration file

Copy sample_config.json to config.json and add the appropriate values.

```
    api_key    : the API key generated in your LoopReturns Admin 
    start_date : the date at which you want to start the data sync 
    end_date   : the date at which you want to end the data pull only
    user_agent : this entry is here for reference purposes
```

The end date parameter is only used on the first sync run.  This allows you to pull a larger window of data when you first start out.  This parameter will be overridden to be 24hours after the start date in subsequent runs.

### 3.  Run the tap in Discovery mode.
```shell
tap-loopreturns -c config.json -d
```
See the Singer docs on discovery mode [here.](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode)

### 4.  Run the tap in Sync mode.
```shell script
# For the first sync
tap-loopreturns -c config.json --catalog catalog.json

# For subsequent syncs
tap-loopreturns -c config.json --catalog catalog.json --state state.json
```
See the Singer docs on sync mode [here.](https://github.com/singer-io/getting-started/blob/master/docs/SYNC_MODE.md)

---

Copyright &copy; 2020 Loop
