---
id: computing-software.cybersecurity-defensive.pomerium.threat-model-and-cookie-stripping
name: threat-model-and-cookie-stripping
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [threat-model, vulnerability-disclosure, clean-upstream-lua, encryption-at-rest, security-reporting]
level: practitioner
status: docs-checked
description: "Understand Pomerium's security scope and threat model, how it strips its session cookie upstream, and how to report a vulnerability."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**In scope**: authentication (Pomerium is not an IdP; it checks each request has a valid session from a trusted provider); cookie handling (the `_pomerium` cookie is removed before forwarding upstream by the `clean-upstream.lua` script, with no configuration, preventing token leakage to backends); authorization (HTTP per request, TCP per session); encryption in transit when certificates are provided; encryption at rest of databroker data and service secrets; availability (inherits Envoy's model); auditability.

**Out of scope**: a compromised trusted provider (user impersonation), memory analysis of a running instance, control of the storage backend, an upstream's own access control, physical access.

**Encryption at rest**: hosted services use AES-256 or stronger block storage plus AES-256-GCM field-level encryption. Enterprise console uses XChaCha20-Poly1305 with random nonces and checks the tag on read; customers encrypt their block storage.

**Reporting**: email security@pomerium.com. Acknowledgement within 48 hours, detailed response within 72 hours. No paid bounty. Avoid DoS, spam, social engineering and physical attacks. Subscribe to pomerium-announce; security mails carry a "[security]" prefix.

## Checked

2026-11-04. Confirmed against the Security and Threat Model page: in and out of scope lists, _pomerium cookie stripping by clean-upstream.lua, per-request HTTP and per-session TCP authorization, at-rest encryption details, disclosure contacts and timings. Removed the databroker-backends caveat, which this page does not state (it says all databroker data is encrypted).

Method: documentation only; no commands were run.
