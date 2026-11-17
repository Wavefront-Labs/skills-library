---
id: computing-software.cryptography-implementation.secure-implementation.commissioning-and-reading-crypto-audits
name: commissioning-and-reading-crypto-audits
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, crypto-audit, security-audit, third-party-review, code-review, assurance]
level: practitioner
status: draft
description: "Commission and read third-party cryptography audits: scoping, choosing firms, preparing artefacts, severity interpretation, fix verification, and publishing reports."
sources: ["https://github.com/trailofbits/publications", "https://blog.trailofbits.com/2023/10/23/how-to-prepare-for-a-security-audit/", "https://ostif.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Commissioning and reading crypto audits

## Scoping
- Define components (protocol spec, library, key management, integration), threat model, commit hash, and what
  is out of scope.
- Cryptography reviews need specialists (NCC Group Cryptography Services, Trail of Bits, Cure53, Least
  Authority, Kudelski, Quarkslab). Check published reports for similar systems.
- Typical effort: 2-6 person-weeks for a library or protocol; more for novel constructions.

## Prepare
- Written spec of the protocol and formats, design rationale, threat model.
- Build and test instructions, test vectors, fuzzing harnesses, known issues list.
- Freeze a commit; name a technical contact available daily.

## Reading the report
- Severity reflects auditor judgment of impact and difficulty; read each finding's exploit scenario.
- "Informational" items often point at fragile design choices; triage them, do not ignore.
- Absence of findings in an area means "not found in the time available", not proof of security. Check the
  coverage section and time spent per component.

## After
- Fix, then request fix verification (auditor reviews patches; report updated with status).
- Publish the report if users rely on the software; public reports build trust and invite more review.
- Re-audit after major changes, not on a fixed calendar alone.

## Verify
- [ ] Every finding has an owner, fix commit or accepted-risk rationale; fix review recorded.
