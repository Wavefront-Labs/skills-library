---
id: computing-software.data-engineering.data-modelling.date-and-time-dimensions
name: date-and-time-dimensions
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, dimensional-modelling, date-dimension, time-dimension, fiscal-calendar, date-spine, iso-week, holidays, smart-keys, kimball]
level: practitioner
status: gated
description: "Build date and time-of-day dimensions: generating a date spine, smart date keys, ISO weeks, fiscal calendars (4-4-5), holidays, special rows, and separating date from time grain."
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/calendar-date-dimension/
  - https://github.com/dbt-labs/dbt-utils#date_spine-source
  - https://en.wikipedia.org/wiki/ISO_week_date
  - https://en.wikipedia.org/wiki/4%E2%80%934%E2%80%935_calendar
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date and time-of-day dimensions

**Goal:** one calendar every fact table joins to, so "this fiscal quarter", "same week last year" and "business days" mean the same thing in every report.

## 1. Grain and key
- One row per calendar day. Separate **time-of-day** dimension (one row per minute or second: 1,440 / 86,400 rows) if you analyse by hour; never combine date and time into one dimension (billions of rows).
- Key: smart integer `date_key = YYYYMMDD` (20261016). Readable, sortable, partition-friendly. This is the accepted exception to meaningless surrogate keys.
- Special rows: `-1` / `19000101` "Unknown", `99991231` "Not yet happened" (open-ended accumulating snapshot dates). Facts with NULL dates point here so inner joins don't drop rows.

## 2. Generate the spine
```sql
-- dbt
{{ dbt_utils.date_spine(datepart="day", start_date="cast('2000-01-01' as date)", end_date="cast('2040-01-01' as date)") }}
-- Snowflake
SELECT DATEADD(day, SEQ4(), '2000-01-01'::date) AS d FROM TABLE(GENERATOR(ROWCOUNT => 14610));
-- BigQuery
SELECT d FROM UNNEST(GENERATE_DATE_ARRAY('2000-01-01', '2039-12-31')) AS d;
-- Postgres
SELECT d::date FROM generate_series('2000-01-01'::date, '2039-12-31', interval '1 day') d;
```
Cover all history plus future dates needed for plans/forecasts; 2000-01-01 to 2039-12-31 is 14,610 rows (computed) — trivial. The DuckDB `generate_series` form and the dbt `dbt_utils.date_spine` macro (dbt_utils 1.4.1 on dbt-duckdb; `end_date` is exclusive, so the 2040-01-01 end gave 2000-01-01..2039-12-31) were run. The Snowflake, BigQuery and Postgres spine snippets are unrun (gated: unconfirmed, source is paywalled or blocked).

## 3. Attributes worth having
`date_key, full_date, day_of_week (ISO 1=Mon), day_name, is_weekend, day_of_month, day_of_year, week_start_date, iso_year, iso_week, month, month_name, month_start, month_end, quarter, year, is_last_day_of_month, fiscal_year, fiscal_quarter, fiscal_period, fiscal_week, is_holiday_<country>, holiday_name, is_business_day, business_day_of_month, same_day_last_year_key`.
- **ISO year ≠ calendar year** around New Year (computed: 2026-12-31 is ISO 2026-W53; 2021-01-01 is ISO 2020-W53, so `year` and `iso_year` differ). Use `iso_year` with `iso_week` — mixing `year` with `iso_week` is a classic bug.
- Week start (Mon vs Sun) differs by country/engine defaults — store it explicitly.

## 4. Fiscal calendars
- Offset fiscal year (FY starts 1 April): `fiscal_year = year + CASE WHEN month >= 4 THEN 1 ELSE 0 END` (or same-year convention — confirm with finance which naming they use).
- Retail 4-4-5 / 4-5-4 / 5-4-4: periods are whole weeks; a 53rd week appears every 5-6 years. Don't compute — load the official fiscal calendar from finance as a seed table and join it.

## 5. Holidays and business days
Load per-country holidays (seed, or a library like Python `holidays` at build time) into a bridge `date_key, country, holiday_name`; derive `is_business_day` per country if you operate in several. Compute "N business days later" with a running business-day counter column, not with date arithmetic.

## 6. Role-playing
One physical date dimension serves order date, ship date, due date via views/aliases (`dim_order_date`, `dim_ship_date`) — see role-playing dimensions.

## Verify
- [ ] No gaps: row count = days between min and max date + 1.
- [ ] Every fact date key matches a dimension row (including Unknown).
- [ ] Spot checks: ISO week for 2020-12-31 (week 53), fiscal period boundaries agreed with finance.
