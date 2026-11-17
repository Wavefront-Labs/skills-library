---
id: computing-software.networking-hardware-and-wireless.unbound.dnssec-failure-diagnosis-and-permissive-mode
name: dnssec-failure-diagnosis-and-permissive-mode
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, dnssec, val-log-level, val-permissive-mode, ignore-cd-flag, bogus, unbound-host]
level: practitioner
status: docs-checked
description: "Diagnose DNSSEC validation failures in Unbound with val-log-level, flush_bogus and unbound-host -v, and know what permissive mode and ignore-cd-flag change."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-host.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnssec failure diagnosis and permissive mode
- `val-log-level` (default 0) logs validation failures regardless of verbosity: 1 logs each failed user query, 2 also logs the reason and the server that sent the faulty data. It can be set at runtime with `set_option`.
- `unbound-host -v name` adds secure, insecure or bogus to each line; `-D` uses the root anchor, `-y` supplies a DS or DNSKEY.
- `unbound-control flush_bogus` removes bogus data from the cache; `num.answer.bogus` and `num.rrset.bogus` count failures with extended statistics.
- `val-permissive-mode: yes` (default no) returns bogus results as indeterminate instead of SERVFAIL, so the client receives the bogus data; the checks and logging still run, and AD is set only for secure results.
- `ignore-cd-flag: yes` (default no) ignores the client CD flag and refuses bogus answers.
- `val-bogus-ttl` (60 s) controls how long bogus results are cached.
- `log-servfail: yes` logs why SERVFAIL was returned.

Unbound-host exit code 0 means no error but the data may still be unavailable; 1 means a fatal error.

## Checked

2026-11-08. Read val-log-level, val-permissive-mode, ignore-cd-flag, val-bogus-ttl and log-servfail in the unbound.conf manual, the unbound-host manual in full, and flush_bogus, set_option and the bogus counters in unbound-control. Clarified that permissive mode hands the bogus data to the client.

Method: documentation only; no commands were run.
