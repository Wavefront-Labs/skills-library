---
id: computing-software.systems-network-administration.pki-tls-administration.crl-generation-distribution
name: crl-generation-distribution
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [crl-generation-distribution, pki-crl, crl, revocation-list, nextupdate, crlnumber, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Generate CRLs with the fields RFC 5280 requires (thisUpdate, nextUpdate, CRL number, AKI) and publish them at the URI in the CRL distribution points extension."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRL generation and distribution
Goal: clients get a current CRL that supersedes older ones unambiguously. Source: RFC 5280 sections 4.2.1.13 and 5.
- Required CRL fields and extensions:
  - `thisUpdate`: issue date of this CRL.
  - `nextUpdate`: the date by which the next CRL will be issued. It may come earlier but not later. Conforming issuers MUST include it in every CRL, and SHOULD issue CRLs with a nextUpdate equal to or later than all previous CRLs.
  - CRL number extension: MUST be in all CRLs, non-critical, a monotonically increasing sequence number for a given scope and issuer. Two CRLs for the same scope issued at different times MUST NOT share a number. Values up to 20 octets; issuers MUST NOT exceed that.
  - Authority key identifier: MUST be included in all CRLs, using the key identifier method.
- Revoked entries: when nothing is revoked, the revoked certificates list MUST be absent. Entries are identified by certificate serial number plus revocation date.
- Date encoding: UTCTime through 2049, GeneralizedTime from 2050.
- Distribution (CRL distribution points extension in certificates): SHOULD be non-critical, and a certificate's DistributionPoint cannot consist of the reasons field alone. If the certificate issuer is also the CRL issuer, the CA MUST omit cRLIssuer and MUST include distributionPoint.
- Multiple names in one distribution point are different ways to fetch the same CRL (for example LDAP and HTTP). DistributionPointName SHOULD include at least one LDAP or HTTP URI.
- With an HTTP or FTP URI, the URI MUST point to a single DER-encoded CRL, and an HTTP server SHOULD answer with media type `application/pkix-crl`.
- A DistributionPoint that omits `reasons` covers all reasons. RFC 5280 recommends against segmenting CRLs by reason code, and any certificate with the extension MUST have at least one DistributionPoint that covers it for all reasons.
- Validity window, cache headers, size targets and alert thresholds are not given by RFC 5280; take the nextUpdate interval from your CA's policy and your relying parties' requirements.
Gotcha: nextUpdate is the latest date the next CRL will appear, so a client holding the current CRL learns of new revocations only from a later CRL (see delta-crl-and-partitioning for deltas).
Verify:
- [ ] Each CRL has thisUpdate, nextUpdate, a CRL number greater than the previous CRL's, and an AKI with a key identifier.
- [ ] The URI in the certificates returns one DER CRL with content type `application/pkix-crl`.
- [ ] Monitoring alerts before nextUpdate passes without a new CRL (threshold is your own policy).

## Checked
Confirmed 2026-11-08 against RFC 5280 sections 4.2.1.13, 5.1.2.4 to 5.1.2.6, 5.2.1 and 5.2.3. Removed: the 24-168 hour and 6-12 month validity figures, the 7-day Baseline Requirements claim, Cache-Control, ETag and compression advice, the 25 percent alert threshold, the `openssl crl` and `step certificate inspect` commands, and the claim that clients cache until nextUpdate (not stated by the page).
Method: docs-only read of cited pages, 2026-11-08
