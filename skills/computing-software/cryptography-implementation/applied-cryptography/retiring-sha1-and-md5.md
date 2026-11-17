---
id: computing-software.cryptography-implementation.applied-cryptography.retiring-sha1-and-md5
name: retiring-sha1-and-md5
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, hash-functions, sha1-deprecation, md5, sha-1, sp-800-131a, shattered, chosen-prefix-collision, migration]
level: practitioner
status: docs-checked
description: "Find and retire SHA-1 and MD5: NIST's 31 December 2030 SHA-1 transition date, why collision attacks matter, and how to inventory and migrate uses."
sources: ["https://csrc.nist.gov/news/2022/nist-transitioning-away-from-sha-1-for-all-apps", "https://csrc.nist.gov/pubs/sp/800/131/a/r2/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retiring SHA-1 and MD5

## What is broken

- NIST cites a serious cryptanalytic attack on SHA-1 collision resistance
  announced in 2005 and "SHA-1 is a Shambles" (Leurent and Peyrin, 2020) as
  the reasons to transition away.
- Collision resistance is necessary for digital signature applications, so
  signatures and certificates are the first uses to move. Treat MD5 the same way.

## Policy

- NIST SP 800-131A (2011) deprecated SHA-1 for generating new digital
  signatures.
- NIST (15 December 2022): the transition away from SHA-1 for all
  applications is to be completed by December 31, 2030; the SHA-1
  specification stays available for handling information protected earlier.
- NIST plans to remove SHA-1 from FIPS 180-5 and revise SP 800-131A.

## Find uses

```bash
rg -n -i "md5|sha1|sha-1" src/
```

Also check: certificate and CSR signatures, code signing, JWT `alg`,
package checksums, git object hashing, password hashes,
TLS signature_algorithms lists, and database columns storing digests.

## Migrate

1. Signatures and certificates: reissue with SHA-256 or better.
2. Integrity checksums: switch to SHA-256, publish both during transition.
3. Identifiers/dedup keys: dual-write new SHA-256 keys, backfill, switch reads.
4. Non-security uses that must stay MD5 or SHA-1 (legacy protocol ids): mark
   them in code so reviewers can tell.

## Verify

- [ ] Inventory lists every SHA-1/MD5 use with an owner and a removal date before 2030.
- [ ] No new signatures are generated with SHA-1.

## Checked

- 2026-11-01. Confirmed (NIST news item of 15 December 2022): SHA-1 transition for all applications to complete by December 31, 2030, SHA-1 specification stays available for earlier-protected data, 2005 collision attack, "SHA-1 is a Shambles" 2020, SP 800-131A in 2011 deprecated SHA-1 for new signatures, plan to remove SHA-1 from FIPS 180-5.
- Removed as unconfirmed: MD5 and Flame history, SHAttered, cost figures, HMAC and HOTP remarks, language and git specifics, the shattered.io source (page no longer about the attack).

Method: documentation only; no commands were run.
