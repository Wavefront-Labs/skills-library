---
id: business-finance.investing-and-trading.bloomberg-terminal.core-functions-and-excel-data-pulls
name: core-functions-and-excel-data-pulls
category: business-finance
field: investing-and-trading
product: bloomberg-terminal
tags: [bloomberg-terminal, bloomberg, bbg, terminal-functions, yellow-keys, security-lookup, des, gp, fa, rv, ee, cn, eqs, srch, yas, eco, flds, launchpad, blp, bloomberg-excel-add-in, bdp, bdh, bds, bql, data-license, market-data, equity-research, fixed-income-analytics]
level: practitioner
status: draft
description: "Work the Bloomberg Terminal efficiently: load securities with yellow keys, the core research functions, screening, field lookup, Launchpad monitors and BDP/BDH/BDS pulls in Excel."
sources: ["Bloomberg Terminal built-in help (HELP key, BU <GO> training)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bloomberg Terminal: core functions and Excel data pulls

**Goal:** get from "I need X about this security" to the right screen or spreadsheet
in seconds, and pull data into Excel in a way that refreshes and doesn't blow your
data limits. Function mnemonics below are long-standing ones, but Bloomberg revises
screens often — **press HELP on any screen, or search the command line, to confirm**;
this draft was not re-checked on a live terminal.

## 1. Loading a security
Syntax: `<identifier> <yellow key> <function> <GO>`.
- Yellow (market sector) keys: **Equity**, **Corp** (corporate bonds), **Govt**,
  **Index**, **Curncy**, **Comdty**, **Mtge**, **Muni**, **Pfd**.
- Equities use ticker + exchange code: e.g. `VOD LN <Equity>`, `AAPL US <Equity>`
  (composite).
- Bonds: ticker + coupon + maturity, or ISIN/CUSIP followed by Corp/Govt.
- Unsure of the ticker? Type a name in the command line and pick from autocomplete.
- Once loaded, functions you type apply to that security until you load another.

## 2. Core functions (one-line purpose each)
- **DES** — description: business, key data, share structure.
- **GP** (price graph), **HP** (historical price table), **GIP** (intraday).
- **FA** — financial analysis: statements, ratios, segments, estimates.
- **EE** — earnings estimates and consensus; **ERN** earnings history.
- **RV** — relative valuation vs peers; **COMP** comparative returns.
- **CN** — company news; **TOP** — top headlines; **N** — news search.
- **DVD** dividends; **CACS** corporate actions; **HDS** holders.
- **EQS** — equity screening; **SRCH** — bond search.
- **YAS** — yield and spread analysis for bonds; **GC** — curves.
- **ECO** — economic calendar; **WEI** — world equity indices.
- **ALRT** — alerts; **MSG** / **IB** — email and instant messaging.
- **FLDS** — find the field mnemonic for any data point (essential for Excel).
- **BU** — Bloomberg University training; **HELP HELP** to reach the help desk.

## 3. Launchpad monitors
**BLP <GO>** opens Launchpad: build pages of monitors (watchlists with chosen
columns), charts, news panes and saved function views. Keep one page per workflow
(morning markets, coverage list, positions). Monitors can be fed from lists you also
use in Excel and screens.

## 4. Excel add-in formulas
- `=BDP("AAPL US Equity","PX_LAST")` — current/reference data point.
- `=BDH("AAPL US Equity","PX_LAST","2024-01-01","2024-12-31","Per","M")` —
  historical time series (here monthly). Optional overrides control currency,
  fill, calendar, adjustments for splits/dividends.
- `=BDS("AAPL US Equity","DVD_HIST_ALL")` — bulk/tabular data sets.
- Find field names in **FLDS**, or via the add-in's field search; check the field's
  definition, not just its name (e.g. `PX_LAST` vs `PX_CLOSE_1D`).
- **BQL** (Bloomberg Query Language) handles universes and calculations in one
  query for screens and cross-sections; worth learning for repeatable analyses.
- Use the **Spreadsheet Builder** wizard to generate formulas while learning.

## Gotchas
- **Data limits:** terminal Excel pulls are capped (daily/monthly). Huge BDH grids
  refreshing on every recalc can exhaust them; set calculation to manual or paste
  values for archive copies.
- **Licensing:** terminal data is for the licensed user; redistributing it (e.g.
  publishing extracted data, sharing workbooks that refresh outside the licence) may
  breach terms — check your firm's Bloomberg agreement.
- **Ticker changes** after corporate actions break historical pulls — use ISIN/FIGI or
  Bloomberg IDs for long histories.
- **Adjusted vs unadjusted prices:** set the override deliberately for return work.
- Login is tied to a person and device (B-Unit biometric); never share credentials.

## Verify
- [ ] You can load an equity, bond and index with the correct yellow key.
- [ ] DES, FA, GP, EE, CN and RV checked for a coverage name in under a minute.
- [ ] Excel uses BDP/BDH/BDS with fields confirmed in FLDS and explicit overrides.
- [ ] Heavy workbooks don't refresh unnecessarily; archive copies pasted as values.
- [ ] Data use stays within your firm's licence.
