---
id: computing-software.data-science-and-analytics.pandas-numpy.string-methods-regex-cleaning
name: string-methods-regex-cleaning
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [str-accessor, regex-extract, text-cleaning, pd-text-categorical]
level: practitioner
status: docs-checked
description: "Normalise whitespace and case, extract fields with regex groups and split columns using the vectorised str accessor."
sources:
  - https://pandas.pydata.org/docs/user_guide/text.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# str accessor
```python
s = df["name"].str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
parts = df["code"].str.extract(r"^(?P<prefix>[A-Z]{2})-(?P<num>\d+)$")
df[["first","last"]] = df["full"].str.split(" ", n=1, expand=True)
```
## Gotchas
- Set `regex=True` or `regex=False` explicitly in `replace`; since pandas 2.0 a single-character pattern with `regex=True` is treated as a regular expression.
- `extract` with named groups returns columns named after the groups.
- An object column can hold a mixture of strings and non-strings; the guide recommends a dedicated string dtype.
## Verify
- [ ] Count rows where extract returned NaN; each is a pattern miss to inspect.

## Checked

Method: docs-checked 2026-11-09 against the pandas working with text data user guide (str accessor, split, replace and extract sections, read via text conversion). Dropped the `contains(na=False)` mask and the non-string-to-NaN claim, which that page does not show.
