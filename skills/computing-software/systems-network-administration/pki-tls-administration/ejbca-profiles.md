---
id: computing-software.systems-network-administration.pki-tls-administration.ejbca-profiles
name: ejbca-profiles
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [ejbca-profiles, pki-ejbca, ejbca, certificate-profile, end-entity-profile, pki-tls-administration]
level: practitioner
status: draft
description: "Model issuance in EJBCA with certificate profiles, end entity profiles and CAs, with approvals and key bindings."
sources:
  - https://docs.keyfactor.com/ejbca/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EJBCA certificate and end entity profiles
Goal: separate what a cert looks like from who may request it.
- Certificate profile: algorithms, key sizes, validity, extensions, usages. Clone the shipped ENDUSER profile rather than editing it.
- End entity profile: which subject DN and SAN fields are required or fixed, which CAs and certificate profiles are allowed, whether a password or approval is needed.
- Role-based access: Administrator roles map to authentication tokens (client cert) and rules per CA or profile.
- Approval profiles require N administrators to approve sensitive requests.
- CLI: `bin/ejbca.sh ra addendentity --username web1 --dn "CN=web1.example.com" --caname IssuingCA --type 1 --token PEM` then `ra setclearpwd` and `batch`.
- Database is the source of truth; back it up with the soft token or HSM-key references.
Gotcha: end entity profiles that allow any DN field let operators enter arbitrary subjects; mark fields as "modifiable = false" with fixed values.
Verify:
- [ ] A request outside profile limits is rejected in the RA web UI.
- [ ] Approval flow triggers for the sensitive profile.
