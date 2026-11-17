---
id: computing-software.data-science-and-analytics.pandas-numpy.resample-and-frequency
name: resample-and-frequency
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [resample, datetimeindex, frequency-alias, pd-timeseries]
level: practitioner
status: docs-checked
description: "Aggregate irregular timestamps to regular intervals with resample, picking label, closed side and aggregation correctly."
sources:
  - https://pandas.pydata.org/docs/user_guide/timeseries.html#resampling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resample
```python
ts = df.set_index("ts").sort_index()
daily = ts["v"].resample("D").sum()
weekly = ts["v"].resample("W-MON", label="left", closed="left").mean()
```
## Gotchas
- `closed` picks which end of each bin is closed and `label` picks whether the bin is labelled by its start or end; the default for both is `left` for most frequencies.
- Check alias names against your pandas version; the current docs list `ME` for month end, `QE`, `YE` and lowercase `h` for hourly.
## Verify
- [ ] Daily total over the period equals the raw total.

## Checked

Method: docs-checked 2026-11-09 against the pandas time series user guide (resampling and offset aliases sections, read via text conversion). Dropped the `min_count` claim and the "renamed in 2.2" attribution, which that page does not state.
