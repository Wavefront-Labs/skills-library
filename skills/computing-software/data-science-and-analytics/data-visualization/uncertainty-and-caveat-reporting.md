---
id: computing-software.data-science-and-analytics.data-visualization.uncertainty-and-caveat-reporting
name: uncertainty-and-caveat-reporting
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [uncertainty-communication, limitations-section, correlation-vs-causation]
level: practitioner
status: draft
description: "Show intervals, sample sizes and data limitations and separate association from causal claims in reports."
sources:
  - https://www.storytellingwithdata.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Honest reporting
- Always show n and interval (error bars with the type stated: SE, SD, 95% CI).
- Use cautious causal wording unless randomised or a defensible design exists.
- List data exclusions, definitions, known measurement issues.
- Version the dataset and code behind each number.
## Gotchas
- Dropping bars to zero error looks precise; do not hide spread.
## Verify
- [ ] Every number in the report traces to a script and a data snapshot.
