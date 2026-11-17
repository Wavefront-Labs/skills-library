---
id: computing-software.systems-network-administration.network-design.tls-inspection-design
name: tls-inspection-design
category: computing-software
field: systems-network-administration
product: network-design
tags: [firewall, tls-inspection, ssl-inspection, ssl-decryption, certificate-pinning, ngfw, swg, privacy]
level: practitioner
status: docs-checked
description: "Plan TLS inspection on firewalls or secure web gateways: forward-proxy CA deployment, bypass categories, pinned apps, TLS 1.3/QUIC handling, performance sizing, and legal limits."
sources:
  - https://www.cisa.gov/news-events/alerts/2017/03/16/https-interception-weakens-tls-security
  - https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/decryption
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS inspection design

Malware delivery and C2 can hide inside TLS. Inspection (forward-proxy decryption) lets IPS, AV and
DLP see it, at the cost of complexity, performance and some breakage.

## How it works
The firewall/SWG terminates the client's TLS with a certificate it mints on the fly, signed by an
internal inspection CA, and opens its own TLS session to the server. Clients must trust the
inspection CA.

## Prerequisites
- Issue a dedicated subordinate CA for inspection from your PKI (never reuse the root key on a
  firewall). Deploy it to the trust store via GPO/MDM; also to applications that keep their own trust stores.
- Decide how sites with invalid certificates are handled, so users still see warnings.

## Bypass list (do not decrypt)
- Categories: financial services and health (the Palo Alto decryption guide gives a no-decryption rule for financial or healthcare data), plus any category your privacy/legal policy names.
- Certificate-pinned and mutual-TLS apps: OS updates, many mobile apps, and agents that pin certificates.
- Keep the bypass list maintained with owners; most "the app broke" tickets end up here.

## Protocol realities
- TLS 1.3: check your device's decryption support for it.
- QUIC/HTTP3 runs over UDP rather than TCP: confirm whether your device can inspect it and decide policy accordingly.

## Sizing
Decryption is resource-intensive (the Palo Alto guide warns that decrypting all traffic indiscriminately can be). Size from vendor "threat prevention
with decryption" numbers, not firewall throughput. Start with user web traffic, not server or
backup traffic.

## Legal and HR
Inform users (acceptable use policy), check works council/privacy law requirements in each
country, and restrict who can view decrypted data in logs.

## Verify
- [ ] Browsing a test site shows the inspection CA as issuer; bypassed categories show the real
  issuer; pinned apps on the bypass list work.

## Checked

- Date: 2026-10-28
- Confirmed: Palo Alto PAN-OS decryption guide: SSL Forward Proxy inspects outbound traffic, a no-decryption rule can bypass financial or healthcare data, indiscriminate decryption is resource-intensive.
- Removed: trust-store product list, forward-trust/untrust wording, pinned-app list, Microsoft no-inspection claim, TLS 1.3, QUIC and ECH statements, throughput factor (CISA page blocked).
Method: documentation only; no commands were run.
