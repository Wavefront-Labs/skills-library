---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.lifecycle-stages-model
name: lifecycle-stages-model
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [lifecycle-stages-model, asset-lifecycle-management, lifecycle states, asset status, ordered, in stock, retired, itam-licence-compliance]
level: intro
status: draft
description: "Define lifecycle states (requested to disposed) with allowed transitions and the evidence each transition needs."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Asset lifecycle stages and state model

Goal: a single status vocabulary so reports and automation agree.

Typical states: Requested, Ordered, Received, In stock, Assigned/In use, In repair, Retired, Disposed, Lost/Stolen.

Method:
- Draw allowed transitions (e.g. Received to In stock to Assigned; never Disposed back to In use).
- Attach required evidence: PO number at Ordered, delivery note at Received, user acknowledgement at Assigned, certificate of destruction at Disposed.
- Enforce in the ITAM tool as a state machine; block invalid jumps.
- Separate operational status from financial status (capitalised, depreciated, written off).

Gotchas:
- Too many states cause stale data; keep under ten.
- Stock held by IT versus by users must be distinguishable.

Verify: a report of assets older than N days in Ordered or In repair should be near empty.
