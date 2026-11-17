---
id: computing-software.data-engineering.data-modelling.grain-and-fact-table-design
name: grain-and-fact-table-design
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, fact-table, grain, transaction-fact, periodic-snapshot, accumulating-snapshot, factless-fact, degenerate-dimension, additive-measure, semi-additive-measure, kimball, star-schema, measure-types]
level: practitioner
status: draft
description: "Pick the correct fact table grain and type (transaction, periodic/accumulating snapshot) before any fact table is built."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fact table grain — the one decision that must be made first

**Goal:** declare the grain in one sentence before writing a single column, because every downstream bug ("double-counted revenue," "can't answer this question," "aggregation doesn't match the source system") traces back to grain confusion.

## 1. Declare the grain explicitly, in writing, before modeling
The grain is "one row represents ___" — e.g. "one row per line item per order" or "one row per account per day." Write it down in the table's documentation verbatim. If you can't state it in one sentence, the table isn't ready to build. The most common real-world failure is a fact table that's *almost* at the stated grain — one row per order mostly, except promotions add a second row for the same order — which silently breaks every `SUM(revenue)` downstream without erroring.

## 2. The three fact table types — pick by the question being answered
- **Transaction fact**: one row per discrete event (an order line, a page view, a payment). Finest possible grain, most flexible, grows unbounded with activity volume. Measures are typically fully additive (sum them across any dimension safely).
- **Periodic snapshot**: one row per entity per fixed time period (e.g. one row per account per month showing balance). Built for "what was the state at time X" and trend-over-time questions a transaction fact answers only with expensive aggregation. Non-additive across the time dimension itself (don't sum monthly balances across 12 months to get an annual "balance" — that's meaningless; see semi-additive below).
- **Accumulating snapshot**: one row per process instance (an order, a support ticket), updated in place as it moves through a pipeline — columns for each major milestone's date/duration (order_date, ship_date, delivered_date). Built for pipeline/funnel analysis ("average days from order to ship"). The *only* fact table type designed to be updated after insert — every other fact type is insert-only; this is the deliberate exception, and the row is revisited and overwritten as the process advances, not appended.
- **Factless fact**: no measures at all, just a set of dimension keys recording that an event/coverage occurred (e.g. "student attended class on date X," or a coverage table of "promotion X was active for product Y on date Z"). Measured by counting rows, not summing a column — easy to miss as a legitimate pattern and over-engineer with a dummy "count=1" column instead.

## 3. Additive, semi-additive, non-additive measures
- **Fully additive** (revenue, quantity, order count): safe to `SUM()` across every dimension, including time. The default assumption, and the type transaction facts should mostly contain.
- **Semi-additive** (account balance, inventory on hand): safe to sum across every dimension *except time* — summing balances across 12 month-end snapshots doesn't give a meaningful annual figure; the correct annual rollup is usually the last period's value (`LAST_VALUE` or a point-in-time read), not a sum. This is the single most common dashboard bug in periodic-snapshot facts.
- **Non-additive** (a ratio, a percentage, an average already computed upstream): never sum directly; store the components (numerator, denominator) and compute the ratio at query time, or it silently becomes wrong the moment it's aggregated at a different grain than it was computed at.

## 4. Degenerate dimensions and grain leakage
A **degenerate dimension** (order number, invoice number) lives in the fact table with no corresponding dimension table — it's an identifier, not an attribute, and belongs at the fact's grain. Grain leakage happens when someone adds a column to a fact table that doesn't exist at the declared grain (e.g. adding `customer_signup_date` directly onto a line-item fact) — this either duplicates that value across every line item (wasteful but survivable) or, worse, becomes subtly wrong when the customer's signup date changes and old fact rows don't get updated. Put it in the dimension it actually belongs to instead.

## Verify
- [ ] The grain is written as one literal sentence in the table's docs/DDL comment, and a sample query confirms exactly one row per that sentence's unit (no duplicates, no missing combinations).
- [ ] Every measure column is labeled additive/semi-additive/non-additive, and dashboards summing a semi-additive measure across time were checked and fixed if wrong.
- [ ] No column exists on the fact table that varies at a grain coarser or finer than the declared one.
- [ ] An accumulating snapshot fact's "update in place" logic is the only fact table in the model that issues UPDATEs — everything else is insert-only.
