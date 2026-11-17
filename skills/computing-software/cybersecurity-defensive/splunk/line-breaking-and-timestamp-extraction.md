---
id: computing-software.cybersecurity-defensive.splunk.line-breaking-and-timestamp-extraction
name: line-breaking-and-timestamp-extraction
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, data-onboarding, props-conf, line-breaking, timestamp-extraction, should-linemerge, line-breaker, time-format, max-timestamp-lookahead]
level: practitioner
status: draft
description: "Configure Splunk props.conf so multi-line events break correctly and timestamps parse exactly: LINE_BREAKER, SHOULD_LINEMERGE, TIME_PREFIX, TIME_FORMAT, TZ."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Data/Configureeventlinebreaking", "https://docs.splunk.com/Documentation/Splunk/latest/Data/Configuretimestamprecognition", "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Propsconf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Line breaking and timestamp extraction

**Goal:** each event is exactly one record with the correct `_time`, set explicitly rather
than left to Splunk's guessing (which is slow and wrong for edge cases).

## The "great eight" props.conf settings
For every custom sourcetype, on the first full Splunk instance in the path (indexer or heavy
forwarder; UF only for `INDEXED_EXTRACTIONS`):
```
[myapp:log]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+)(?=\d{4}-\d{2}-\d{2}T)
TRUNCATE = 10000
TIME_PREFIX = ^
TIME_FORMAT = %Y-%m-%dT%H:%M:%S.%3N%z
MAX_TIMESTAMP_LOOKAHEAD = 30
EVENT_BREAKER_ENABLE = true
EVENT_BREAKER = ([\r\n]+)(?=\d{4}-\d{2}-\d{2}T)
```
- `LINE_BREAKER`: the first capture group is discarded; the lookahead keeps the timestamp
  in the next event. Multi-line stack traces stay in one event because continuation lines
  do not start with a date.
- `SHOULD_LINEMERGE = false` with an explicit breaker is much faster than the merge rules.
- `EVENT_BREAKER` lets universal forwarders split on event boundaries so load balancing
  does not cut events in half.
- `TRUNCATE` default is 10000 bytes; raise for large JSON, never set to 0 in production.

## Timestamps
- `TIME_PREFIX` is a regex anchoring where the time starts; for JSON use
  `TIME_PREFIX = "timestamp":\s*"`.
- `MAX_TIMESTAMP_LOOKAHEAD` counts characters after the prefix; keep it tight so digits
  later in the event are never parsed as time.
- Epoch: `TIME_FORMAT = %s%3N` for milliseconds.
- No zone in the data: set `TZ = UTC` (or the source's zone) in the sourcetype or per host
  stanza `[host::fw-syd-*]`. Without it the indexer's local zone is assumed.
- `DATETIME_CONFIG = CURRENT` only for sources with no usable time at all.

## Test before production
Settings > Add Data > upload a sample, pick the sourcetype, and watch the event preview;
or run on a dev instance with `oneshot`:
```
splunk add oneshot sample.log -sourcetype myapp:log -index sandbox
```

## Gotchas
- Props on a search head do nothing for parsing; parsing happens where data is first parsed.
- Changes only affect newly indexed data; re-ingest a sample to confirm.
- `MAX_DAYS_AGO`/`MAX_DAYS_HENCE` silently clamp bad dates to the previous event's time.

## Verify
```
index=sandbox sourcetype=myapp:log | eval lag=_indextime-_time
| stats min(lag) max(lag) avg(lag) count by host
index=_internal sourcetype=splunkd (component=DateParserVerbose OR component=LineBreakingProcessor)
| stats count by component, data_sourcetype
```
Lag should be small and positive; the internal warnings should be zero for the sourcetype.
