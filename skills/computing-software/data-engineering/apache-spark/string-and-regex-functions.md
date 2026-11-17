---
id: computing-software.data-engineering.apache-spark.string-and-regex-functions
name: string-and-regex-functions
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, spark-sql, spark-regex-functions, regexp-extract, regexp-replace, split, format-string, string-functions]
level: practitioner
status: docs-checked
description: "Clean and parse text columns in Spark with regexp_extract, regexp_replace, rlike, split, format_string and friends, with Java regex and null-handling notes."
sources:
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html
  - https://spark.apache.org/docs/latest/sql-ref-functions-builtin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String and regex functions in Spark

## Core toolkit
```python
from pyspark.sql import functions as F
df = (df
  .withColumn("order_id", F.regexp_extract("raw", r"ORD-(\d{6})", 1))
  .withColumn("phone", F.regexp_replace("phone", r"[^0-9+]", ""))
  .withColumn("is_email", F.col("contact").rlike(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$"))
  .withColumn("parts", F.split("path", "/"))                          # the pattern is a regex
  .withColumn("domain", F.element_at(F.split("email", "@"), -1))
  .withColumn("label", F.format_string("%s-%05d", "region", "seq"))
  .withColumn("name", F.initcap(F.trim("name")))
  .withColumn("sku", F.lpad("sku", 8, "0")))
```
- Spark regex is **Java** regex (the PySpark `rlike` docs say so). Check how backslashes are escaped in SQL string literals for your Spark version before copying patterns between Python and SQL.
- `regexp_extract(str, regexp[, idx])` returns the first match for a group; `regexp_extract_all` returns all matches; `regexp_substr` returns null when the pattern is not found. `regexp_count` and `regexp_instr` also exist. Test what your version returns on no match before relying on null vs empty.
- `split(str, regex, limit)` takes a regex and returns an array of at most `limit` elements.
- `concat_ws(sep, ...)` skips null values.
- `translate(input, from, to)` replaces characters one-for-one, which suits single-character swaps better than a regex.

## Performance
- Prefer built-in functions over a Python UDF for text cleanup.
- Regex in a hot path: anchor patterns and avoid nested quantifiers that backtrack catastrophically.

## Verify
- [ ] Test the pattern on edge rows (null, empty, unicode, multiple matches) with a small `spark.createDataFrame`.
- [ ] `explain()` shows no Python UDF stage for string logic.

## Checked
2026-11-01: confirmed against the Spark SQL built-in functions page and the PySpark functions reference: regexp_extract, regexp_extract_all, regexp_substr, regexp_count, regexp_instr, regexp_replace, split(str, regex, limit), concat_ws skipping nulls, translate, format_string, initcap, rpad, element_at (negative index counts from the end), Java regex wording for rlike. Removed: version gates, no-match empty-string claim, nullif, parser literal settings, pushdown and runtime claims.
Method: documentation only; no commands were run.
