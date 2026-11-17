---
id: computing-software.cryptography-implementation.protocol-implementation.acme-renewal-information-and-mass-revocation
name: acme-renewal-information-and-mass-revocation
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, certificate-lifecycle, acme-ari, rfc9773, mass-revocation, ca-incident, renewal-window, certbot, lego]
level: advanced
status: docs-checked
description: "Use ACME Renewal Information (ARI, RFC 9773) so CAs can trigger early renewal, and survive CA mass-revocation events (24h/5-day deadlines) without outages."
sources: ["https://datatracker.ietf.org/doc/html/rfc9773", "https://letsencrypt.org/2024/04/25/guide-to-integrating-ari-into-existing-acme-clients/", "https://cabforum.org/working-groups/server/baseline-requirements/requirements/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACME Renewal Information and mass revocation

Under CA/B Forum Baseline Requirements section 4.9.1.1 a CA must revoke a subscriber certificate within 24 hours
for reasons such as key compromise, and for other listed reasons should revoke within 24 hours and must revoke
within 5 days (short-lived certificates are excepted). A CA incident can therefore force revocation of many
certificates at once, and organisations renewing only on a fixed schedule risk outages.

## ARI (RFC 9773)

The CA publishes a suggested renewal window per certificate at the
`renewalInfo` endpoint (advertised in the ACME directory) as a `suggestedWindow`. A CA that needs
certificates replaced early can move the window, and ARI-aware clients renew within it.

- Clients: check your ACME client's documentation for ARI support and how to enable it.
- The client fetches RenewalInfo again as soon as possible after the `Retry-After` time; it must set limits on the
  interval (RFC 9773 suggests treating values under one minute as one minute and over one day as one day) and, after
  a long-term error, retries after about six hours. It then picks a uniform random time inside the window
  (Let's Encrypt integration guide), which also spreads CA load.
- On renewal, the client sends the `replaces` field (the old certificate's ARI identifier) in newOrder. Servers may
  give such orders higher priority or let them bypass rate limits (RFC 9773); Let's Encrypt states ARI renewals
  made inside the window are exempt from its rate limits.

## Be ready for a revocation notice even without ARI

1. Inventory with owner contacts for every certificate (CT monitoring tells
   you what exists; your inventory tells you who renews it).
2. Renewal must be a no-touch operation that can run for all certificates
   within hours: test a "renew everything" run (staging CA) and measure time.
3. Subscribe to CA incident notices (CA status pages, account email) and to CT
   monitoring for your domains.
4. Revocation means TLS clients that check revocation will fail - expired is not the only failure mode.

## Verify

- [ ] ACME client version supports ARI and it is enabled; logs show `renewalInfo` checks.
- [ ] Bulk renewal drill completed well inside the 24-hour revocation deadline for the whole estate.
- [ ] CA incident contact (email/account) monitored by on-call, not an individual.

## Checked
Date: 2026-10-31. Confirmed in RFC 9773 (renewalInfo directory field, suggestedWindow, Retry-After handling and the
one-minute and one-day example limits, six-hour long-term error retry, `replaces`, rate-limit priority), the Let's
Encrypt ARI integration guide (random time in window, rate-limit exemption, `replaces`) and Baseline Requirements
4.9.1.1 (24 hours and 5 days). Removed: the "2/3 of lifetime" default, named CA incidents, ACME client version
claims, CRLite and named CT monitors (not in the fetched sources).
Method: documentation only; no commands were run.
