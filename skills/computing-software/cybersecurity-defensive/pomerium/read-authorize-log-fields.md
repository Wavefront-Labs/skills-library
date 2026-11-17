---
id: computing-software.cybersecurity-defensive.pomerium.read-authorize-log-fields
name: read-authorize-log-fields
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [allow-why-false, deny-why-false, claim-unauthorized, authorization-audit, databroker-version]
level: practitioner
status: docs-checked
description: "Interpret the allow, deny, allow-why and deny-why keys in Pomerium authorization logs to explain why a request was permitted or refused."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/audit-logs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Key meanings in authorize service entries:

- `allow`: true if at least one allow rule passed. If `deny` is also false, the request is allowed.
- `allow-why-true` / `allow-why-false`: short reason strings. `claim-unauthorized` means a policy rule on a claim did not pass. `non-pomerium-route` means the request was not to `/.pomerium/`, which any authenticated user may reach.
- `deny`: true if at least one deny rule passed, so the request is denied.
- `deny-why-true` / `deny-why-false`: reason strings for the deny block.
- `databroker_server_version` and `databroker_record_version`: for auditing. With these numbers and the full history of databroker changes you can determine what data was used for policy evaluation.

The `why` keys are easiest to read through the Pomerium Policy Language rule: a request is allowed to a route if it matches at least one allow rule and zero deny rules. `allow-why-*` reports whether the allow block's requirements were met; `deny-why-*` reports whether a deny block matched.

In the page's example entry, `allow` is false with `allow-why-false` of `claim-unauthorized` and `non-pomerium-route`, and `deny` is false.

## Checked

2026-11-04. Confirmed against the Audit Logs page: meanings of allow, deny, the why keys, claim-unauthorized, non-pomerium-route, databroker version keys, and the PPL allow/deny rule. Replaced an inferred example reading with the page's own example entry.

Method: documentation only; no commands were run.
