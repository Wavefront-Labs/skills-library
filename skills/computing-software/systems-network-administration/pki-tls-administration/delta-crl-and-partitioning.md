---
id: computing-software.systems-network-administration.pki-tls-administration.delta-crl-and-partitioning
name: delta-crl-and-partitioning
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [delta-crl-and-partitioning, pki-crl, crl, delta-crl, issuing-distribution-point, crl-sharding, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Use delta CRLs, the freshest CRL extension and issuingDistributionPoint scoping as RFC 5280 defines them, including the rules that tie them together."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delta CRLs and CRL partitioning
Goal: reduce download size and revocation latency with the mechanisms RFC 5280 defines (sections 4.2.1.15, 5.2.3 to 5.2.6).
- Delta CRL: carries updates to revocation information already distributed, rather than a full list. It MUST include a critical delta CRL indicator holding the CRL number of the base CRL, and the issuer MUST publish that base as a complete CRL. Delta plus base equals a complete CRL at the delta's publication time.
- A delta CRL MUST cover the same reasons and certificates (same scope) as its base. Deltas are generally smaller than the CRLs they update.
- Numbering: complete and delta CRLs for a scope share one numbering sequence. If issued at the same time, a delta and a complete CRL carry the same number and equivalent information.
- Locating deltas: the freshest CRL extension (non-critical, same syntax as cRLDistributionPoints) names where deltas are found. It can appear in certificates and in complete CRLs, but MUST NOT appear in delta CRLs. In a CRL only the distributionPoint field is meaningful; reasons and cRLIssuer MUST be omitted.
- Partitioning: the issuing distribution point extension is critical and defines a CRL's scope. Fields: distributionPoint, onlyContainsUserCerts (end-entity certificates only), onlyContainsCACerts, onlySomeReasons, indirectCRL, onlyContainsAttributeCerts (MUST be FALSE for conforming issuers). At most one of the three onlyContains flags may be TRUE, and the extension must not be an empty sequence.
- If distributionPoint is present in the CRL, it MUST include at least one name from the distributionPoint field in the cRLDistributionPoints extension of every certificate in scope, with identical encoding. So each certificate's CRL URI has to match the shard that lists it.
- If distributionPoint is absent, the CRL contains all revoked unexpired certificates from that issuer within scope.
- Reason and indirect CRLs: onlySomeReasons splits by reason (the RFC's example separates keyCompromise, cACompromise and aACompromise from the rest), but RFC 5280 recommends against segmenting by reason. `indirectCRL` TRUE means the CRL covers certificates from authorities other than its issuer. Use either only when you need it.
- Support: the IDP extension is critical, yet implementations are not required to support it. One that does not must treat the status of unlisted certificates as unknown or find another CRL without unrecognised critical extensions. Client support for deltas varies and is not covered by the page; do not rely on deltas alone.
- How to shard (by serial hash, month, etc.), delta and base intervals, and client or browser revocation aggregation are outside the cited page.
Gotcha: a delta is only usable with its referenced base, so keep the base CRL published for as long as deltas point to it.
Verify:
- [ ] The delta CRL indicator value equals the CRL number of a published complete CRL of the same scope.
- [ ] Each certificate's CRL distribution point name matches the distributionPoint in the IDP of the CRL that lists it.

## Checked
Confirmed 2026-11-08 against RFC 5280 sections 4.2.1.15, 5.2.3, 5.2.4, 5.2.5 and 5.2.6. Removed: Windows delta/base period defaults, the Windows-uses-deltas claim, the sharded CRL and CRLite statement, `certutil` command, the "fail closed" claim, and the "indirect CRLs rarely supported" claim (the RFC states only that support for the IDP extension is not required).
Method: docs-only read of cited pages, 2026-11-08
