---
id: computing-software.cloud-infrastructure-engineering.graylog.indexer-failures-field-types
name: indexer-failures-field-types
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [indexer-failures, mapper-parsing-exception, field-types, index-cycling]
level: advanced
status: docs-checked
description: "Understand indexer failures such as MapperParsingException: first type per index wins, so keep field types stable."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/indexer_failures.html
  - https://go2docs.graylog.org/current/setting_up_graylog/index_model.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# indexer failures field types

Indexer failures are stored in a size-limited MongoDB collection. Tens of thousands fit, but it is not a complete error history.

Classic failure: `MapperParsingException ... NumberFormatException`. You wrote a string into a numeric field. Typical triggers are GELF messages that send a field with differing types, or extractors writing strings without conversion.

Why it happens: the first type written to a field per index wins. When the index cycles, field types start fresh, so a field first written as a string stays a string until the next cycle.

Fix: decide field types deliberately and never change them. If `https_response_code` is numeric, always send a number. Have extractors convert strings to numbers. The same applies to booleans and other types.

## Checked

2026-11-04. Confirmed against the Indexer Failures page. Removed: "Convert values in pipeline rules before indexing", which the page does not state (it says to have extractors convert strings to numbers).

Method: documentation only; no commands were run.
