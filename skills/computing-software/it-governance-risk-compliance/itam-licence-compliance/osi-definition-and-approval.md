---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.osi-definition-and-approval
name: osi-definition-and-approval
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [osi-definition-and-approval, licence-classification-osi-fsf, osi, open-source-definition, osd, approved-licence, licence-review, itam-licence-compliance]
level: intro
status: docs-checked
description: "Apply the ten criteria of the Open Source Definition and understand how a licence gets OSI approval."
sources:
  - https://opensource.org/osd
  - https://opensource.org/licenses/review-process
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Open Source Definition and OSI approval

Goal: decide whether a licence is open source in the OSI sense.

## The ten criteria
The OSD states that open source is more than access to source: distribution terms must meet all of these.
1. Free redistribution: no restriction on selling or giving away the software as part of an aggregate distribution; no royalty.
2. Source code: included or obtainable for no more than reasonable reproduction cost; must be the preferred form for modification (no obfuscation, no preprocessor output).
3. Derived works: modifications and derived works allowed, distributable under the same terms.
4. Integrity of the author's source: modified source may be restricted only if patch files are allowed; distribution of software built from modified source must be permitted; a different name or version number may be required.
5. No discrimination against persons or groups.
6. No discrimination against fields of endeavour (for example business use or genetic research).
7. Distribution of licence: rights apply to all recipients without an additional licence.
8. Licence must not be specific to a product.
9. Licence must not restrict other software distributed with it.
10. Licence must be technology-neutral.

## Approval process
- All licences go through the public License Review Process; formal approval requires it. Submission is to the license-review mailing list, and approval is by consensus: no one person can approve or reject.
- The License Committee observes the discussion and, on consensus, its Chair recommends approval or rejection to the OSI Board, which votes.
- Decision Date is normally 60 days after first submission (30 days after a revised version, but not earlier than 60 days from the original), and may be extended.
- A legacy licence is one used for at least five years by more than twenty projects of unrelated entities; any other is new. New licences must also be reusable, fill a gap, be clear, and be possible to comply with. Overlays such as Commons Clause are not approved in isolation.
- Approval of similar terms in the past does not bind the OSI.

## Method
For an unfamiliar licence, check the OSI licence list (https://opensource.org/licenses), then read the text against the ten criteria.

## Gotchas
- A field-of-use restriction fails criterion 6, so such licences are not open source in the OSI sense.
- "Open source" in marketing is not a legal test; the OSD criteria are.

## Verify
- [ ] Licence appears on the OSI list, or is assessed against all ten criteria.

## Checked
2026-11-08. Confirmed against the OSD page and the OSI License Review Process page, both read in full. Removed: the SPDX isOsiApproved flag claim and the "no AI use" example (neither on these pages); the bulk-generated ISO, SPDX, CycloneDX, NTIA, OpenChain, REUSE and GNU sources, which were not read in this batch.
Method: documentation only; no commands were run.
