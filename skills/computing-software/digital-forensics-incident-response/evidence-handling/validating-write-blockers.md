---
id: computing-software.digital-forensics-incident-response.evidence-handling.validating-write-blockers
name: validating-write-blockers
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [write-blocker-validation, tool-validation, nist-cftt, write-blocker, dfir]
level: practitioner
status: draft
description: "Validate a hardware or software write blocker before casework: NIST CFTT approach, a repeatable in-house test, firmware changes, and recording results."
sources: ["https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt", "https://www.swgde.org/documents/published-complete-listing/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Validating write blockers

**Goal:** evidence that your write blocker blocks writes and passes reads correctly, in the
configuration you use, so it withstands challenge.

## Use published testing
NIST CFTT publishes test reports for many hardware write blockers (HWB specification) and
software write block tools (SWB). Note the model and **firmware version** tested; a firmware
update means your unit is no longer the tested configuration.

## In-house validation procedure (per unit, per firmware)
1. Prepare a test drive: wipe, write known content, hash (SHA-256) the full device.
2. Connect through the blocker in write-blocked mode.
3. Attempt writes from the host: create a file on a mounted partition, `dd` a sector, format,
   change partition table. All must fail.
4. Read the full device and hash; must equal the reference hash.
5. Confirm full capacity read (sector count equals drive's), and HPA/DCO reporting behaves
   as documented.
6. Remove, hash the drive on a separate known-good path; must equal the reference.
7. Record: date, tester, unit serial, firmware, OS/tool versions, steps, results, pass/fail.

## Frequency
At acquisition of the unit, after every firmware update, and periodically (e.g. yearly) or
after damage. Laboratories accredited to ISO/IEC 17025 must have this documented.

## Verify
Every acquisition record references a validation record for the blocker unit used whose date
precedes the acquisition and whose firmware matches.
