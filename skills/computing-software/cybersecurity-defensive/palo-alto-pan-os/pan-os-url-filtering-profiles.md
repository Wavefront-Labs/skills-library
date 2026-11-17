---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-url-filtering-profiles
name: pan-os-url-filtering-profiles
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [url-filtering, pan-os, url-categories, advanced-url-filtering, custom-url-category, credential-phishing, safe-search]
level: practitioner
status: draft
description: "Configure PAN-OS URL filtering profiles by category, custom URL lists, safe search and credential phishing protection, and test categorisation."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/url-filtering"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: control web access by category with predictable exceptions.

```
configure
set profiles custom-url-category allowed-partners type "URL List" list [ "partner.example.com/" "*.partner.example.com/" ]
set profiles url-filtering UF-STD block [ malware phishing command-and-control ] alert [ social-networking ] allow [ allowed-partners ]
set profiles url-filtering UF-STD enable-container-page yes
set profile-group PG-STANDARD url-filtering UF-STD
commit
```
Attach via the rule profile setting or the profile group, and the rule must allow web-browsing/ssl so URL filtering sees the traffic.

Behaviours
- Action order when multiple categories match a URL: block beats allow beats alert, and custom categories take precedence over predefined ones.
- HTTPS filtering without decryption uses SNI/CN only; with decryption it sees the full URL path.
- Credential phishing prevention can block entry of corporate credentials to non-approved categories (needs User-ID group mapping or domain credential detection, confirm mode).

Gotchas
- URL wildcard syntax: trailing `/` and `*` rules differ; `example.com/` matches only the host root, use `example.com/*` for paths (confirm).
- Cloud lookup failures fall back to the local cache; check connectivity to the URL cloud through the management or service route.

## Verify
```
test url www.example.com
show running url-cache statistics
```
The `test url` output should name the category; also confirm with a URL filtering log entry.
