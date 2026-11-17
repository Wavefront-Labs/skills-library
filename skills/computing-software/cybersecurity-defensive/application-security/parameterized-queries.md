---
id: computing-software.cybersecurity-defensive.application-security.parameterized-queries
name: parameterized-queries
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [input-validation, parameterized-queries, sql-injection, prepared-statements, orm-raw-queries, injection]
level: practitioner
status: docs-checked
description: "Eliminate SQL injection with parameterised queries, bind-variable stored procedures, fixed mappings for identifiers and sort direction, and least-privilege database accounts."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html", "https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameterised queries

**Goal:** untrusted data is always sent to the database as bound values, never concatenated into SQL text.
Applies to data from requests, other services and previously stored data.

## Primary defence: prepared statements
Define the SQL structure separately and bind values through the database API. Concatenating untrusted values
before preparing defeats the protection. Examples from the OWASP Query Parameterization Cheat Sheet:
- Java: `connection.prepareStatement("SELECT account_balance FROM user_data WHERE user_name = ?")` then
  `setString(1, value)`.
- ASP.NET: `SqlCommand` with `@CustomerId` and `command.Parameters.Add(new SqlParameter(...))`.
- PHP PDO: `$dbh->prepare("... VALUES (:name, :value)")` then `bindParam`.
- Ruby, Perl DBI, Rust SQLx, Cold Fusion `cfqueryparam`, JPA/Hibernate named parameters are also shown there.
- Do the parameterisation server-side: client-side libraries often build strings and send raw queries.
- With ORMs, bind untrusted values rather than concatenating them into query strings; Hibernate queries can
  be vulnerable.

## Stored procedures
Not automatically safe. Binding the call's arguments does not protect dynamic SQL built inside the procedure:
use bind variables there (Oracle `EXECUTE IMMEDIATE ... USING`; SQL Server `sp_executesql` with a parameter
list).

## Things parameters cannot bind
Table names, column names and SQL keywords such as `ASC`/`DESC`. Keep them fixed in code, or map the user's
choice to a small set of application-owned tokens and reject unknown choices (map a sort direction to the
literal `ASC` or `DESC`). Continue binding all data values even when they passed validation.

## Escaping
Strongly discouraged as a substitute for binding: behaviour depends on SQL dialect and configuration (MySQL
`NO_BACKSLASH_ESCAPES` disables backslash escaping).

## Hardening
Least privilege limits damage but does not prevent injection: no DBA/admin rights for application accounts,
read-only accounts where only reads are needed, separate DB users per application, views to limit exposed
columns, and a restricted OS account for the DBMS.

## Verify
Review query construction in code and stored procedures: untrusted values are bound, identifiers and sort
directions come from a fixed mapping. Use the OWASP Web Security Testing Guide SQL injection tests.

## Checked
2026-11-01. Confirmed against the OWASP SQL Injection Prevention and Query Parameterization cheat sheets.
Removed: Python, Node and .NET SqlCommand-specific snippets not on those pages, `PDO::ATTR_EMULATE_PREPARES`,
Django/SQLAlchemy/Sequelize/EF raw-API list, LIKE and IN-list advice, Semgrep and CodeQL rule names, grep
patterns, charset-bypass and second-order claims, and the test payloads.
Method: documentation only; no commands were run.
