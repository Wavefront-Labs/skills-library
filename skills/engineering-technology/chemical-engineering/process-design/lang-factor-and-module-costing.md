---
id: engineering-technology.chemical-engineering.process-design.lang-factor-and-module-costing
name: lang-factor-and-module-costing
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-capital-cost-estimation, lang-factor-and-module-costing, lang-factor, bare-module-cost, module-costing, installed-cost, fixed-capital-investment, total-capital, factored-estimate]
level: practitioner
status: draft
description: "Convert purchased equipment cost to fixed capital with Lang factors or module (bare-module) costing, and understand what each includes and where it misleads."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lang factor and module costing

**Goal:** total capital from equipment cost by a factored method, with the limits understood.

## Lang factors
Fixed capital = Lang factor x sum of delivered equipment cost. Commonly quoted Lang factors are about 3.1 for solids processing, about 3.6 for mixed solid-fluid processing and about 4.7 for fluid processing (Peters, Timmerhaus and West; confirm values in the edition you use). The factor lumps installation, piping, instrumentation, electrical, buildings, yard, engineering, construction and contingency.

## Module costing (Turton et al.)
For each equipment item: C_BM = C_p0 x F_BM, where F_BM combines material, pressure and installation factors. Total module cost C_TM = 1.18 x sum C_BM (contingency and fee, as published). Grass-roots cost adds auxiliary facilities (published as an additional share of base-case module costs, for example 0.5 x sum of C_BM at base conditions). Confirm the factors in your edition.

## Detailed factoring
Alternative is the Hand or Peters approach: installation, piping, instruments, electrical, buildings, yard, services as separate percentages of equipment cost, adjusted to project type (grassroots, expansion, retrofit).

## Procedure
1. Total delivered equipment cost from the correlation step.
2. Choose method by project type and accuracy needed.
3. Add owner's costs and start-up, working capital separately.
4. Compare the result against a ratio to a similar project ($ per annual tonne).

## Gotchas
- Lang factors are for whole-plant order-of-magnitude; they overstate small modifications and understate harsh-materials plants.
- Retrofit projects differ greatly; use project-specific factors.

## Verify
- [ ] Method, factors and edition recorded.
- [ ] Sanity check against capital intensity of comparable plants.
