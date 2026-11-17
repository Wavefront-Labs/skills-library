---
id: computing-software.cryptography-implementation.applied-cryptography.assessing-vendor-pq-readiness
name: assessing-vendor-pq-readiness
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, pq-readiness-assessment, post-quantum, vendor-assessment, ml-kem, ml-dsa, pq-migration]
level: practitioner
status: draft
description: "Assess vendor and library post-quantum readiness: questionnaire items, checking ML-KEM/ML-DSA support, hybrid TLS testing, FIPS status and roadmap evidence."
sources: ["https://www.ncsc.gov.uk/whitepaper/next-steps-preparing-for-post-quantum-cryptography", "https://www.cisa.gov/quantum", "https://pq.cloudflareresearch.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assessing vendor PQ readiness

## Questions to ask
1. Which FIPS 203/204/205 algorithms are supported today, in which product versions?
2. Hybrid key exchange in TLS (`X25519MLKEM768`) supported and enabled by default?
3. PQ certificates or signatures (ML-DSA, SLH-DSA, LMS) for firmware and code signing?
4. CMVP status of the module containing PQ algorithms (validated, in process)?
5. Crypto agility: can algorithms be changed by configuration without a redeploy?
6. Roadmap dates with commitments, not "evaluating".

## Hands-on checks
```sh
openssl s_client -connect vendor.example:443 -groups X25519MLKEM768 </dev/null 2>&1 | grep -i "group"
```
- Browser devtools Security tab shows the negotiated key exchange.
- Check library versions: OpenSSL 3.5+, BoringSSL, Go 1.24+, Java 24+ (ML-KEM/ML-DSA), .NET 10, rustls with aws-lc-rs.

## Scoring
Rate each vendor: ready (shipping, default on), available (opt-in), planned (dated), unknown. Unknown on a
system with long-lived confidential data is a risk item.

## Verify
- [ ] Evidence recorded (screenshots, scan output, documentation links) per vendor with review date.
