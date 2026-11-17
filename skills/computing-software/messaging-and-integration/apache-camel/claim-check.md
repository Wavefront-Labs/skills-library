---
id: computing-software.messaging-and-integration.apache-camel.claim-check
name: claim-check
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, claim-check, push-pop, filter]
level: practitioner
status: docs-checked
description: "Camel Claim Check EIP: Set, Get, GetAndRemove, Push and Pop operations, key rules and merge filter include, exclude and remove prefixes."
sources:
  - https://camel.apache.org/components/next/eips/claimCheck-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Claim Check

Stores message content temporarily in an internal memory store and retrieves it later by key. It can also hide sensitive data.

Options: `operation` (required), `key` (required for Get, GetAndRemove, Set), `filter`, `aggregationStrategy`, `aggregationStrategyMethodName`, `disabled` (default false).

Operations:
- `Set`: store under a key, overwriting.
- `Get`: retrieve by key, keep it.
- `GetAndRemove`: retrieve and delete.
- `Push`: put on a stack, no key.
- `Pop`: take the latest from the stack, no key.

`Set` and `Push` leave the body unchanged. Keys can be dynamic with Simple, e.g. `${header.myKey}`. No exchange properties.

Merging on Get or Pop uses an AggregationStrategy; the default uses `filter`. Values: `body`, `attachments`, `headers`, `header:pattern`, comma separated. Patterns support trailing `*` and regex. Prefixes: `+` include (default), `-` exclude (beats include), `--` remove (beats everything). Empty filter or a wildcard merges everything. You cannot mix `+` and `-` on `header:pattern` in one filter.

Examples: Push the original body, transform, then Pop to restore it. `filter="header:(foo|bar)"` merges back only headers `foo` and `bar`.

Verify: Set with key `foo`, then Get twice returns the body both times; GetAndRemove returns it once.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Claim Check EIP page source (claimCheck-eip.adoc) and the Claim Check model definition (claimCheck.json) from the apache/camel repository, which generate the cited page. Confirmed the in-memory store, the five operations and key rules, Set and Push leaving the body unchanged, the filter values and wildcard or regex patterns, the + - and -- prefixes and their precedence, empty or wildcard filter, the include and exclude restriction, dynamic Simple keys, options and the examples. Nothing was removed. No commands were run.
