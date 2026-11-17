---
id: computing-software.cloud-infrastructure-engineering.fluentd.extract-and-inject-sections
name: extract-and-inject-sections
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, extract-section, inject-section, tag-key, time-key, hostname-key]
level: practitioner
status: docs-checked
description: "Use extract to pull tag and time out of records and inject to add tag, time, hostname and worker_id fields to records."
sources:
  - https://docs.fluentd.org/configuration/extract-section
  - https://docs.fluentd.org/configuration/inject-section
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd extract and inject sections
**extract** (under `<source>`, `<match>` or `<filter>`, for plugins such as `exec`) takes values out of the record:
- `tag_key`, `keep_tag_key` (default false): field to use as the tag.
- `time_key`, `keep_time_key` (default false): field to use as event time.
- Time parameters `time_type` (default `float`), `time_format`, `localtime`, `utc`, `timezone`.

**inject** (under `<match>` or `<filter>`) adds values to the record:
- `hostname_key` (value from `hostname`, default `Socket.gethostname`), `worker_id_key`, `tag_key`, `time_key`.
- `time_type`: `float` (default, microseconds), `unixtime`, `unixtime_millis` (since v1.11.4), `unixtime_micros` and `unixtime_nanos` (since v1.20.0), `string` (with `time_format`).

```
<inject>
  time_key fluentd_time
  time_type string
  time_format %Y-%m-%dT%H:%M:%S.%NZ
  tag_key fluentd_tag
</inject>
```
Record `{"message":"hello"}` with tag `test` becomes `{"message":"hello","fluentd_tag":"test","fluentd_time":"2019-01-15T18:06:03.952259000Z"}`.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/extract-section, https://docs.fluentd.org/configuration/inject-section and confirmed: parameter names, defaults and versions, worked inject example. Removed or reworded: nothing.

Method: documentation only; no commands were run.
