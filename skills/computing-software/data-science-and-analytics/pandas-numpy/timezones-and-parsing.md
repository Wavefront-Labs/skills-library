---
id: computing-software.data-science-and-analytics.pandas-numpy.timezones-and-parsing
name: timezones-and-parsing
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [tz-localize, tz-convert, datetime-parsing]
level: practitioner
status: docs-checked
description: "Localise naive timestamps, convert between zones and avoid daylight saving errors when parsing and comparing datetimes."
sources:
  - https://pandas.pydata.org/docs/user_guide/timeseries.html#time-zone-handling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time zones
```python
t = pd.to_datetime(df["ts"]).dt.tz_localize("UTC")        # naive values assumed to be UTC
local = t.dt.tz_convert("Australia/Brisbane")
naive = pd.to_datetime(df["ts"]).dt.tz_localize("America/New_York", ambiguous="infer", nonexistent="shift_forward")
```
## Gotchas
- DST creates ambiguous and nonexistent local times; `tz_localize` raises by default. `ambiguous` accepts `"infer"`, `"NaT"` or a boolean array, and `nonexistent` accepts `"raise"`, `"NaT"`, `"shift_forward"`, `"shift_backward"` or a timedelta.
- `"infer"` for ambiguous times relies on the monotonicity of the timestamps.
- `tz_localize(None)` drops the time zone and keeps local time; `tz_convert(None)` is the same as converting to UTC then dropping it.
## Verify
- [ ] Round-trip UTC -> local -> UTC returns identical values.

## Checked

Method: docs-checked 2026-11-09 against the pandas time series user guide (time zone handling, ambiguous and nonexistent times sections, read via text conversion). Dropped the claim that mixing aware and naive values raises and the reporting advice, which that page does not state; `pd.to_datetime(utc=True)` was replaced by an explicit tz_localize.
