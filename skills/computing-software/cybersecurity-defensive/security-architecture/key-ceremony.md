---
id: computing-software.cybersecurity-defensive.security-architecture.key-ceremony
name: key-ceremony
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [key-ceremony, root-ca, offline-root-ca, hsm, m-of-n, dual-control, pki]
level: advanced
status: draft
description: "Run a root CA key ceremony: script, roles and witnesses, offline HSM key generation with M-of-N custody, sub-CA signing, evidence capture and secure storage afterwards."
sources: ["https://www.iana.org/dnssec/ceremonies", "https://cabforum.org/working-groups/server/baseline-requirements/documents/", "https://csrc.nist.gov/pubs/sp/800/57/pt2/r1/final", "https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Root CA key ceremony

A key ceremony generates or uses the root private key under documented, witnessed, dual-control
conditions so that anyone can later trust the key was never exposed.

## Roles
Ceremony administrator (runs the script), crypto officers / key custodians (hold HSM smartcards or
PINs, M-of-N), internal witness/auditor, videographer/scribe. Nobody holds enough material alone to
use the key.

## Preparation
- Script reviewed in advance: every command, expected output, and sign-off lines.
- Air-gapped laptop/server (no NIC/wireless, BIOS-locked), freshly installed or verified image, hash of software recorded.
- HSM (e.g. Thales Luna, Entrust nShield) initialised with M-of-N quorum (e.g. 3 of 5 cards).
- Tamper-evident bags with serial numbers; safe access list.

## Ceremony steps
1. Attendance log, ID checks, cameras on, room inspected.
2. Unseal equipment, record bag serials.
3. Boot offline machine, verify software hashes.
4. Initialise/activate HSM with quorum; generate root key pair in HSM (non-exportable, or backup to backup HSM/cards under quorum).
5. Create self-signed root certificate with the agreed profile (validity e.g. 20 years, path length, key usage keyCertSign/cRLSign).
6. Sign the issuing CA CSRs brought on removable media; issue initial CRL.
7. Export public material only (root cert, sub-CA certs, CRL); hash and record.
8. Shut down, seal HSM and media in new tamper-evident bags, log serials, store in separate safes.
9. All participants sign the script; scribe preserves video and logs.

## Afterwards
- Root comes online only for scheduled CRL signing (before `nextUpdate`, e.g. every 6-12 months) and sub-CA renewal, each as a mini-ceremony.

## Gotchas
- Forgetting to schedule CRL re-signing breaks revocation checking estate-wide when the root CRL expires.
- Custodian turnover: re-key cards when a custodian leaves.
- Any deviation from the script must be recorded and witnessed.

## Verify
- [ ] Signed script, attendance log, video and bag serials archived.
- [ ] CRL renewal date in the operations calendar.
