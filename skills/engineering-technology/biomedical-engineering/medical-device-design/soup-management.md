---
id: engineering-technology.biomedical-engineering.medical-device-design.soup-management
name: soup-management
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [soup, medical-device-software, samd, software-of-unknown-provenance, iec-62304, third-party-software, sbom, anomaly-list]
level: practitioner
status: gated
description: "Manage software of unknown provenance under IEC 62304: SOUP inventory, requirements, known anomalies review, version control, monitoring and replacement planning."
sources: ["IEC 62304 Medical device software - Software life cycle processes (clauses on SOUP; confirm edition)", "FDA, Content of Premarket Submissions for Device Software Functions (final, June 2023), https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-premarket-submissions-device-software-functions", "IEC 82304-1 Health software product safety requirements"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SOUP management

**Goal:** know every piece of third-party or legacy software in the device, what you rely on it for, and what its known defects could do to patients.

SOUP means (IEC 62304 definition (gated: unconfirmed, source is paywalled or blocked)) software already developed and not intended for your medical device, or software developed under an unknown or insufficient process.

## Inventory
Record for each SOUP item:
- Title, manufacturer or project, **exact version** and unique designator (for example library name and version, OS build).
- Licence and source (supports your obligations and SBOM).
- The software item(s) that use it and the safety class of that item.
- **Functional and performance requirements** you need from it (written by you, not copied from marketing).
- Required hardware and software environment (OS, runtime, compiler flags).
- Where it is fixed (static linking, container image digest).

## Evaluation
1. **Is it suitable?** Review documentation, quality evidence, community track record, test coverage and support lifetime.
2. **Known anomalies:** review the published defect list and security advisories at the chosen version; assess each for its effect on your hazards; record the evaluation.
3. **Risk analysis:** include SOUP failure modes (crash, wrong output, memory leak, timing) in the software risk analysis; add controls (watchdog, validation, isolation).
4. **Verification:** test the SOUP's use in your context (the functions you rely on), and verify your risk controls.

## Maintenance
- Monitor for new anomalies and vulnerabilities (CVE feeds, vendor bulletins) through the life; define assessment timelines.
- Change control for updates (re-evaluate, re-test affected functions).
- Plan for end-of-life of components and operating systems.
- Keep a software bill of materials (SBOM) in a standard format (SPDX, spdx.dev, or CycloneDX, cyclonedx.org; both projects exist).

## Gotchas
- Pulling an unpinned dependency at build time.
- Using SOUP in a Class C item without enough evidence; consider replacing or isolating it.
- Forgetting transitive dependencies and firmware blobs.

## Verify
- [ ] Inventory complete with versions, matching the build.
- [ ] Anomaly review dated and signed for each release.
- [ ] Update process tested.
