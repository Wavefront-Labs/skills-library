---
id: computing-software.data-science-and-analytics.pandas-numpy.dataframe-validation-pandera
name: dataframe-validation-pandera
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [pandera-schema, data-validation-checks, great-expectations]
level: practitioner
status: draft
description: "Codify column types, ranges, uniqueness and nullability as a schema that fails fast when incoming data breaks assumptions."
sources:
  - https://pandera.readthedocs.io/
  - https://docs.greatexpectations.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Schema validation (pandera)
```python
import pandera as pa
schema = pa.DataFrameSchema({
    "id": pa.Column(int, unique=True),
    "amt": pa.Column(float, pa.Check.ge(0), nullable=False),
    "status": pa.Column(str, pa.Check.isin(["new", "paid", "void"])),
})
clean = schema.validate(df, lazy=True)      # lazy=True reports all failures
```
## Gotchas
- Validate at pipeline boundaries (after load, before publish).
- Checks that tolerate everything are worthless; set realistic bounds.
- API details vary by version; check the docs for your release.
## Verify
- [ ] A deliberately bad row triggers a failure.
