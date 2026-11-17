---
id: computing-software.database-administration.sql-server.implicit-conversions-and-non-sargable-predicates
name: implicit-conversions-and-non-sargable-predicates
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, execution-plan, implicit-conversion, data-type-precedence, nvarchar]
level: practitioner
status: docs-checked
description: "Understand SQL Server implicit conversions and data type precedence: which side of a comparison gets converted, and how to align types."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-type-precedence-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-type-conversion-database-engine
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Implicit conversions and data type precedence

## The rule
When an operator combines expressions of different types, the type with the **lower precedence** is converted to the type with the **higher precedence**; if the conversion is not a supported implicit one, an error is returned. For comparison operators and other expressions the result type follows these precedence rules. Relevant order (highest first): datetime2, datetime, date, time, float, decimal, bigint, int, smallint, tinyint, bit, uniqueidentifier, **nvarchar**, nchar, **varchar**, char, varbinary, binary.

## Consequences
- `nvarchar` outranks `varchar`, so comparing a `varchar` column to an `nvarchar` value converts the column side. Drivers that send strings as nvarchar by default therefore trigger the conversion on varchar columns. Whether the plan can still seek the index is something to confirm in the actual execution plan (look for a conversion warning); the cited pages do not discuss plans.
- `int` outranks `varchar`, so `@int + ' text'` tries to convert the text to int and fails with Msg 245 (conversion failed), whereas `@int + '1'` adds (returns the sum) rather than concatenates.
- Assignment is different: assigning a value to a variable or inserting into a column yields the type defined by the variable or column.
- Some conversions are not supported implicitly at all, for example nchar to binary needs an explicit conversion.

## Practice
- Make parameter types match column types in the application (check the driver's setting for how strings are sent), or align the schema so joined columns share a type.
- Use `CAST` for ISO-compliant code, or `CONVERT` when you need its style argument.
- Read the actual execution plan for conversion warnings on columns, and compare logical reads (`SET STATISTICS IO ON`) before and after a change.

## Verify
After aligning types, the plan shows no conversion on the column side and the query returns the same rows.

## Checked
2026-11-09. Read in full: "Data type precedence (Transact-SQL)" and "Data type conversion (Database Engine)". Confirmed the precedence order, the lower-to-higher conversion rule, the Msg 245 and sum examples, assignment typing, and the nchar-to-binary example. Removed (not on either page): sargability and index-seek claims, plan warning text, the plan-cache query, driver-specific settings, and the rewrite table for non-sargable predicates.
Method: documentation only; no commands were run.
