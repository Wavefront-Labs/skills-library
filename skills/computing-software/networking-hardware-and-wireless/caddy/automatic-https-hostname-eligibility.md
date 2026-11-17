---
id: computing-software.networking-hardware-and-wireless.caddy.automatic-https-hostname-eligibility
name: automatic-https-hostname-eligibility
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [hostname-requirements, certificate-eligibility, wildcard, localhost, ip-address, public-ca, automatic-https]
level: practitioner
status: docs-checked
description: "Check whether a hostname qualifies for a managed or publicly trusted certificate in Caddy: allowed characters, localhost TLDs, IPs and single left-most wildcard."
sources:
  - https://caddyserver.com/docs/automatic-https
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand why one name gets a public cert and another a local one.

A hostname qualifies for a fully managed certificate if it is non-empty, consists only of alphanumerics, hyphens, dots and the wildcard `*`, and does not start or end with a dot (RFC 1034).

It additionally qualifies for a publicly trusted certificate only if it is not localhost (including the `.localhost`, `.local`, `.internal` and `.home.arpa` TLDs), is not an IP address, and has at most a single wildcard as the left-most label.

Consequences from the page: non-public hosts such as `127.0.0.1` and `localhost` are still served over HTTPS using Caddy's own CA; IP addresses generally do not qualify for public certificates (some CAs can issue them, but not by default), so they are also served from the local CA unless HTTPS is disabled.

Wildcards: only the left-most label may be a wildcard. `*.example.com` qualifies; `sub.*.example.com`, `foo*.example.com`, `*bar.example.com` and `*.*.example.com` do not, a restriction of the WebPKI.

Practical check: if a name you expect to be public is being served with a "Caddy Local Authority" certificate, test it against these rules (a `.home.arpa` or `.internal` suffix is a common cause).

## Checked

2026-11-03: read automatic-https against this skill. Confirmed: RFC 1034 name rules, localhost/.local/.internal/.home.arpa exclusions, IP addresses, left-most-only wildcard and the example names.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
