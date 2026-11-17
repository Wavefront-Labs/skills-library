---
id: computing-software.data-engineering.apache-spark.xml-data-source
name: xml-data-source
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, spark-xml, xml, rowtag, data-sources, nested-data-spark]
level: practitioner
status: docs-checked
description: "Read and write XML in Spark with the native XML source (4.0+) or spark-xml: rowTag, attribute prefixes, schema inference cost, and malformed-record handling."
sources:
  - https://spark.apache.org/docs/latest/sql-data-sources-xml.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XML data source

Spark ships a built-in `xml` data source, documented in the data sources guide; `rowTag` must be specified. It is available through `DataFrameReader` / `DataFrameWriter`, the streaming reader and writer, the functions `from_xml`, `to_xml` and `schema_of_xml`, and the `OPTIONS` clause of CREATE TABLE USING.

```python
df = (spark.read.format("xml")
      .option("rowTag", "book")            # XML element that maps to a DataFrame row (required)
      .option("attributePrefix", "_")       # prefix for attribute field names (default "_"; may be empty for reading, not for writing)
      .option("valueTag", "_VALUE")         # tag used for the value when an element has attributes but no child (default)
      .option("mode", "PERMISSIVE")
      .option("columnNameOfCorruptRecord", "_corrupt_record")
      .schema(book_schema)                  # strongly recommended
      .load("s3a://raw/catalog/*.xml"))
```

## Things to know
- Schema inference uses `samplingRatio` (default 1.0, the fraction of rows used) and can give unstable types for fields that sometimes repeat; define the schema explicitly and use `ArrayType` for anything that can repeat.
- `ignoreNamespace` (default false) ignores namespace prefixes on elements and attributes, except on the `rowTag` element itself.
- `rowValidationXSDPath` validates each row against an XSD file; rows that fail are treated like parse errors.
- `mode` PERMISSIVE puts the malformed string in the field named by `columnNameOfCorruptRecord` and sets malformed fields to null; if the schema lacks that field, corrupt records are dropped during parsing (when inferring a schema the field is added implicitly).
- Flatten nested results with `select` and `F.explode` on the array field.
- `from_xml(col, schema)` parses an XML string column.
- Writing uses `rootTag` (default `ROWS`) and `rowTag`: `df.write.format("xml").option("rootTag", "books").option("rowTag", "book").save(path)`.

## Verify
- [ ] Row count matches the number of `rowTag` elements in a sample file.
- [ ] `_corrupt_record` is empty or monitored (and present in the schema).

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in sql-data-sources-xml.md: rowTag required, attributePrefix default _ (empty allowed for reading only), valueTag default _VALUE, samplingRatio default 1.0, ignoreNamespace default false and its rowTag exception, rowValidationXSDPath behaviour, mode / columnNameOfCorruptRecord semantics (corrupt records dropped when the schema lacks the field), rootTag default ROWS, supported APIs and from_xml / to_xml / schema_of_xml. Wrong claim fixed: for XML a schema without the corrupt-record column drops corrupt records (unlike CSV, which retains them). Removed the Databricks spark-xml version history and pinned 0.18.0 package, the nesting rule and one-file-per-partition claims.

Method: documentation only; no commands were run.
