---
id: computing-software.cybersecurity-defensive.falco.domain-name-fields-fd-sip
name: domain-name-fields-fd-sip
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [fd-sip-name, fd-cip-name, dns-resolution, network-rules, domain-ioc]
level: advanced
status: docs-checked
description: "Use fd.sip.name style fields correctly: domains resolve at rule load, refresh on a 10 to 320 second schedule, with operator and output limits."
sources:
  - https://falco.org/docs/concepts/rules/fd-sip-name/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`fd.sip.name` (server IP) and the related `fd.cip.name` (client IP) and similar `fd.*ip.name` fields compare an event's IP against the addresses of a domain. Example for crypto mining pools:

```yaml
- macro: minerpool_https
  condition: (fd.sport="443" and fd.sip.name in (https_miner_domains))
```

How it works: the domain names on the right of the comparison are saved in the engine, the A records are looked up at once, and the IP set is stored. When a syscall event is evaluated, its actual IP is compared with that set. Lookups run on a separate thread so the event loop is not stalled.

Refresh: the base refresh time is 10 seconds. If addresses do not change in a refresh cycle, the timeout doubles up to 320 seconds.

Caveats:
- The right side must be a resolvable domain name, so substring or wildcard domains are not possible.
- Only `=`, `!=` and `in`, optionally with a preceding `not`, are allowed.
- In outputs, `%fd.sip.name` has a meaningful value only when the IP matched the domain. With a negative match like `fd.sip.name!=yahoo.com`, the output field is blank; use `%fd.name` for the connection.

Gotcha: a domain that does not resolve at rule load time cannot match anything, so verify names before deploying.

## Checked

2026-11-08. Read the fd.sip.name page in full; claims match (resolve at load, 10 to 320 second refresh, =, != and in only). Reworded nothing material.

Method: documentation only; no commands were run.
