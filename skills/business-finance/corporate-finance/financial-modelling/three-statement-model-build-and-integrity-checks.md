---
id: business-finance.corporate-finance.financial-modelling.three-statement-model-build-and-integrity-checks
name: three-statement-model-build-and-integrity-checks
category: business-finance
field: corporate-finance
product: financial-modelling
tags: [financial-modelling, financial-modeling, three-statement-model, 3-statement-model, income-statement, balance-sheet, cash-flow-statement, balance-check, circular-reference, interest-circularity, working-capital, debt-schedule, model-architecture, assumptions-sheet, fast-standard, model-audit, scenario-switch, sensitivity-analysis, excel, dcf]
level: practitioner
status: draft
description: "Build a linked three-statement model that balances: sheet architecture, driver-based forecasts, working capital and debt schedules, the cash flow link, circularity and checks."
sources: ["FAST Standard (fast-standard.org)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Three-statement model: build and integrity checks

**Goal:** a model where income statement, balance sheet and cash flow are mechanically
linked, the balance sheet balances in every period without a plug, and someone else
can audit it in an hour.

## 1. Architecture
- **Inputs → calculations → outputs**, separated by sheet or block. Inputs are the only
  hard-coded numbers; colour them (blue font is the common convention), everything else
  is a formula (black).
- One **timeline** row at the top of every calc sheet; identical columns across sheets
  so period N is always the same column. Flags (`=AND(date>=start, date<=end)`) switch
  logic on and off by period instead of different formulas per column.
- **One formula per row**, copied across. A row that changes formula mid-way is the
  most common source of hidden errors.
- Keep a **checks** sheet and an aggregate check on the cover.

## 2. Forecast order
1. **Historicals** (3 years if available), restated to a consistent layout.
2. **Revenue drivers** (volume × price, customers × ARPU, or growth % if nothing better).
3. **Costs** as % of revenue or bottom-up; fixed vs variable.
4. **Working capital** by days: receivables = revenue × DSO/365; inventory = COGS ×
   DIO/365; payables = COGS (or purchases) × DPO/365.
5. **Capex and depreciation** via a fixed-asset roll-forward: opening + capex −
   depreciation − disposals = closing.
6. **Debt schedule** per facility: opening + drawdowns − repayments = closing; interest
   on average or opening balance.
7. **Tax**, dividends, equity roll-forward.

## 3. Linking the statements
- Net income → retained earnings (equity roll-forward) and the top of the cash flow.
- Cash flow from operations = net income + non-cash items (D&A) − increase in working
  capital. Investing = −capex + disposals. Financing = debt drawn − repaid + equity −
  dividends.
- **Closing cash on the balance sheet = opening cash + net cash flow.** Cash is the
  only balance-sheet line that comes from the cash flow; every other BS line comes from
  its own schedule.
- Revolver / minimum cash: if cash falls below the minimum, draw the revolver; this
  plus interest on average balances creates a **circular reference**. Either compute
  interest on opening balances, or use a circularity **breaker switch** (an input that
  zeros the circular term) with iterative calc — never leave unexplained iterations on.

## 4. Integrity checks
- **Balance check:** assets − liabilities − equity = 0, every period (round to e.g.
  0.001 to avoid floating-point noise).
- Cash flow closing cash = BS cash.
- Retained earnings roll-forward ties.
- Debt and asset roll-forwards tie to BS.
- No negative cash without a revolver; no negative debt.
- Sum of quarters = annual where both exist.

## Debugging an imbalance
Find the **first period** that fails. If the difference equals a line item's change,
that item is missing from the cash flow (or double-counted). Signs matter: an increase
in an asset is a cash *outflow*. A difference that grows by the same amount each
period is usually a missing non-cash item.

## Gotchas
- Hard-codes inside formulas (`=B10*1.05`) — move the 1.05 to inputs.
- Plugs to force a balance hide the actual error; delete them.
- Mixing signs conventions (costs positive vs negative) across sheets.
- Merged cells and hidden rows break copying and auditing.

## Verify
- [ ] Balance check = 0 in every historical and forecast period, no plugs.
- [ ] Cash flow closing cash equals balance sheet cash every period.
- [ ] All hard-codes live on input sheets; one formula per row.
- [ ] Circularity has a breaker switch or is designed out.
- [ ] A flex of a key input (e.g. revenue −10%) flows through all three statements.
