---
id: computing-software.ux-hci-design.interaction-design.hicks-law-and-choice-overload
name: hicks-law-and-choice-overload
category: computing-software
field: ux-hci-design
product: interaction-design
tags: [hicks-law, choice-overload]
level: practitioner
status: draft
description: "Reduce decision time by limiting and chunking choices rather than applying a fixed 7 plus or minus 2 rule."
sources:
  - https://lawsofux.com/hicks-law/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hick's law
RT = b * log2(n + 1): decision time grows with the number of equally likely choices.
- Cut or group options; highlight a recommended default; progressive disclosure.
- Miller's 7 plus or minus 2 is about short-term memory, not a menu size limit; do not use it to cap navigation.
- Do not remove choices at the cost of task completion; categorise and make scannable.

## Verify
- [ ] Time to selection and error rate in testing improve after trimming.
