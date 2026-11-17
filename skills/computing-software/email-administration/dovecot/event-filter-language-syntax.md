---
id: computing-software.email-administration.dovecot.event-filter-language-syntax
name: event-filter-language-syntax
category: computing-software
field: email-administration
product: dovecot
tags: [event-filter, category-filter, wildcard-match, ip-filter, metric-filter, log-debug]
level: advanced
status: docs-checked
description: "Write event filters: SQL-like AND, OR, NOT expressions, name and source location matching, wildcard and operator rules per field type."
sources:
  - https://doc.dovecot.org/main/core/config/events/filter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Event filters select which events are processed, for example for debug logging or metrics. Individual events can be identified by name or by source location, but locations change between versions and should be avoided.

Matching rules:
- Event names: case-sensitive wildcard match with `?` and `*`; escape a literal with a backslash.
- Source location: file name case-sensitive, line number as an integer (optional).
- Categories: a "has a" relationship. Every category in the filter must be present on the event; extra categories on the event do not matter.
- Fields: case-insensitive wildcard match.

The unified language is a SQL-like boolean expression with AND, OR, NOT, parentheses and the comparisons `=`, `<`, `>`, `<=`, `>=`. A comparison has the form `key operator value`. The key is case-sensitive, the value comparison is not. A value is a single word token or a quoted string, and may contain wildcards only with `=`.

Operator limits by field type:
- string: only `=`.
- ip: only `=`. IPs are matched in parsed form (2001::1 equals 2001:0:0:0:0:0:0:1) and may match CIDR masks such as 127.0.0.0/8. A wildcard compares the text form, so 2001::1* matches 2001::1234 but 2001:0:0:0:0:0:0:1* matches neither. Link-local addresses match only on the same interface, and the `%` needs quoting.
- number: all operators; wildcards compare as strings (40* matches 40 and 401).
- timestamp: no operators.
- list of strings: only `=`, true if the key is one of the values; an empty string matches an empty list.

The key is one of `event`, `category`, `source_location` or a field name. Whitespace between tokens is not significant, so `event=abc` and `event = "abc"` are equivalent. Sizes take the units B (default), KB, MB, GB, TB (powers of 1024, case-insensitive); times take milliseconds (msecs), seconds (secs), minutes (mins), days, weeks. The page says a type mismatch or unsupported operation now generates a warning (previously silently ignored).

Use these filters in global settings such as `log_debug`, for example:
```
log_debug = (event=http_request_finished AND category=imap) OR \
    (event=imap_command_finished AND user=testuser)
```
and in the `filter` key of a statistics `metric` block (for example `filter = event=http_request_finished AND category=storage AND status_code=200`).

Performance: from 2.4.6, matching `log_debug` and `log_core_filter` is cached per event, but if either setting contains `source_location` anywhere (even inside NOT) caching is disabled for all events in the process and every debug log call becomes several times slower. Use `source_location` only temporarily; prefer event name, category or fields. Metric filters are not affected.

## Checked
2026-11-09. Read the whole Dovecot "Event Filtering" page (doc.dovecot.org/main/core/config/events/filter.html) and confirmed every rule above; added keys, units, examples and the source_location performance warning from it.

Method: documentation only; no commands were run.
