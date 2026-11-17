---
id: computing-software.cryptography-implementation.applied-cryptography.harvest-now-decrypt-later-prioritisation
name: harvest-now-decrypt-later-prioritisation
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, post-quantum-migration, harvest-now-decrypt-later, mosca-inequality, pq-migration, risk-prioritisation, nist-ir-8547]
level: advanced
status: draft
description: "Prioritise PQ migration with Mosca's inequality: data secrecy lifetime, migration time, key exchange before signatures, and NIST deprecation dates."
sources: ["https://csrc.nist.gov/pubs/ir/8547/ipd", "https://globalriskinstitute.org/publication/2024-quantum-threat-timeline-report/", "https://www.ncsc.gov.uk/whitepaper/next-steps-preparing-for-post-quantum-cryptography"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Harvest-now-decrypt-later prioritisation

An adversary can record encrypted traffic today and decrypt it once a
cryptographically relevant quantum computer (CRQC) exists. Anything
protected only by RSA/ECDH key exchange and still sensitive at that point
is already exposed.

## Mosca's inequality

```
x = years the data must stay confidential
y = years needed to migrate the system
z = years until a CRQC (estimate)
If x + y > z, you are already late.
```

Use ranges for z from expert surveys (Global Risk Institute timeline report)
rather than one number.

## Ordering

1. **Key exchange on long-lived confidential data in transit**: TLS, VPN,
   SSH, messaging carrying health, financial, state or IP data with x of
   10+ years. Deploy hybrid ML-KEM first; this is the HNDL exposure.
2. **Data at rest wrapped with RSA/ECDH** (RSA-OAEP key wrapping, ECIES
   envelopes) with long retention: re-wrap under symmetric keys or hybrid.
   Symmetric AES-256 data is not the problem.
3. **Long-lived signatures and roots of trust**: firmware signing, root CAs,
   code signing with decades-long validity. Forgery needs a CRQC at
   verification time, so it is less urgent than HNDL but slow to change.
4. **Short-lived authentication** (TLS certificates, tokens): last.

## Deadlines to plan against

- NIST IR 8547 (draft): 112-bit RSA/ECC deprecated after 2030, all
  quantum-vulnerable public-key algorithms disallowed after 2035.
- NSA CNSA 2.0: web/cloud services prefer PQ by 2025, exclusively by 2033.
- UK NCSC: discovery by 2028, priority migration by 2031, complete by 2035.

## Verify

- [ ] Each inventory entry has x, y and a priority tier.
- [ ] Tier 1 systems have hybrid key exchange enabled or a dated plan.
