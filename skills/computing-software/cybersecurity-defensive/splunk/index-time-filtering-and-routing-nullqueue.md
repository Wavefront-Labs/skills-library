---
id: computing-software.cybersecurity-defensive.splunk.index-time-filtering-and-routing-nullqueue
name: index-time-filtering-and-routing-nullqueue
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, data-onboarding, nullqueue-filtering, transforms-conf, props-conf, index-routing, license-reduction, heavy-forwarder]
level: practitioner
status: draft
description: "Drop noisy events with nullQueue and route events to other indexes or sourcetypes at index time via props/transforms, on the right tier, without losing needed data."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Forwarding/Routeandfilterdatad", "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Transformsconf", "https://docs.splunk.com/Documentation/Splunk/latest/Data/Advancedsourcetypeoverrides"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Index-time filtering and routing

## Drop events (nullQueue)
props.conf
```
[WinEventLog:Security]
TRANSFORMS-drop = drop_4662_noise
```
transforms.conf
```
[drop_4662_noise]
REGEX = (?m)^EventCode=(4662|5156)\b
DEST_KEY = queue
FORMAT = nullQueue
```
Keep-only pattern (drop everything, then put wanted events back on the index queue). Order matters:
```
TRANSFORMS-set = setnull, setparsing
[setnull]
REGEX = .
DEST_KEY = queue
FORMAT = nullQueue
[setparsing]
REGEX = action=(deny|drop)
DEST_KEY = queue
FORMAT = indexQueue
```

## Route to another index or sourcetype
```
[route_dc_to_ad_index]
SOURCE_KEY = MetaData:Host
REGEX = ^host::dc\d+
DEST_KEY = _MetaData:Index
FORMAT = ad_security

[rename_st]
REGEX = "eventType":"AwsApiCall"
DEST_KEY = MetaData:Sourcetype
FORMAT = sourcetype::aws:cloudtrail:api
```

## Where it runs
- Parsing happens on the first full Splunk instance: indexer or heavy forwarder. Universal
  forwarders do not apply TRANSFORMS (except structured data with INDEXED_EXTRACTIONS).
- If a heavy forwarder sits in front of the indexers, the config must live on the HF; the
  indexers receive already-cooked data and will ignore it.
- Deploy via cluster manager bundle (`master-apps`/`manager-apps`) for indexer clusters.

## What to drop safely
- Agree with detection owners first. Security-relevant noise is often what an investigation
  needs later (e.g. 4662 is noisy but used for DCSync detection with specific GUIDs; filter
  by GUID rather than dropping the event ID).
- Prefer trimming at the source (Windows audit policy, firewall log profile) over parsing cost.
- For partial reduction keep a sample: route the rest to a cheap short-retention index instead.

## Gotchas
- REGEX applies to `_raw` unless SOURCE_KEY is set; XML-rendered Windows events have different
  text (`<EventID>4662</EventID>`) to classic format.
- Dropped data is gone; there is no recovery.
- Ingest Actions (Settings > Data > Ingest Actions) offers the same with a preview UI on 9.x.

## Verify
- Before/after volume: `| tstats count where index=wineventlog by sourcetype _time span=1h`.
- `index=_internal source=*metrics.log group=per_sourcetype_thruput series="WinEventLog:Security"`
  for licence impact.
- Spot-check that wanted events still arrive.
