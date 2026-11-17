---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.fsf-free-software-and-compatibility
name: fsf-free-software-and-compatibility
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [fsf-free-software-and-compatibility, licence-classification-osi-fsf, fsf, gpl-compatible, gpl-incompatible, apache-2-0, mpl-2-0, original-bsd, gpl-faq, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Check GPL compatibility before combining code: what the GPL FAQ, Apache and MPL-2.0 pages say about Apache-2.0, MPL-2.0, original BSD and GPLv2 versus GPLv3."
sources:
  - https://www.gnu.org/licenses/gpl-faq.html
  - https://www.apache.org/licenses/GPL-compatibility.html
  - https://www.mozilla.org/en-US/MPL/2.0/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSF free software classification and GPL compatibility

Goal: check compatibility before combining code. This skill states what the cited pages say; it is not legal advice.

- Meaning of "compatible": per the GNU GPL FAQ, a licence is GPL-compatible if you can combine code under it with GPL code in one larger program. All GPL versions permit such combinations privately and permit distribution provided the combination is released under the same GPL version; the other licence is compatible if it permits this too.
- Combining versus running together: installing two separate programs on one system does not combine them into a larger work, so their licences need not be compatible.
- Free software licence: the FAQ says any licence that provides the user certain specific freedoms is a free software licence, and that the FSF list is incomplete.
- GPLv2 and GPLv3 are not compatible with each other, per the FAQ (combining GPLv2-only and GPLv3 code would violate section 6 of GPLv2). Code released as "version 2 or later" is compatible with GPLv3. GPLv3 is compatible with more licences than GPLv2 because section 7 permits specific additional requirements.
- Apache-2.0: the Apache Software Foundation page says the FSF considers it a free software licence compatible with GPL version 3 (so Apache 2 code can be included in GPLv3 projects, but not the reverse), and that the FSF has never considered it compatible with GPL version 2, citing the patent termination and indemnification provisions.
- Original BSD (with the advertising clause): the FAQ says it is GPL-incompatible because the advertising requirement is a further restriction (GPLv2 section 6; GPLv3 section 10). The revised BSD licence has no advertising clause, which removes the problem.
- MPL-2.0: the licence text defines "Secondary License" as the GNU GPL 2.0, LGPL 2.1, AGPL 3.0 or any later versions of those, and section 3.3 (Larger Work) refers to Secondary Licenses. Read section 3.3 itself before relying on it for a given combination.
- AGPL-3.0 and GPL-3.0: the FAQ says each explicitly permits linking with code under the other.

Method: look up each component's licence and the combination (linking, merging into one module, or separate programs), and record the determination and the page you used in the component approval. For licences not covered here (CDDL, EPL and others), read the FSF licence list directly; it was not readable when this skill was checked.

Gotchas:
- Compatibility is about combining into one work, not about running programs together.
- Vendor and foundation statements are positions, not court rulings; take legal advice on borderline cases.

Verify: link the determination and its source page in the approval record.

## Checked

2026-11-08. Confirmed against the GNU GPL FAQ (compatibility meaning, separate programs, free software licence, GPLv2/GPLv3, original BSD, AGPL/GPL linking), the Apache GPL-compatibility page (Apache-2.0 versus GPLv3 and GPLv2) and the MPL-2.0 text (Secondary License definition). Removed: the four-freedoms wording, and the CDDL and EPL-1.0 incompatibility examples, because the FSF licence list and philosophy pages on gnu.org could not be fetched (connection refused). The ISO, SPDX, CycloneDX, NTIA, OpenChain and REUSE sources supported no remaining claim and were dropped. MPL-2.0 section 3.3 body text was not readable, so it is cited by name only.
Method: documentation only; no commands were run.
