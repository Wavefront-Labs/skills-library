---
id: computing-software.systems-network-administration.headscale.pending-registration-limits
name: pending-registration-limits
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, register-cache, http-503, retry-after, pending-auth]
level: advanced
status: docs-checked
description: "Limits on pending registrations: the 1024-entry cache, 503 Retry-After at capacity, the 64 KiB payload cap, and single-use OIDC state."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/registration.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pending authentication limits

Admitted registration requests are kept until they complete or expire.

- Default allocation: 1024 entries, adjustable:

```yaml
tuning:
  register_cache_max_entries: 1024
```

- At capacity, new requests get HTTP 503 with `Retry-After`. Existing approvals and pre-authenticated key registrations remain available.
- SSH checks have 64 reserved entries beyond the allocation, including in the OIDC state cache.
- Pending registrations keep only hostname, OS and requested tags from Hostinfo; other metadata arrives with the node's first MapRequest.
- A serialised registration must fit in 64 KiB; larger payloads are rejected, not truncated. Noise registrations return HTTP 200 with `RegisterResponse.Error` (the client shows the permanent size error); the admin API reports HTTP 413.
- At the default, retained payloads use at most 64 MiB plus overhead (cache storage only).
- OIDC login URLs must reference an existing pending authentication of the matching type.
- OIDC callback state is single-use, even if the identity provider exchange fails: restart the browser login after an error.

## Gotcha

Capacity limits protect admitted requests but cannot guarantee admission during sustained overload. Pre-authenticated key registration remains available when capacity is reached.

## Checked

2026-11-04. Confirmed against the Headscale registration reference (Pending authentication limits) and config-example.yaml. Removed an unsourced recommendation about bulk enrolment.
Method: documentation only; no commands were run.
