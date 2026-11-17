---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.strong-and-network-copyleft-overview
name: strong-and-network-copyleft-overview
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [strong-and-network-copyleft-overview, open-source-licence-families, gpl, gpl-2.0, gpl-3.0, agpl, strong copyleft, network copyleft, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Explain what GPL-2.0, GPL-3.0 and AGPL-3.0 require for derivative works, internal use and network use, and how GPLv2 and GPLv3 interact."
sources:
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strong and network copyleft: GPL and AGPL

Goal: judge whether copyleft reaches your code.

- GPL: anyone who receives a copy from you has the right to redistribute copies, modified or not; a combined work that includes GPL code is distributed under the GPL with source.
- An organisation can make a modified version and use it internally without releasing it outside the organisation; the obligation arises when you give copies to others.
- AGPL-3.0 section 13 adds an obligation for users interacting with a modified version remotely through a computer network; the FAQ has entries on what counts as remote interaction and how to offer source.
- GPLv3 can be combined with more kinds of licences than GPLv2, and the GPL FAQ covers installation information for user products (the "tivoization" provision) and patents.
- The FAQ states that GPLv2 and GPLv3 are not compatible with each other: combining GPLv2-only code with GPLv3 code would violate section 6 of GPLv2.

Gotchas:
- Aggregation versus combination, and what linking does, are judgement calls; read the FAQ entries on aggregates and linking and get legal advice.
- "or any later version" wording decides which versions you may use; record it for every component.
- SSPL and other source-available licences are outside the cited page: assess them from their own text.

Verify: for each copyleft component, the exact licence version and whether "or any later version" applies are recorded.

## Checked

2026-11-09. Checked against the GNU GPL FAQ (searched by keyword, partial read; distribution right, internal modified use, AGPL section 13 entries, GPLv2/GPLv3 incompatibility and section 6, installation information, patents, aggregate entries, "or any later" wording). Removed: the SSPL and OSI approval claim, the SPDX -only / -or-later identifier advice, and the flat statement that linking always makes a combined work, because the cited pages do not support them as written. Sources not read in full or unreadable (ISO, SPDX, REUSE) were dropped.

Method: documentation only; no commands were run.
