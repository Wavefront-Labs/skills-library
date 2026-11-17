---
id: computing-software.networking-hardware-and-wireless.caddy.acme-server-internal-ca
name: acme-server-internal-ca
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [acme-server, internal-ca, pki, lifetime, challenges, allow-deny, private-ca, caddyfile]
level: advanced
status: docs-checked
description: "Run an ACME server inside Caddy with acme_server: ca id, certificate lifetime rule, challenges, wildcard names, allow and deny policy, and the validate database lock."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/acme_server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: issue certificates to other ACME clients (including other Caddy servers) from your own CA.

Requests matching `/acme/*` are handled by the server. Clients use `https://localhost/acme/local/directory` by default, where `local` is the default CA id.

Syntax: `acme_server [<matcher>] { ca <id>  lifetime <duration>  resolvers <resolvers...>  challenges <challenges...>  allow_wildcard_names  allow { domains ...  ip_ranges ... }  deny { domains ...  ip_ranges ... } }`.
- `ca`: CA id, default `local` (self-signed dev CA); name a different CA for broader use, created if missing, configured in the PKI global options.
- `lifetime`: default `12h`. It must be less than `renewal_window_ratio x intermediate_lifetime` of the signing intermediate; if you raise it, raise `intermediate_lifetime` too, otherwise a leaf can outlive its signing intermediate and the chain becomes invalid until renewal.
- `resolvers`: DNS servers for dns-01 TXT lookups (UDP port 53 by default; one chosen at random).
- `challenges`: any of http-01, tls-alpn-01, dns-01; all enabled when omitted.
- `allow_wildcard_names`: permit wildcard SANs. `allow` and `deny` apply policy per Step-CA's evaluation rules, on domains and IP ranges.

Example: `pki { ca home { name "My Home CA" } }` globally; then `acme.example.com { tls { issuer internal { ca home } }  acme_server { ca home } }`. A client Caddy sets `acme_ca https://acme.example.com/acme/<ca-id>/directory with the id from `ca`` and `acme_ca_root /path/to/home_ca_root.crt`.

Operational trap: the ACME server holds an on-disk database that only one process may open, so `caddy validate` fails with a database timeout while Caddy serves this config. Validate before starting, or use `caddy reload`, which provisions inside the running process and keeps the active config if provisioning fails.

## Checked

2026-11-03: read caddyfile/directives/acme_server against this skill. Confirmed: syntax, ca default local, lifetime default 12h and its renewal_window_ratio x intermediate_lifetime limit, resolvers, challenges, allow_wildcard_names, allow/deny, validate-versus-reload caveat.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
