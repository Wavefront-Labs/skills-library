---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.weak-copyleft-licences-overview
name: weak-copyleft-licences-overview
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [weak-copyleft-licences-overview, open-source-licence-families, lgpl, mpl-2-0, epl, cddl, weak-copyleft, file-level-copyleft, linking, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Compare weak copyleft licences by scope of the copyleft: library, file or module level and the linking rules."
sources:
  - https://opensource.org/license/lgpl-2-1
  - https://opensource.org/license/lgpl-3-0
  - https://opensource.org/license/mpl-2-0
  - https://opensource.org/license/epl-2-0
  - https://opensource.org/license/cddl-1-0
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Weak copyleft: LGPL, MPL, EPL, CDDL

Goal: pick compliant integration patterns.

- LGPL-2.1 section 6: you may combine or link a "work that uses the Library" and distribute the result under terms of your choice, if those terms permit modification for the customer's own use and reverse engineering for debugging. You must give prominent notice, supply the licence, and either ship the Library source plus the work in a form that lets the user relink (6a), or use a suitable shared library mechanism (6b: a runtime copy already on the user's system that works with an interface-compatible modified version).
- LGPL-3.0 section 4 (Combined Works): terms of your choice that do not restrict modification of the Library portions or reverse engineering for debugging, plus prominent notice, a copy of the GNU GPL and the LGPL text, and either (0) Minimal Corresponding Source and Application Code suitable for relinking, or (1) a suitable shared library mechanism. Installation Information is required only where GPLv3 section 6 would require it. Section 3 relaxes duties for header material limited to numerical parameters, data layouts, accessors or small macros/inline functions/templates of ten or fewer lines.
- MPL-2.0: file-level. Modifications are files containing or derived from Covered Software; Source Code Form must stay under MPL-2.0 and executables must be accompanied by how to obtain the source. A Larger Work (Covered Software combined with other material in separate files) may be distributed under terms of your choice, provided the MPL requirements are met for the Covered Software. Secondary Licenses are GPL 2.0, LGPL 2.1 and AGPL 3.0 or later, unless the file is marked Incompatible With Secondary Licenses.
- EPL-2.0: Modified Works are changes to or new files containing Program content; works that only link to, bind by name or subclass the Program are excluded. Source must be available when you Distribute the Program in any form. Executables may go under a different licence if it disclaims warranties and liability on behalf of other Contributors, does not limit rights in the source, and requires onward distribution to satisfy the same section. Source may be offered under a Secondary License (GPL 2.0 or later) only if the initial Contributor attached the Exhibit A notice. Patent rights end for a recipient who sues alleging the Program itself infringes.
- CDDL-1.0: file-level. Modifications are files changed or new files containing Original Software. Covered Software in Executable form must also be available as Source Code under CDDL only; Executable form may go under a licence of your choice that does not limit source rights. Larger Works with code not governed by the licence are allowed. You must mark each of your Modifications with your identity as Contributor.

## Method
Record how each component is linked and whether modified, to decide what must be published.

## Gotchas
- The licence text is the test, not the linking label: LGPL needs relink ability or a shared-library mechanism for combined works.
- Header-only code in LGPL-3.0 falls under section 3's size limits, which blur the library boundary.
- Whether a given pattern counts as a derivative or Combined Work is a legal question.

## Verify
- [ ] Legal sign-off per integration pattern.

## Checked
2026-11-08. Confirmed against the OSI pages for LGPL-2.1 (section 6 only), LGPL-3.0 (sections 0-5), MPL-2.0 (sections 1-3) and EPL-2.0 and CDDL-1.0 (read in full). Removed: LGPL-2.1 and 3.0 "modifications stay LGPL" and "static linking needs extra steps" (not separately confirmed), the CDDL "GPL-incompatible" claim (not on the page), and the bulk-generated ISO, SPDX, CycloneDX, NTIA, OpenChain, REUSE and GNU sources.
Method: documentation only; no commands were run.
