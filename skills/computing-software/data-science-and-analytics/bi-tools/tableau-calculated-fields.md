---
id: computing-software.data-science-and-analytics.bi-tools.tableau-calculated-fields
name: tableau-calculated-fields
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [tableau-calculated-field, tableau-if-case, tableau-aggregate-calculation, tableau-calcs]
level: practitioner
status: draft
description: "Create row-level and aggregate calculated fields with IF, CASE and string/date functions and avoid mixing aggregate and non-aggregate arguments."
sources:
  - https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calculated fields
```
IF [Profit] < 0 THEN "Loss" ELSEIF [Profit] = 0 THEN "Even" ELSE "Gain" END
SUM([Profit]) / SUM([Sales])            // ratio of sums, not average of ratios
DATETRUNC('month', [Order Date])
ZN([Quantity])                          // null to zero
```
## Gotchas
- "Cannot mix aggregate and non-aggregate arguments": wrap everything in aggregates or use LOD.
- Aggregate ratios must be computed after summing, so build them as one calculated field.
## Verify
- [ ] Compare the calculation with a hand total for one mark.
