---
id: computing-software.systems-network-administration.pki-tls-administration.ejbca-ra-protocols
name: ejbca-ra-protocols
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [ejbca-ra-protocols, pki-ejbca, ejbca, est, cmp, scep, acme, pki-tls-administration]
level: practitioner
status: draft
description: "Expose EJBCA through ACME, EST, CMP, SCEP and REST, choosing a protocol per client type and securing it."
sources:
  - https://docs.keyfactor.com/ejbca/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EJBCA RA protocols and issuance interfaces
Goal: enable only the enrolment protocols clients need.
| Client | Protocol |
|---|---|
| Web servers, cert-manager | ACME (RFC 8555) |
| IoT, EST-capable devices | EST (RFC 7030) |
| Telecom, network gear | CMP (RFC 4210) |
| Network devices, MDM | SCEP |
| Automation | REST API (client-cert authenticated) |
- Each protocol maps to an end entity profile and CA via an alias (`/ejbca/.well-known/est/<alias>`).
- Enable protocols individually under System Configuration > Protocol Configuration.
- Use client-certificate authentication for REST and EST; SCEP's challenge password is shared secret and weak, so prefer one-time passwords per request.
- Terminate TLS with a mutual-auth proxy and pass the client cert on correctly.
Gotcha: leaving unused protocols enabled adds attack surface; confirm via port scan and the admin UI.
Verify:
- [ ] An ACME or EST test request issues a certificate with the expected profile.
- [ ] Disabled protocols return 404/403.
