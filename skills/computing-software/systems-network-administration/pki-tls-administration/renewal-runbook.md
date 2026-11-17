---
id: computing-software.systems-network-administration.pki-tls-administration.renewal-runbook
name: renewal-runbook
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [renewal-runbook, pki-lifecycle, renewal, runbook, rotation, ca-migration, pki-tls-administration]
level: practitioner
status: draft
description: "Document the renewal procedure per certificate class, rollback, owner handoffs and the emergency replace procedure."
sources:
  - https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Renewal and replacement runbook
Goal: anyone on-call can renew or replace a certificate safely.
Per class (public web, internal service, CA, client/device) record:
1. How issued (ACME/API/manual) and from where.
2. Where the key and cert live and who can read them.
3. How deployed (reload command, orchestration, restart impact).
4. Validation after: `openssl s_client`, browser check, dependent clients.
5. Rollback: keep previous cert and key for 7 days; a one-line restore.
Emergency replace (key compromise):
- Revoke old cert at the CA; generate a new key; issue; deploy; update pinning and trust stores; record in incident log; check CT for rogue issuance.
CA renewal: generate new CA cert (same key preferred), publish AIA/CRL, push to trust stores 6+ months before the old expiry, then switch issuance.
Run a renewal drill quarterly on a non-critical cert.
Gotcha: renewal dates cluster (everything issued at one go-live); stagger them so a single failure does not take all services.
Verify:
- [ ] Runbook is tested by someone who did not write it.
- [ ] Dates for next renewals are in monitoring.
