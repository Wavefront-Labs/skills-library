---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-web-filter-profiles
name: fortigate-web-filter-profiles
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [web-filter, fortios, webfilter, fortiguard-category, urlfilter, safe-search, static-url-filter]
level: practitioner
status: draft
description: "Build a FortiGate web filter profile with FortiGuard categories, static URL lists and safe search, and diagnose rating lookups."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: category-based web access control with explicit exceptions.

```
config webfilter urlfilter
    edit 1
        set name "allowlist"
        config entries
            edit 1
                set url "partner.example.com"
                set type simple
                set action exempt
            next
        end
    next
end
config webfilter profile
    edit "wf-std"
        set feature-set flow
        config ftgd-wf
            config filters
                edit 1
                    set category 26
                    set action block
                next
            end
        end
        set web-url-filter-table 1
    next
end
```
Category 26 is Malicious Websites in current releases (confirm via `?`). Static URL filter entries (simple, wildcard, regex) apply before or after FortiGuard rating depending on configuration (static filter is processed first); `exempt` skips remaining filters.

Gotchas
- HTTPS filtering without deep inspection uses SNI/certificate CN only, so path-level rules do not match.
- `Rating errors` (FortiGuard unreachable) can allow or block; set `set options rate-server-ip` and the failure action deliberately.
- Different FortiOS versions renumber or rename categories; export and compare when upgrading.

## Verify
```
diagnose debug rating
diagnose webfilter fortiguard statistics list
```
`diagnose debug rating` shows the rating server and status; test a blocked category URL from a client and check the web filter log.
