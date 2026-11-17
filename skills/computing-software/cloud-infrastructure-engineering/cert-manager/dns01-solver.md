---
id: computing-software.cloud-infrastructure-engineering.cert-manager.dns01-solver
name: dns01-solver
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [dns01, cnamestrategy, delegation, dns01-recursive-nameservers, wildcard, split-horizon]
level: practitioner
status: docs-checked
description: "Configure cert-manager DNS01 solvers: provider blocks, selectors, cnameStrategy Follow delegation, the wildcard CNAME trap and self-check nameserver flags."
sources:
  - https://cert-manager.io/docs/configuration/acme/dns01/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Configuration sits at `spec.acme.solvers[].dns01` with one provider block per solver. One Issuer can hold several providers, even two instances of the same one. `selector.dnsZones` restricts a solver to zones. Built-in providers: ACMEDNS, Akamai, AzureDNS, CloudFlare, Google, Route53, DigitalOcean, RFC2136; others run as external webhooks.

`cnameStrategy`: `None` (default) or `Follow`. With `Follow`, cert-manager follows CNAMEs at `_acme-challenge.<domain>` to find the zone to update. Delegation: CNAME `_acme-challenge.example.com` to `_acme-challenge.less-privileged.example.org`, give the solver credentials for the target zone, and keep the selector on the original domain.

Wildcard trap with `Follow`: a wildcard such as `*.example.com CNAME lb.example.org` is followed too, so cert-manager tries to write the TXT at `lb.example.org` and the provider rejects it (Route 53: RRSet not permitted in the zone). Fix by adding an explicit `_acme-challenge.<domain>` record, or leave `cnameStrategy: None`.

Self-check: by default the controller reads recursive resolvers from `/etc/resolv.conf`, finds the authoritative nameservers and queries them directly.
- `--dns01-recursive-nameservers`: comma-separated `host:port` list, e.g. `8.8.8.8:53,1.1.1.1:53`.
- `--dns01-recursive-nameservers-only`: verify only through recursive resolvers; can be slower because of caching.
Use these with split-horizon DNS or several authoritative servers. In Helm, set them via `extraArgs` and escape commas as `\,`.

## Checked

2026-11-03. Confirmed on the cert-manager DNS01 page (configuration/acme/dns01): solver location, multiple providers, built-in provider list, cnameStrategy values and delegation example, wildcard CNAME warning, self-check flags and Helm comma escape. Nothing removed.
Method: documentation only; no commands were run.
