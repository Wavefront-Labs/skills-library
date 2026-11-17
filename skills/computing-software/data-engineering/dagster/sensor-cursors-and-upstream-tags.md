---
id: computing-software.data-engineering.dagster.sensor-cursors-and-upstream-tags
name: sensor-cursors-and-upstream-tags
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, sensor-cursor, run-key, asset-sensor, partition-key, logging-tags]
level: advanced
status: docs-checked
description: "Use sensor cursors for high-volume events, avoid the run_key plus cursor reset trap, and read upstream partition tags in sensors."
sources:
  - https://docs.dagster.io/guides/automate/sensors/index
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sensor cursors and upstream tags

## Cursors
For many events, store state in a cursor so each evaluation only creates `RunRequest`s for files updated since the last tick (docs example: modified time of files in a directory). With several event streams, serialize a richer structure into the cursor string.

Gotcha: if you set both `run_key` and a cursor, resetting the cursor will NOT relaunch runs for unchanged files, because their run keys are unchanged. To be able to reset a cursor, do not set `run_key`s.

## Upstream tags
Retrieve the partition key from the upstream event and pass it on:

```python
@sensor(asset_key=AssetKey("my_asset"))
def my_asset_sensor(context, asset_event):
    partition_key = asset_event.dagster_event.logging_tags.get("dagster/partition")
    if partition_key:
        return RunRequest(run_key=partition_key,
                          tags={"dagster/partition": partition_key})
    return None
```

## Checked

2026-11-09. Pages read in full against this skill:
- https://docs.dagster.io/guides/automate/sensors/index

Confirmed: cursor usage for high-volume events, the run_key plus cursor reset gotcha, and the upstream partition tag snippet, against the page text and code.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
