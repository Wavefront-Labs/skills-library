---
id: computing-software.cloud-infrastructure-engineering.graylog.search-syntax-basics
name: search-syntax-basics
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [search-syntax, query-language, wildcards, case-sensitivity, boolean-operators]
level: practitioner
status: docs-checked
description: "Graylog search query rules: case sensitivity, whitespace tokenization, fields, Boolean operators, wildcards, ranges and escaping."
sources:
  - https://go2docs.graylog.org/current/making_sense_of_your_log_data/search_syntax_reference.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# search syntax basics

Without a field restriction, a query searches indexed messages across available fields.

- Searches are case-sensitive by default, because a whitespace analyzer splits terms on whitespace.
- You can use terms, phrases, Boolean operators, fields, grouping and modifiers.
- Pattern matching: wildcards, fuzzy search, proximity search and regular expressions.
- Range searches cover numeric and date values within boundaries.
- Reserved characters must be escaped to be searched literally.

Parsing, tokenization and query limits all affect results. If a result is unexpected, review the page's common errors section.

Details from the page:
- Unquoted terms with no operator are OR-connected: `ssh login failed` means `ssh OR login OR failed`. Quote a phrase for an exact sequence (also case-sensitive).
- Operators `AND`, `OR`, `NOT` must be uppercase; `+` and `-` are the short forms of required and excluded.
- Search a field with `field:value`, group values with `type:(ssh OR login)`, and test existence with `_exists_:field`.
- Case-insensitive search: use wildcards such as `*error*`, or regex with a case-insensitive flag.
- Leading wildcards are disabled by default (`allow_leading_wildcard_searches = true` in `graylog.conf` enables them, not recommended in production). The default maximum clause count is 32,768.
- Ranges: `[400 TO 500]` inclusive, `{400 TO 500}` exclusive, mixed `[400 TO 500}`, and `>400`, `<=400` style one-sided forms. The time picker range must still cover any dates in the query. Relative values such as `[now-5d TO now-4d]` work.
- Fuzzy `roam~` or `roam~1`; proximity `"ssh login"~5`; regex goes between slashes, for example `user_name:/.*\$/`, and cannot be used on analyzed fields (`source`, `message`, `full_message`).
- Characters to escape with a backslash: `& | : \ / + - ! ( ) { } [ ] ^ " ~ * ?`.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/making_sense_of_your_log_data/search_syntax_reference.htm (read in full, Graylog 7.2 docs). Dropped the earlier line about saved searches, search filters and export, which the page does not describe beyond links.
