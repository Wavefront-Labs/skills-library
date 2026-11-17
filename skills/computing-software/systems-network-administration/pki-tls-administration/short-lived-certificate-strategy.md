---
id: computing-software.systems-network-administration.pki-tls-administration.short-lived-certificate-strategy
name: short-lived-certificate-strategy
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [short-lived-certificate-strategy, pki-crlite, short-lived-certs, revocation-strategy, acme-profiles, 6-day, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Use very short certificate lifetimes backed by ACME automation to shrink the compromise window, using Let's Encrypt's six-day and IP certificate design."
sources:
  - https://letsencrypt.org/2025/01/16/6-day-and-ip-certs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Short-lived certificates instead of revocation
Goal: shrink the exposure window so revocation matters less.

What Let's Encrypt states (announcement of 16 January 2025, updated 15 January 2026):
- Six-day and IP address certificates are now generally available (per the page's update note; the linked general-availability post was not read).
- Rationale: revocation has historically been unreliable, so a compromised-key certificate may keep being used until it expires. The longer the lifetime, the longer that window. Short-lived certificates greatly reduce the window and the need for revocation.
- Six-day certificates do not include OCSP or CRL URLs.
- The 90-day certificates remain available alongside the six-day option.
- Opt-in is through a certificate profile in the ACME API: use an ACME client that supports ACME certificate profiles and select the short-lived profile. Requesting an IP address automatically selects a short-lived profile.
- IP address certificates carry the address as a Subject Alternative Name. Validation for IP addresses is limited to the http-01 and tls-alpn-01 challenges; dns-01 is unavailable because DNS is not involved, and there is no CAA check for IP addresses.
- Short-lived certificates practically require automation. The announcement's advice: first make sure your ACME client renews reliably; if it does, switching should cost nothing.

Planning points (operational judgement, not figures from the page):
- Pick the renewal interval and failure budget from the certificate lifetime, and monitor renewal success rather than waiting for expiry.
- Keep a tested path for CA or ACME outages.
- Keep revocation processes for long-lived certificates, such as client and CA certificates.

Verify:
- [ ] The ACME client supports certificate profiles and renews unattended.
- [ ] Renewal failures alert well before the remaining lifetime runs out.

## Checked
Checked against the Let's Encrypt announcement page (full text).
Removed: the claim that the Baseline Requirements let certificates under 7 days omit CRL/OCSP, step-ca and Vault TTL figures, the renewal fractions and 8-hour schedule, the 99.9 percent target and the clock-skew threshold (none are on the cited page).
Method: docs-only read of cited pages, 2026-11-08
