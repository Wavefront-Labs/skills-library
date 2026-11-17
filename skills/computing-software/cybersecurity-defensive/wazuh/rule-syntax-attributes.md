---
id: computing-software.cybersecurity-defensive.wazuh.rule-syntax-attributes
name: rule-syntax-attributes
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [rule-syntax, frequency, timeframe, noalert, if-matched-sid, same-field, rules-xml]
level: advanced
status: docs-checked
description: "Wazuh rule XML reference: attributes and ranges, match and regex options, if_ and same_ conditions, and gotchas."
sources:
  - https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Attributes on `<rule>`:
- `level`: 0 to 16.
- `id`: 1 to 999999.
- `maxsize`: 1 to 9999.
- `frequency`: 2 to 9999 matches before an alert fires.
- `timeframe`: 1 to 99999 seconds, used with `frequency`.
- `ignore`: 1 to 999999 seconds of suppression after a trigger.
- `overwrite`: yes/no; replaces a rule with local changes.
- `noalert`: 0 (default) or 1; with 1 the event still passes through other rules.

Options:
- `match` / `regex`: default types osmatch and osregex; attributes `negate` (default no) and `type` (osmatch, osregex, pcre2).
- Field tags such as `decoded_as`, `srcip`, `dstip`, `srcport`, `user`, `program_name`, `id`, `url`, `location`: multiple `field` tags are ANDed.
- `if_sid`, `if_group`, `if_level`, `if_matched_sid`, `if_matched_group`: parent or correlation conditions; the `if_matched_*` forms need the match within a timeframe.
- `same_*` and `different_*`: require a decoded field to match or differ.
- `time` and `weekday`: evaluated against Wazuh server time, not the event timestamp.
- `list`: CDB list path. `var`: defines variables such as BAD_WORDS.

Gotchas:
- Repeated `match`/`regex` labels concatenate; attributes come from the last label.
- Every rule must belong to at least one group.
- Always give custom rules a `description`.
- Overwrite rules ignore the `if_*` labels.

## Checked

2026-11-08. Read the whole Rules Syntax page. Confirmed: all rule attribute ranges and defaults (level, id, maxsize, frequency, timeframe, ignore, overwrite, noalert), match and regex types and negate, field AND behaviour, if_ and same_/different_ options, time and weekday using server time, list, var and BAD_WORDS, concatenation rule, mandatory group, description advice, overwrite ignoring if_* labels. Nothing removed.
Method: documentation only; no commands were run.
