---
id: computing-software.cloud-infrastructure-engineering.cert-manager.dns01-acme-dns
name: dns01-acme-dns
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [acme-dns, acmedns, dns01, cname, accountsecretref, max-concurrent-challenges]
level: practitioner
status: docs-checked
description: "Use the acme-dns server with cert-manager DNS01: pre-register an account, restrict allowfrom, create the CNAME and Secret, and avoid the 2-domain limit."
sources:
  - https://cert-manager.io/docs/configuration/acme/dns01/acme-dns/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Issuer: `spec.acme.solvers[].dns01.acmeDNS` with `host` (e.g. `https://acme.example.com`) and `accountSecretRef` (`name: acme-dns`, `key: acmedns.json`).

Registration is manual because cert-manager cannot register interactively:
1. `curl -X POST http://auth.example.com/register` returns `username`, `password`, `fulldomain`, `subdomain`, `allowfrom`.
2. Strongly recommended: restrict updates by posting JSON `{"allowfrom": ["10.244.0.0/16"]}`, matching your pod range.
3. Build `acmedns.json`: an object keyed by domain (e.g. `example.com`), each value holding the registration fields. One credential set can cover several domains.
4. Create DNS: `_acme-challenge.example.com CNAME <fulldomain>`; the value must equal `fulldomain` exactly.
5. `kubectl create secret generic acme-dns --from-file acmedns.json`.

Namespaces: an Issuer and its Secret share a namespace; for a ClusterIssuer the Secret goes in `cert-manager`.

Known limit: with more than two domains on one credential set (for example `example.com`, `*.example.com` and `foo.example.com`) DNS01 may solve only two, non-deterministically. Workarounds:
- use separate credential sets so each acme-dns subdomain serves at most two challenged names;
- run the controller with `--max-concurrent-challenges 2` so only two TXT records exist in acme-dns at once.

## Checked

2026-11-03. Confirmed on the cert-manager ACMEDNS page (configuration/acme/dns01/acme-dns): issuer fields, manual registration, allowfrom recommendation, acmedns.json layout, CNAME rule, Secret namespace rules, the more-than-two-domains limitation and both workarounds. Nothing removed.
Method: documentation only; no commands were run.
