---
id: computing-software.cryptography-implementation.protocol-implementation.short-lived-certificates-47-day-validity
name: short-lived-certificates-47-day-validity
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, certificate-lifecycle, short-lived-certificates, cab-forum-ballot-sc081, certificate-validity, automation, revocation-alternative, internal-pki]
level: advanced
status: docs-checked
description: "Prepare for shrinking public TLS validity (CA/B SC-081: 398 days down to 47 by March 2029) and use short-lived internal certs to replace revocation."
sources: ["https://cabforum.org/2025/04/11/ballot-sc081v3-introduce-schedule-of-reducing-validity-and-data-reuse-periods/", "https://letsencrypt.org/2025/01/16/6-day-and-ip-certs", "https://smallstep.com/docs/step-cli/reference/ca/certificate/", "https://smallstep.com/docs/step-cli/reference/ca/renew/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Short-lived certificates and the 47-day schedule

CA/Browser Forum ballot SC-081 (2025) reduces the maximum validity of public
TLS certificates from 398 days to 47 days in steps, starting in March 2026 and
concluding in March 2029. The same ballot reduces how long validated domain/IP
data (SAN validation) may be reused from 398 days to 10 days. Read the ballot
and the current Baseline Requirements for the exact intermediate steps and
dates; do not rely on a copy of the table.

Let's Encrypt also offers 6-day certificates (opt-in through an ACME
certificate profile; they carry no OCSP or CRL URLs). Anything renewed by hand,
uploaded through a portal, or pinned in a device will break on this schedule.

## Get ready (public certs)

1. Inventory every public certificate: Certificate Transparency log search for
   your domains, load balancer and CDN consoles, appliances, SaaS custom domains.
2. For each, identify the renewal path. Manual uploads (hardware appliances,
   some PaaS, on-prem email gateways) need an ACME client, a vendor API, or a
   TLS-terminating proxy in front that can automate.
3. Remove certificate pinning of leaf keys in mobile apps and partners (pin
   CA/intermediate SPKIs with backups, or stop pinning).
4. Monitor: alert at 1/3 lifetime remaining, independent of the renewal tool.

## Short-lived certs as a design tool (internal PKI)

Certificates valid for hours to a few days make revocation largely
unnecessary: a compromised key is useless once its cert expires, and CRL/OCSP
infrastructure (with its reliability problems) can be dropped.

- step-ca: `step ca certificate svc.internal svc.crt svc.key --not-after 24h`
  (`--not-after` takes a time or a duration), renewal daemon
  `step ca renew --daemon svc.crt svc.key` (by default renews before 2/3 of the
  validity has elapsed; `--renew-period` overrides).
- Other CAs and workload-identity systems (Vault PKI, SPIFFE/SPIRE, SSH
  certificates) support the same idea: set a short TTL and renew automatically.

Requirements: reliable time sync (NTP) on all clients and servers, and a CA
with high availability - if issuance is down longer than the cert lifetime,
services fail.

## Verify

- [ ] Every public certificate has an automated renewal path; manual ones listed with owners.
- [ ] Renewal tested with the next shorter validity (e.g. issue 6-day staging certs).
- [ ] Internal short-lived issuance has HA and alerting on issuance failures.

## Checked

2026-10-31. Confirmed against the CA/B Forum SC-081v3 ballot page (reduction from 398 to 47 days, SAN validation
reuse 398 to 10 days, March 2026 to March 2029), the Let's Encrypt 6-day announcement (opt-in profile, no OCSP/CRL
URLs, automation needed) and the smallstep `step ca certificate` / `step ca renew` reference pages (`--not-after`,
`--daemon`, 2/3 default, `--renew-period`). Removed: the 200/100-day intermediate steps and their dates (not on the
fetched page), the crt.sh query string, the Vault `ttl=72h` and SPIRE 1-hour examples (no source fetched).
Method: documentation only; no commands were run.
