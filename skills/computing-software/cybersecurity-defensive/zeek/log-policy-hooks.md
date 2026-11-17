---
id: computing-software.cybersecurity-defensive.zeek.log-policy-hooks
name: log-policy-hooks
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, log-policy, log-stream-policy, veto-record, log-delay]
level: advanced
status: docs-checked
description: "Veto or modify Zeek log records with Log::log_stream_policy and per-filter policy hooks, and defer writes for enrichment with Log::delay and Log::delay_finish."
sources: ["https://docs.zeek.org/en/current/frameworks/logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# log policy hooks

Two hook levels decide whether a record is written. The global `Log::log_stream_policy` runs first, once per write. Then each filter's `policy` hook (type `Log::PolicyHook`) runs. A handler that executes `break` vetoes the write for that filter. Streams should define a default hook and pass it as `$policy`:

```
global log_policy: Log::PolicyHook;
Log::create_stream(Foo::LOG, [$columns=Info, $path="foo", $policy=log_policy]);

hook Foo::log_policy(rec: Foo::Info, id: Log::ID, filter: Log::Filter)
    {
    if ( rec$missed_bytes > 0 )
        break;
    }
```

Shipped streams have such hooks, for example `HTTP::log_policy`. Setting `$policy` on a new filter replaces the stream hook for that filter, so prefer checking `filter$name` inside the default hook. Hooks may modify the record, but the same record passes through all filters in unspecified order, so changes persist.

**Delaying** (marked as added in 6.2): inside `Log::log_stream_policy`, call `Log::delay(id, rec)` to hold a write while async work (such as a `when` lookup) completes, then `Log::delay_finish(id, rec, token)` once per delay call. The record sits after the global hook and before filter hooks. The maximum delay is `Log::default_max_delay_interval` (per stream via `Log::set_max_delay_interval`). Delayed records are lost if a worker crashes. Move discard logic into the stream policy to avoid delaying records that will be dropped.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
