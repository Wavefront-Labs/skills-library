---
id: computing-software.cloud-infrastructure-engineering.openbao.policy-path-matching
name: policy-path-matching
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, wildcard, glob, path-matching, policy]
level: practitioner
status: docs-checked
description: "How OpenBao policy paths match: the trailing * glob, the + segment wildcard, priority among overlapping paths, canonical paths."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/policies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy path matching

- `*` is a prefix glob and must be the final character of a path. It is not a regular expression.
- `+` matches any characters within a single path segment.

## When several paths match

The most specific one applies. Priority depends on where the first wildcard appears, whether the path ends in `*`, the number of `+` segments, path length, and lexical order.

- Identical patterns across policies combine their capabilities.
- Different matching patterns use only the highest-priority match, so the lower-priority policy's path is not used for that request.

## Canonical paths

Policy paths must use the engine's canonical form, usually lowercase. Inbound request paths are canonicalized, but paths written in a policy are not, so a non-canonical policy path will mismatch.

## Gotchas

- `deny` takes precedence over any other capability defined for the matching path, including `sudo`.
- Root-protected endpoints need a root token or `sudo`.

## Checked

2026-11-04. Read the OpenBao policies concepts page in full. Confirmed: `*` only as the last character and not a regular expression, `+` within one segment, the five priority rules, union of identical patterns versus highest-priority match, canonical path warning, `deny` precedence and root-protected paths needing a root token or `sudo`. Removed: a `bao token capabilities` section the page does not mention, the claim that `deny` ignores path specificity, and a speculation about silent failures.
Method: documentation only; no commands were run.
