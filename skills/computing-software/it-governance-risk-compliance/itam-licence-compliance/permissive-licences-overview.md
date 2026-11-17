---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.permissive-licences-overview
name: permissive-licences-overview
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [permissive-licences-overview, open-source-licence-families, mit, bsd, apache-2-0, isc, permissive, attribution, patent-grant, itam-licence-compliance]
level: intro
status: docs-checked
description: "Know the obligations of MIT, BSD-2/3, ISC and Apache-2.0 including attribution, notices and the Apache patent grant."
sources:
  - https://opensource.org/license/mit
  - https://opensource.org/license/bsd-2-clause
  - https://opensource.org/license/bsd-3-clause
  - https://opensource.org/license/isc
  - https://opensource.org/license/apache-2-0
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Permissive licences: MIT, BSD, Apache, ISC

Goal: comply with permissive terms without over-worrying.

- MIT: the copyright notice and permission notice must be included in all copies or substantial portions.
- ISC: the copyright notice and permission notice must appear in all copies.
- BSD-2-Clause: source redistributions retain the copyright notice, conditions and disclaimer; binary redistributions reproduce them in the documentation and/or other materials provided with the distribution.
- BSD-3-Clause: adds that the copyright holder's and contributors' names may not be used to endorse or promote derived products without written permission.
- Apache-2.0 (section 4): give recipients a copy of the licence; mark modified files with prominent change notices; retain copyright, patent, trademark and attribution notices in the Source form; if the Work has a NOTICE file, include a readable copy of its attributions in a NOTICE file, in the source or documentation, or in a display of the Derivative Work. NOTICE contents are informational and do not modify the licence.
- Apache-2.0 also grants a patent licence (section 3) that terminates if you start patent litigation alleging the Work infringes. Section 6 grants no trademark rights.
- None of these texts requires you to disclose source for your own code. Apache-2.0 lets you add your own terms to your modifications provided the Work's conditions are still met.

## Method
Collect licence texts and NOTICE contents into a third-party notices file shipped with the product.

## Gotchas
- Binary distributions still carry duties (BSD-2/3 require reproduction in documentation or other materials); put notices in an About screen or documentation.
- All of these disclaim warranty on an "as is" basis.

## Verify
- [ ] The release artefact contains the notices file.

## Checked
2026-11-08. Confirmed against the OSI pages for MIT, BSD-2-Clause, BSD-3-Clause, ISC and Apache-2.0, all read in full. Removed: the claim that Apache-2.0 is incompatible with GPLv2-only (the GNU page could not be read), and the bulk-generated ISO, SPDX, CycloneDX, NTIA, OpenChain, REUSE and GNU sources. Corrected: the patent termination applies to a licensee who sues, not "a contributor".
Method: documentation only; no commands were run.
