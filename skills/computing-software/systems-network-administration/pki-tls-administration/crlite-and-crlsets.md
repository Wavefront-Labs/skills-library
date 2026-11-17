---
id: computing-software.systems-network-administration.pki-tls-administration.crlite-and-crlsets
name: crlite-and-crlsets
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [crlsets, revocation-checking, chrome, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Understand how Chrome CRLSets handle revocation (emergency blocking, no routine OCSP or CRL fetches) and what that means for revoking certificates."
sources:
  - https://www.chromium.org/Home/chromium-security/crlsets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chrome CRLSets and browser revocation
Goal: know what revocation protection Chrome actually provides.
- CRLSets are the primary means by which Chrome quickly blocks certificates in emergency situations. As a secondary function they hold some non-emergency revocations, for intermediate and leaf certificates, obtained by crawling CRLs published by CAs.
- Online checks (OCSP and CRL) are not generally performed by Chrome. Online OCSP checks can be enabled by enterprise policy.
- Chromium's CRLSet-handling source is public, but the process that generates CRLSets is not.
- Google crawls CRLs disclosed to CCADB and, for intermediates, those discovered via Certificate Transparency. CRLs are fetched infrequently (at most once every few hours) and verified against the signing certificate. Only a subset of the certificates revoked on those CRLs is included in the current CRLSet.
- The current CRLSet can be dumped with the agl/crlset-tools code, and Chrome's CRLSet version is visible at chrome://components.
- Consequence: revoking a certificate does not guarantee Chrome blocks it, since only a subset of revocations is in the CRLSet. Do not rely on revocation alone after a key compromise.
Verify:
- [ ] You can state per client which revocation mechanism applies, and have not assumed Chrome checks OCSP.

## Checked
Method: docs-checked 2026-11-09 against the Chromium "CRLSets" page (read in full). The Mozilla Security Blog CRLite tag page was read and is only an article index, so the CRLite content, Safari/Apple behaviour, the 47-day lifetime claim and the internal PKI advice were removed as unconfirmed, and that source was dropped. The skill is now scoped to CRLSets; the name is unchanged. The consequence line is an inference from the page, not a quoted statement.
