---
id: computing-software.digital-forensics-incident-response.evidence-handling.choosing-hash-algorithms-for-evidence
name: choosing-hash-algorithms-for-evidence
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [hash-algorithm-choice, md5, sha1, sha256, hash-collisions, evidence-integrity, dfir]
level: practitioner
status: draft
description: "Choose hash algorithms for evidence integrity: MD5 and SHA-1 collision issues, why dual hashing persists, SHA-256 as default, and explaining it in court."
sources: ["https://csrc.nist.gov/projects/hash-functions", "https://shattered.io/", "https://www.swgde.org/documents/published-complete-listing/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing hash algorithms for evidence

**Goal:** pick hashes that are defensible for integrity, compatible with tools and hash sets,
and explainable to a non-technical audience.

## Facts
- **MD5**: practical collisions since 2004 (chosen-prefix collisions 2007+). Still no
  practical *second-preimage* attack, which is what forging a match for an existing image
  would need.
- **SHA-1**: practical collision shown in 2017 (SHAttered) and chosen-prefix in 2020;
  deprecated by NIST for digital signatures.
- **SHA-256 / SHA-3**: no known practical attacks; NIST-approved (FIPS 180-4, 202).

## Recommendation
- Default to **SHA-256** for images and exported files.
- **Dual-hash (MD5 + SHA-256)** when interoperating with older tools, hash sets (NSRL RDS
  includes MD5 and SHA-1 and SHA-256), or agency requirements; most imagers compute both in
  one pass at negligible cost.
- Record the algorithm with every value; a hex string without algorithm is useless.

## Explaining collisions
A collision attack lets someone craft *two new* files with the same hash; it does not let
them create a different file matching *your existing* image's hash. Combined with chain of
custody and a second algorithm, integrity remains strongly supported. SWGDE notes MD5/SHA-1
remain acceptable for integrity verification but recommends stronger algorithms going forward.

## Matching known files
Malware intel often still publishes MD5/SHA-1; compute those too for lookups, but cite
SHA-256 in reports.

## Verify
Case documentation names the algorithm(s) per evidence item and the tool that computed
them, and reports use SHA-256 as the primary identifier.
