---
id: computing-software.cybersecurity-defensive.pomerium.ppl-device-and-record-matchers
name: ppl-device-and-record-matchers
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [device-matcher, record-matcher, external-data, enclave-only, device-approved]
level: advanced
status: docs-checked
description: "Use the PPL device matcher (is, approved, type) and the Enterprise record matcher for external data sources in Pomerium policies."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/ppl.mdx
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/native-ssh-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Device matcher** (criterion `device`)
- `is`: exact device ID. Users find their device IDs at the `/.pomerium` endpoint.
- `approved`: Enterprise only.
- `type`: `enclave_only` for platform authenticators, `any` to include hardware security keys too.

**Record matcher** (criterion `record`, Enterprise Console only, for external data sources)
- `type`: the Record Type set in the Enterprise Console.
- `field`: field name from the data source.
- `exists`: boolean, true if the record is found. It does not need `field`.
- Numeric comparisons: `<`, `<=`, `=`, `>`, `>=`.
- String and string-list matcher operators also work.

**String list matcher** (used by `groups` and `record`): key `has` checks whether a string is in a list. A direct value behaves like `has`.

On SSH routes the `device` criterion does not apply, while `record` is available on SSH routes in Enterprise only.

## Checked

2026-11-04. Read the Pomerium Policy Language page and the Native SSH Access page: device operators and types, record matcher keys, exists operator, numeric operators, string list matcher, and the SSH applicability notes all confirmed. Nothing removed.

Method: documentation only; no commands were run.
