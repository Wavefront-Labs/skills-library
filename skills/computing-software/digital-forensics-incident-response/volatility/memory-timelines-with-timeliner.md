---
id: computing-software.digital-forensics-incident-response.volatility.memory-timelines-with-timeliner
name: memory-timelines-with-timeliner
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [timeliner, memory-forensics, volatility3, super-timeline, bodyfile, dfir]
level: practitioner
status: docs-checked
description: "Build memory timelines with the Volatility 3 timeliner plugin: how it collects timestamps from other plugins, bodyfile output, the plugin filter, and merging with disk timelines."
sources: ["https://volatility3.readthedocs.io/en/latest/", "https://github.com/volatilityfoundation/volatility3", "https://raw.githubusercontent.com/volatilityfoundation/volatility3/develop/volatility3/framework/plugins/timeliner.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory timelines with timeliner

**Goal:** get all timestamps Volatility can extract from a RAM image in one sorted view and
merge them with disk timelines.

## Run
```bash
vol -f mem.raw timeliner.Timeliner
vol -f mem.raw timeliner.Timeliner --create-bodyfile          # also writes a body file
vol -f mem.raw timeliner.Timeliner --plugin-filter windows.pslist windows.netscan   # subset
```
- Timeliner runs every plugin that implements `TimeLinerInterface`; each yields tuples of
  (description, timestamp type, timestamp) where the type is one of CREATED, MODIFIED,
  ACCESSED or CHANGED. Which plugins take part depends on your Volatility version and OS
  plugins installed.
- `--plugin-filter` takes a list and runs only plugins whose name contains one of the
  substrings; `--create-bodyfile` is a boolean that writes a body file while producing results.
- Expect it to be slow on big images, since it runs many plugins.
- Choose the output format (CSV, JSON, pretty) with Volatility's renderer option; see
  `vol --help` for your version.

## Merge with disk evidence
- Feed the body file to a mactime-style tool (Sleuth Kit) together with disk body files, or
  convert the output for your timeline tool (Timesketch, Timeline Explorer).
- Keep a source column (memory vs disk) so analysts can tell which timestamps came from RAM.

## Interpretation
- Timestamps reflect objects still resident in memory; confirm time zone handling in your
  version's output before merging with local-time disk data.
- Network objects' times show when the object was created, not necessarily live traffic.

## Verify
Pick a known event (e.g. a process start also in Prefetch or Security event 4688) and confirm
the times match across memory and disk timelines.

## Checked
2026-11-01. Confirmed in the Volatility 3 source (`plugins/timeliner.py`): the `plugin-filter`
list option ("Only run plugins featuring this substring"), the `create-bodyfile` boolean, the
`TimeLinerInterface` generator tuple and the four timestamp types. Removed: the specific
plugin list, `mactime`/`fls -m` command lines, UTC and registry-flush claims, and the
`-q -r csv` form, none of which the fetched docs confirm.
Method: documentation only; no commands were run.
