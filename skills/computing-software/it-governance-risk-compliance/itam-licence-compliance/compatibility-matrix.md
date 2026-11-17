---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.compatibility-matrix
name: compatibility-matrix
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [compatibility-matrix, licence-compatibility-analysis, combining-licences, inbound-outbound, gpl-compatibility, licence-conflict, lgpl, itam-licence-compliance]
level: advanced
status: docs-checked
description: "Decide whether components under different licences can be combined, using the GNU GPL FAQ and the Apache GPL-compatibility page; not legal advice."
sources:
  - https://www.gnu.org/licenses/gpl-faq.html
  - https://www.apache.org/licenses/GPL-compatibility.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compatibility matrix and combination rules

Goal: choose an outbound licence that satisfies all inbound licences. This skill records what the cited pages say; have counsel sign off on real combinations.

Method:
- List inbound licences, with exact SPDX identifiers (GPL-2.0-only and GPL-2.0-or-later differ), for every component in a combined work.
- GPL rule from the GNU GPL FAQ: all GPL versions permit combining GPL code with code under another licence, and distributing the combination provided it is released under the same GPL version; the other licence is GPL-compatible if it permits this too. Aggregates of separate programs on the same media are different: the GPL permits them even when the other licences are nonfree or GPL-incompatible, provided the aggregate is not released under a licence that takes away rights each program's licence grants.
- GPL-2.0-only with GPL-3.0 code: not compatible (the FAQ says combining them would violate section 6 of GPLv2). "Version 2 or later" code is compatible with GPLv3.
- Apache-2.0: the Apache Software Foundation page says it can be included in GPLv3 projects but GPLv3 software cannot be included in Apache projects, and that the FSF has never considered Apache-2.0 compatible with GPL version 2.
- Original BSD with the advertising clause is GPL-incompatible; revised BSD is not (FAQ).
- AGPL-3.0 and GPL-3.0 code can be linked in both directions (FAQ).
- LGPL: the FAQ says that if you statically link an LGPL library you must also provide your application in an object (not necessarily source) format so the user can modify the library and relink; if you dynamically link a library already on the user's computer you need not convey its source; if you convey the LGPL library yourself you must convey its sources. The FAQ adds that LGPL libraries can be used in nonfree programs but with requirements you must follow.
- Conflicts: remove or replace the component, keep it a separate program, or obtain permission from its copyright holders. Only they can add exceptions (FAQ).

Gotchas:
- "Or later" must be in the component's licence for later-version compatibility to apply.
- Documents, fonts and data have their own licences; check each separately.

Verify: legal sign-off is recorded for each product's combination, naming the pages used.

## Checked

2026-11-08. Confirmed against the GNU GPL FAQ (compatibility meaning, aggregates, GPLv2/GPLv3, original BSD, AGPL/GPL, LGPL static and dynamic linking, only copyright holders add exceptions) and the Apache GPL-compatibility page. Removed: the blanket statements that any GPL-3.0 inbound forces a GPL-3.0 outbound and that LGPL outbound can always be proprietary, replaced by the FAQ's conditions; the CC BY-SA and OFL examples (not supported by a fetched page). ISO, SPDX, CycloneDX, NTIA, OpenChain, REUSE and OSI sources supported no remaining claim and were dropped.
Method: documentation only; no commands were run.
