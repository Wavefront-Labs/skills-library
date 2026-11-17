---
id: computing-software.data-science-and-analytics.bi-tools.tableau-table-calcs-parameters
name: tableau-table-calcs-parameters
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [tableau-table-calculation, tableau-parameters, tableau-sets]
level: practitioner
status: docs-checked
description: "Use table calculations (rank, running total, percent of total) with correct addressing, and parameters to make Tableau views interactive."
sources:
  - https://help.tableau.com/current/pro/desktop/en-us/calculations_tablecalculations.htm
  - https://help.tableau.com/current/pro/desktop/en-us/parameters_create.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table calcs, parameters
- A table calculation transforms the values in the visualization (rankings, running totals, percent of total). It computes on local data using the virtual table defined by the dimensions in the level of detail; add one with right-click on the measure > Add Table Calculation.
- Every dimension in the level of detail is either a partitioning field (scope; the calculation restarts per partition) or an addressing field (direction). Compute Using options (Table across/down, Pane, Cell) set these automatically; Specific Dimensions lets you choose, and "At the level" is available only with Specific Dimensions and more than one addressing dimension.
- A parameter is a workbook variable (number, date, string) that replaces a constant in a calculation, filter (Top N) or reference line. Create it from the Data pane dropdown > Create Parameter; accept values as All, List or Range (Range needs minimum, maximum and step size; a string parameter does not support Range).
- A parameter does nothing until referenced and exposed: Show Parameter control, a parameter action (clicking marks) or a dynamic parameter.
## Gotchas
- Table calculations do not consider measures or dimensions filtered out of the visualization, so filtered rows drop out of totals; wrong Compute Using / addressing is the usual bug.
- Deleting a parameter invalidates calculated fields that use it.
- A dynamic current value from a calculation must be a single-value, view-independent calculation (use a FIXED LOD); do not use a dynamic parameter in an extract filter, which hurts performance.
## Verify
- [ ] Change the parameter and confirm the view updates; compare running totals with a pivoted table.

## Checked
Confirmed on the table calculations page: definition, partitioning versus addressing, Compute Using options, At the level, filter behaviour. Confirmed on the create parameters page: definition, creation steps, All/List/Range, usage in calculations/filters/reference lines, controls, parameter actions, dynamic current value rules, deletion. Removed: function examples (RUNNING_SUM, RANK, LOOKUP) and the description of sets, which neither page covers; the "sets" tag is kept for continuity only.
Method: docs-checked 2026-11-09 against the Tableau Help table calculations and create parameters pages, both read in full.
