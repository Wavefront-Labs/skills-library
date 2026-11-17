---
id: computing-software.cloud-infrastructure-engineering.openbao.pki-secrets-overview
name: pki-secrets-overview
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, pki, certificates, short-ttl, x509]
level: intro
status: docs-checked
description: "What the OpenBao PKI secrets engine is for, the short-TTL design principle, and which docs pages cover setup, CEL, ACME and rotation."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/secrets/pki/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PKI secrets engine overview

The engine generates dynamic X.509 certificates, removing the manual key, CSR and signing steps. OpenBao's own authentication and authorization verify requesters.

## Design guidance from the docs

- Keep TTLs relatively short: less need for revocation, smaller CRLs.
- Give each application instance its own certificate, avoiding sharing and easing rollover.
- Ephemeral certificates can be fetched at startup, held in memory and discarded at shutdown without touching disk.

## Where to go next (pages in the PKI docs section)

- Setup and Usage (brief setup and issuance)
- Quick Start: Root CA, Intermediate CA
- CEL Guide in PKI (dynamic issue and sign policies)
- Considerations (operating the engine)
- Troubleshooting ACME
- Rotation Primitives
- PKI secrets engine API

## Notice

If OpenBao is a Consul Connect CA, run Consul greater than 1.12.8.

## Checked

2026-11-04. Read the OpenBao PKI secrets engine overview page in full. Confirmed: the short-TTL design reasoning, per-instance certificates, ephemeral in-memory certificates, the list of documentation pages and the Consul note. Removed: a closing sentence of advice the page does not state and a cross-reference to a skill that is not in this folder.
Method: documentation only; no commands were run.
