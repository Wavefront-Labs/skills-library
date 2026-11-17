---
id: computing-software.general-digital-literacy.office-suites.goal-seek-and-what-if-analysis
name: goal-seek-and-what-if-analysis
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, sort-and-filter, goal-seek, what-if-analysis, scenario-manager, data-table]
level: practitioner
status: docs-checked
description: "Work backwards to a target with Excel Goal Seek, compare options with Scenario Manager and data tables, e.g. the loan payment or price that hits a goal."
sources:
  - https://support.microsoft.com/en-us/office/introduction-to-what-if-analysis-22bffa5f-e891-4acc-bf7a-e4645c446fb4
  - https://support.microsoft.com/en-us/excel/use-goal-seek-to-find-the-result-you-want-by-adjusting-an-input-value
  - https://support.microsoft.com/en-us/excel/define-and-solve-a-problem-by-using-solver
  - https://support.google.com/docs/answer/9506732
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Goal Seek and what-if analysis

## Goal Seek (one unknown)
Example: what loan amount gives a £400 monthly payment?
1. Model: B1 rate 5%, B2 months 60, B3 amount 20000, B4 `=PMT(B1/12,B2,-B3)`.
2. Data › **What-If Analysis › Goal Seek** › Set cell **B4** › To value **400** › By changing
   **B3** › OK.
3. Accept or Cancel. It changes the input cell's value (keep a copy of the original).
- Goal Seek works with a single input value. The *Set cell* must be a formula that depends
  (directly or indirectly) on the changing cell.

## Data table (one or two inputs, many results)
A data table cannot take more than two variables. Rates down A8:A14, amounts across B7:F7,
top-left A7 `=B4`. Select A7:F14 › What-If Analysis › **Data Table** › Row input B3, Column input
B1. Gives a grid of payments.

## Scenario Manager (named sets of inputs)
What-If Analysis › **Scenario Manager** › Add "Best", "Worst" with changing cells. A scenario holds
up to 32 variable values.

## Solver (several unknowns, constraints)
An add-in you activate first; use it when more than one input must change or you need a min or max
subject to constraints. It is not available in Excel for the web.

## Google Sheets
Goal Seek is an add-on installed from the Extensions menu (Google's help says it is English-only);
otherwise build a small table of trial inputs.

## Verify
- [ ] Put the found input back in manually: the formula returns the target.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft what-if analysis pages (Scenario Manager holds up to 32 variable values; a data table accepts at most two variables; Goal Seek works with one input; Solver is an add-on that must be activated and is not available in Excel for the web), Google Sheets Goal Seek help (add-on installed from Extensions; English only).
Method: documentation only; no commands were run.
