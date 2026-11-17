---
id: computing-software.systems-network-administration.pki-tls-administration.path-length-constraints
name: path-length-constraints
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [path-length-constraints, pki-hierarchy, pki, basicconstraints, pathlen, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Set basicConstraints pathLenConstraint so CAs cannot create deeper hierarchies than designed; choose values per tier and test chain building."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path length constraints
Goal: stop a subordinate CA from issuing further CAs it should not.
RFC 5280 section 4.2.1.9: `pathLenConstraint` gives the maximum number of non-self-issued intermediate certificates that may follow this certificate in a valid path. The last certificate in the path (usually the end entity, sometimes a CA) is not counted.
- `pathLenConstraint` of 0: no non-self-issued intermediate CA certificate may follow. An issuing CA with 0 can still sign a final certificate (an end entity).
- Field absent: no limit. When present it must be greater than or equal to 0.
- It is meaningful only when `cA` is true and the key usage extension, if present, asserts `keyCertSign`. CAs MUST NOT include the field otherwise.
- Conforming CAs MUST include basicConstraints in every CA certificate whose key validates certificate signatures, and MUST mark it critical there.
- If `cA` is not asserted, `keyCertSign` MUST NOT be asserted either.
- Worked example for a three-tier design (root, policy CA, issuing CA, leaf), counting intermediates after each certificate: root at most 2 (policy and issuing follow it), policy CA 1 (only the issuing CA follows), issuing CA 0. The value belongs on the certificate that carries it and counts downward, not from the root.
- A root with pathlen 1 over that chain has 2 intermediates after it, which exceeds the limit, so path validation must fail.
Verify:
- [ ] The CA certificate text shows basicConstraints marked critical with CA true and the intended path length.
- [ ] A chain built through your intended tiers validates, and a deliberately deeper chain is rejected by your validator.

## Checked
Confirmed 2026-11-08 against RFC 5280 section 4.2.1.9 (pathLenConstraint semantics, critical marking, keyCertSign rule). Removed: the openssl.cnf sample sections and `openssl x509 -ext` / `openssl verify` commands (not in RFC 5280), and the claim that strict clients fail while lax ones accept (not stated). The tier values above are an example worked from the RFC definition, not a recommendation.
Method: docs-only read of cited pages, 2026-11-08
