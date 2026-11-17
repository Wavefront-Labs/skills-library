---
id: computing-software.database-administration.sql-server.policy-based-management
name: policy-based-management
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, policy-based-management, pbm, facets, conditions, compliance]
level: practitioner
status: docs-checked
description: "Enforce and audit SQL Server configuration with Policy-Based Management: facets, conditions, policies, evaluation modes, and PowerShell evaluation."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/policy-based-management/administer-servers-by-using-policy-based-management
  - https://learn.microsoft.com/en-us/powershell/module/sqlserver/invoke-policyevaluation
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Policy-Based Management (PBM)

## Pieces
- **Facet**: a set of logical properties that model the behaviour of a type of managed target (instance, database, table, index...). Only the maker of a facet can add or remove its properties; some properties apply only to specific versions.
- **Condition**: a Boolean expression that specifies the allowed states of a target with regard to a facet.
- **Policy**: one condition plus the expected behaviour: evaluation mode, target filters and schedule. A policy contains only one condition, can be enabled or disabled, and is stored in `msdb`.
- **Policy category**: a user-defined grouping; a policy belongs to one category. Databases implicitly subscribe to the default category, and only policies from subscribed categories govern a database.
- System objects are excluded from the object set by default; add them explicitly to evaluate them.

## Evaluation modes
| Mode | Behaviour |
|---|---|
| On demand | evaluated when you specify it |
| On schedule | a SQL Server Agent job evaluates periodically |
| On change: log only | event notification evaluates the policy when a relevant change is made |
| On change: prevent | DDL triggers detect and roll back non-compliant DDL |

On schedule supports all policies; not every policy with an arbitrary object set is supported for on-change modes (performance). With no automated policy enabled, PBM does not affect system performance.

## Workflow
Use SQL Server Management Studio to pick a facet, define a condition, define a policy (condition, target filters, evaluation mode) and check compliance. A failed policy shows a critical health warning (red icon) in Object Explorer.

## Evaluate from PowerShell
`Invoke-PolicyEvaluation` (SqlServer module) evaluates policies against a target set. In check mode it reports compliance without changing anything; in configure mode it reconfigures non-compliant objects. `-OutputXml` writes the result in SML-IF format.
```powershell
Get-ChildItem "SQLSERVER:\SQLPolicy\<SERVER>\DEFAULT\Policies" |
  Invoke-PolicyEvaluation -TargetServer "<SERVER>" -OutputXml > <REPORT_DIR>\pbm.xml
```

## Gotchas
- On change: prevent depends on DDL triggers and the `nested triggers` server option; disabling nested triggers or removing the PBM triggers makes it fail or behave unexpectedly.
- A policy can break features: an "every table must have an index" policy enforced against `systranschemas` makes change data capture and transactional replication fail.

## Verify
Run the policy on demand and confirm the result matches the objects you expect to pass or fail.

## Checked
2026-11-09. Confirmed against the Learn pages "Administer Servers by Using Policy-Based Management" and "Invoke-PolicyEvaluation": components, terms, evaluation modes, nested-triggers warning, systranschemas warning, the PowerShell syntax and examples. Removed (not stated on the cited pages): the central management server evaluation steps (that Learn page returns 404), the msdb history query, example condition expressions, and the claim that on-change prevent applies only to naming-convention facets.
Method: documentation only; no commands were run.
