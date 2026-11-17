---
id: computing-software.data-science-and-analytics.pandas-numpy.excel-and-database-io
name: excel-and-database-io
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [read-excel, read-sql, pandas-sql-io]
level: practitioner
status: draft
description: "Load Excel sheets with read_excel and query databases with read_sql through a SQLAlchemy engine using bound parameters."
sources:
  - https://pandas.pydata.org/docs/user_guide/io.html#excel-files
  - https://pandas.pydata.org/docs/user_guide/io.html#sql-queries
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Excel and SQL I/O
```python
x = pd.read_excel("book.xlsx", sheet_name="Sales", header=1, usecols="A:F")  # needs openpyxl
from sqlalchemy import create_engine, text
eng = create_engine("postgresql+psycopg2://USER:PASS@HOST/DB")   # placeholders; take from env
df = pd.read_sql(text("select * from orders where day >= :d"), eng, params={"d": "2026-01-01"})
df.to_sql("orders_clean", eng, if_exists="append", index=False, chunksize=10_000)
```
## Gotchas
- Never build SQL with f-strings; use bound parameters.
- `to_sql(if_exists="replace")` drops and recreates the table, losing constraints and indexes.
- Excel dates and merged cells need manual cleanup; sheet_name=None returns all sheets as a dict.
## Verify
- [ ] Row counts in and out match; credentials come from environment, not source.
