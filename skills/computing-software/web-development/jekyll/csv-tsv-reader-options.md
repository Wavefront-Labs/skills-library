---
id: computing-software.web-development.jekyll.csv-tsv-reader-options
name: csv-tsv-reader-options
category: computing-software
field: web-development
product: jekyll
tags: [csv-reader, tsv-reader, csv-converters, headers-option, data-encoding]
level: advanced
status: docs-checked
description: "Customise how Jekyll parses CSV and TSV data files with csv_reader and tsv_reader: converters, encoding and headers options."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/datafiles.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ruby's parsing of CSV and TSV files in `_data` is configurable through `csv_reader` and `tsv_reader`. Both keys take the same options:

- `converters`: which CSV converters to apply. Available: `integer`, `float`, `numeric`, `date`, `date_time` and `all`. Empty by default.
- `encoding`: file encoding; defaults to the site `encoding` option.
- `headers`: whether the first line is headers. When `false`, the first row is treated as data. Defaults to `true`.

```yaml
csv_reader:
    converters:
      - numeric
      - date_time
    headers: true
    encoding: utf-8
tsv_reader:
    converters:
      - all
    headers: false
```

CSV and TSV data files must contain a header row.

## Checked

2026-11-04. Confirmed against the Jekyll data files doc: `csv_reader` and `tsv_reader`, the three options, the converter names, defaults, and the header-row requirement. The page's own example writes `datetime`, but its list of converters says `date_time`, so the example here uses `date_time`. Removed an unsupported sentence about rows not being keyed by column name.

Method: documentation only; no commands were run.
