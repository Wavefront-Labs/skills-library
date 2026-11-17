---
id: computing-software.cloud-infrastructure-engineering.external-dns.txt-prefix-suffix-and-wildcards
name: txt-prefix-suffix-and-wildcards
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, txt-prefix, txt-suffix, txt-wildcard-replacement, apex-domain, record-type-placeholder]
level: practitioner
status: docs-checked
description: "Configure ExternalDNS --txt-prefix, --txt-suffix and --txt-wildcard-replacement: apex-domain rules, the 63-byte limit, and why they must never change."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/registry/txt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TXT prefix, suffix and wildcard replacement

Use a prefix or suffix so registry TXT records do not collide with TXT or CNAME records produced by sources. It is added to the first label of the registry record's name.

- `--txt-prefix` and `--txt-suffix` are mutually exclusive.
- Either may contain `%{record_type}`, replaced by the type of the record whose metadata is stored.
- Never change the prefix or suffix after the first deployment: existing registry records are orphaned and the metadata is lost.
- Both count towards the 63-byte maximum record length, so keep them short and use them only when needed.

**Apex domains:** with a prefix, include the type substitution and end it with a period, created under the same domain as the apex record:

```sh
--txt-prefix=someprefix-%{record_type}.
```

A suffix does not work at the apex. `--txt-suffix="-.%{record_type}"` for `ex.com` would give `ex-.a.com`, which is outside the managed zone and fails to create. For `www.ex.com` it gives `www-.cname.ex.com.`.

**Wildcards:** a registry record for `*.example.com` has invalid domain syntax and most providers reject it. `--txt-wildcard-replacement` sets a string that replaces the `*` in registry TXT names.

**Verify:** list the zone's TXT records and confirm each managed record has a matching registry record with the expected prefix and type.

## Checked

2026-11-04. Read the TXT registry page (note on apex domains, Prefixes and Suffixes, Wildcard Replacement, record-format examples). Confirmed the mutual exclusion, %{record_type}, the apex prefix rule, the ex-.a.com failure and the www-.cname.ex.com. result. Reworded the 63-byte limit to the page's wording (maximum record length).

Method: documentation only; no commands were run.
