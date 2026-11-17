---
id: computing-software.database-administration.schema-design.money-and-exact-numeric-types
name: money-and-exact-numeric-types
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, data-type-selection, decimal-money, numeric, integer-cents, floating-point, currency, rounding, money-type]
level: practitioner
status: gated
description: "Store money exactly: NUMERIC/DECIMAL with explicit scale or integer minor units plus a currency code, never FLOAT, and handle rounding and multi-currency correctly."
sources:
  - https://www.postgresql.org/docs/current/datatype-numeric.html
  - https://dev.mysql.com/doc/refman/8.4/en/fixed-point-types.html
  - https://www.iso.org/iso-4217-currency-codes.html
  - https://www.postgresql.org/docs/16/datatype-numeric.html
  - https://www.postgresql.org/docs/16/datatype-money.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Money and exact numeric types

**Goal:** sums of money are exact to the cent, in every engine and language that touches them.

## Never binary floating point
`FLOAT`/`REAL`/`DOUBLE` cannot represent 0.10 exactly:
`SELECT 0.1::float8 + 0.2::float8 = 0.3::float8;` → false (run on PostgreSQL 16.4; the numeric version is true, and `sum` of float8 0.1 and 0.2 gave 0.30000000000000004). Errors accumulate in
sums and comparisons (`WHERE amount = 19.99` misses rows).

## Two correct options
1. **Decimal with explicit scale**
   ```sql
   amount NUMERIC(19,4) NOT NULL,      -- PostgreSQL / Oracle NUMBER(19,4)
   amount DECIMAL(19,4) NOT NULL,      -- MySQL / SQL Server
   currency CHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$')   -- ISO 4217
   ```
   Scale 4 leaves room for intermediate calculations (tax, FX); round to the
   currency's minor unit when presenting or settling.
2. **Integer minor units**: `amount_minor BIGINT` (cents) + `currency`. Fast,
   exact, language-friendly; the minor-unit exponent differs per currency (JPY 0,
   USD 2, KWD 3; confirmed from CLDR data via Babel; ISO 4217 itself is the authority), so store or look it up per currency.

## Avoid
- PostgreSQL `money` type: depends on `lc_monetary` (checked: `'12.5'::money` printed `$12.50` under a US locale setting), a single currency, awkward casts.
- SQL Server `money`/`smallmoney`: fixed 4 decimals and lossy multiplication/division rounding (gated: unconfirmed, source is paywalled or blocked); DECIMAL is safer.
- Unscaled `NUMERIC` (no precision): accepts arbitrary scale, so 10.005 and 10.01 coexist (checked).

## Rounding rules
- Decide the rounding mode per business rule (half-up for invoices, banker's
  rounding in some accounting) and implement it in one place.
- Allocation (split $100 three ways) must distribute the remainder cent explicitly
  so parts sum to the whole.
- Do arithmetic in the database with NUMERIC, or in the app with a decimal type
  (Java BigDecimal, Python Decimal, .NET decimal); JSON numbers in JS are doubles:
  send money as strings or integer minor units.

## Verify
`SELECT sum(amount) FROM ledger` equals the sum computed by the app's decimal type;
a test inserting 0.1 + 0.2 stores exactly 0.3000; schema review finds no float money columns:
```sql
SELECT table_name, column_name, data_type FROM information_schema.columns
WHERE data_type IN ('real','double precision','float') AND column_name ~* '(amount|price|cost|total)'
  AND table_schema NOT IN ('pg_catalog', 'information_schema');   -- without this filter PostgreSQL 16.4 also returns system columns such as pg_proc.procost
```
