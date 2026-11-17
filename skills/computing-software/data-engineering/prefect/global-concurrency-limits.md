---
id: computing-software.data-engineering.prefect.global-concurrency-limits
name: global-concurrency-limits
category: computing-software
field: data-engineering
product: prefect
tags: [concurrency, rate-limit, lease, slots, slot-decay]
level: practitioner
status: docs-checked
description: "Use Prefect global concurrency limits and rate limits: slots, lease duration and renewal failure options, slot decay, active versus inactive."
sources:
  - https://docs.prefect.io/v3/concepts/global-concurrency-limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: throttle any Python operation across flows.

Limits use slots: an operation requests one or more, blocking until free. A limit can be active (enforced) or inactive (exists, never blocks), toggled without code changes.

`concurrency` context manager:
- Holds a slot for the whole block and releases on exit.
- Lease duration defaults to 5 minutes; custom durations have a minimum of 1 minute.
- The client renews the lease while in use; if renewal stops the slot is released, preventing deadlocks when a process dies.
- `strict` (default `False`): `True` stops execution on renewal failure.
- `raise_on_lease_renewal_failure` (default `None`): `True` terminates, `False` continues, `None` follows `strict`.
- With defaults a warning is logged and execution continues. `strict=True` plus `raise_on_lease_renewal_failure=False` enforces acquisition but tolerates transient renewal errors.

`rate_limit` function:
- Occupies a slot briefly, then it decays automatically at `slot_decay_per_second`.
- The limit must have slot decay configured or the call raises.
- `slot_decay_per_second=5.0` is about one operation every 0.2 s; `0.1` is about 10 s between operations.

Unlike work pool, work queue, deployment and tag-based limits (scoped to Prefect objects), global limits apply to any Python code. Typical uses: database connection pool size, memory-heavy work, external API rate limits.

## Checked
2026-11-08. Confirmed against the Global concurrency limits concept page: slots, active and inactive states, concurrency context manager, 5 minute default and 1 minute minimum lease, strict and raise_on_lease_renewal_failure behaviour, rate_limit with slot decay, the 5.0 and 0.1 decay examples, and comparison with other limit types. Nothing removed.
Method: documentation only; no commands were run.
