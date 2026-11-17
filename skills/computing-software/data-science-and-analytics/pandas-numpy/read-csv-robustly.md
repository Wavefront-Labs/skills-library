---
id: computing-software.data-science-and-analytics.pandas-numpy.read-csv-robustly
name: read-csv-robustly
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [read-csv-options, csv-parsing, pandas-read-csv, pd-io]
level: practitioner
status: docs-checked
description: "Use read_csv with explicit dtype, parse_dates, na_values, encoding and usecols so type inference and encodings never surprise you."
sources:
  - https://pandas.pydata.org/docs/user_guide/io.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Robust read_csv
```python
df = pd.read_csv(
    "data.csv", sep=",", encoding="utf-8",   # match encoding to the file
    dtype={"zip": "string", "id": "Int64"},    # keep leading zeros in codes
    parse_dates=["created"], na_values=["", "NA", "n/a", "-"],
    usecols=["id","zip","created","amt"], thousands=",",
)
```
## Gotchas
- `low_memory=True` (the default) parses in chunks, which can give mixed type inference; to avoid it, set `low_memory=False` or specify `dtype`.
- `dtype` accepts a dict such as `{'c': 'Int64'}`; use `str` or `object` with suitable `na_values` to preserve values without interpreting the dtype.
- Match `encoding` to the file; the user guide shows decoding with `encoding="latin-1"` for latin-1 data.
- `on_bad_lines` accepts `'error'` (default), `'warn'` or `'skip'`.
- Numbers with a thousands separator are parsed as strings unless `thousands` is set.
- `usecols` limits the columns parsed.
## Verify
- [ ] Row count matches the source file minus header; key columns have expected dtypes.

## Checked

Method: docs-checked 2026-11-09 against the pandas IO tools user guide (read_csv parameter list, usecols, thousands, na_values and encoding sections, read via text conversion). Dropped the utf-8-sig advice, the DtypeWarning-per-chunk claim and the wc-based check, which that page does not state.
