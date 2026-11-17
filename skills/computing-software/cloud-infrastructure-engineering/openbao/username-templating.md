---
id: computing-software.cloud-infrastructure-engineering.openbao.username-templating
name: username-templating
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, username-template, templating, random, truncate]
level: practitioner
status: docs-checked
description: "Write OpenBao username templates in Go template syntax with DisplayName, RoleName and the random, truncate, timestamp and hash functions."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/username-templating.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Username templating

Go template language. Fields need a leading dot (`{{.DisplayName}}`); functions do not (`{{random 20}}`). The database engine example provides `DisplayName` and `RoleName`; other engines may differ, so check each.

## Functions

- Strings: `lowercase`, `uppercase`, `replace` (`{{.FieldName | replace - _}}`), `truncate` (`{{.FieldName | truncate 10}}`), `truncate_sha256` (truncates, then swaps the last 8 characters for the first 8 of the removed text's SHA256)
- Generators: `random` (letters and numbers), `timestamp` (Go time layout, e.g. `{{timestamp "2006-01-02T15:04:05Z"}}`), `unix_time`, `unix_time_millis`, `uuid`
- Hashing: `base64`, `sha256`

## Examples

```
{{.DisplayName}}_{{.RoleName}}
{{printf "v_%s_%s_%s_%s" (.DisplayName | truncate 8) (.RoleName | truncate 8) (random 20) (unix_time) | truncate 45}}
```

The second caps the final name at 45 characters, useful for database username limits.

## Warnings

- Include enough randomness for uniqueness, or concurrent credential requests can interfere with each other.
- A template without randomness, like the first, is not suitable for dynamic usernames.

## Checked

2026-11-04. Confirmed against the Username templating page: Go template language, leading dot for fields and none for functions, DisplayName and RoleName from the database example, all listed functions with their examples, the 45-character truncation example and the randomness warnings. Nothing removed.

Method: documentation only; no commands were run.
