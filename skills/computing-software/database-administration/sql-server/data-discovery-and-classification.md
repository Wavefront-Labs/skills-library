---
id: computing-software.database-administration.sql-server.data-discovery-and-classification
name: data-discovery-and-classification
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, data-classification, sensitivity-labels, add-sensitivity-classification, gdpr, compliance, auditing]
level: practitioner
status: docs-checked
description: "Find and label sensitive columns in SQL Server and Azure SQL with ADD SENSITIVITY CLASSIFICATION, report on them, and surface label access in audit logs."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/sql-data-discovery-and-classification
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/add-sensitivity-classification-transact-sql
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/data-discovery-and-classification-overview
  - https://learn.microsoft.com/en-us/powershell/module/sqlserver/get-sqlsensitivityclassification
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data discovery and classification

## Discover
- SSMS: database -> Tasks -> Data Discovery and Classification -> Classify Data. It scans column
  names (not data) against built-in patterns (name, email, credit card, national ID) and suggests labels.
- Azure SQL and Managed Instance have their own Data Discovery & Classification experience (see the Azure SQL overview). In SSMS the recommendation engine is disabled while the Microsoft Purview Information Protection policy mode is used.
- Name-based discovery misses columns like `col7` or `notes`; sample data for free-text columns yourself.

## Label (SQL Server 2019+, Azure SQL)
```sql
ADD SENSITIVITY CLASSIFICATION TO
    dbo.Customer.Email, dbo.Customer.Phone
WITH (LABEL = 'Confidential', INFORMATION_TYPE = 'Contact Info', RANK = MEDIUM);

ADD SENSITIVITY CLASSIFICATION TO dbo.Customer.NationalId
WITH (LABEL = 'Highly Confidential - GDPR', INFORMATION_TYPE = 'National ID', RANK = CRITICAL);

DROP SENSITIVITY CLASSIFICATION FROM dbo.Customer.Phone;
```
Use the label/information-type GUIDs from your Microsoft Purview policy (`LABEL_ID`, `INFORMATION_TYPE_ID`)
so labels match across tools. Before SQL Server 2019 the classification lives in the extended properties `sys_information_type_name` and `sys_sensitivity_label_name`; `sys.sensitivity_classifications` exists from 2019. Viewing needs `VIEW ANY SENSITIVITY CLASSIFICATION`; managing needs `ALTER ANY SENSITIVITY CLASSIFICATION` (implied by database ALTER or CONTROL SERVER).

## Report
```sql
SELECT SCHEMA_NAME(o.schema_id) AS sch, o.name AS tbl, c.name AS col,
       sc.label, sc.information_type, sc.rank_desc
FROM sys.sensitivity_classifications sc
JOIN sys.objects o ON o.object_id = sc.major_id
JOIN sys.columns c ON c.object_id = sc.major_id AND c.column_id = sc.minor_id
ORDER BY sc.rank DESC, sch, tbl;
```
SSMS can generate, print and export a classification report (Tasks > Data Discovery and Classification > Generate Report). The SqlServer PowerShell module has `Get-SqlSensitivityClassification` for scripted inventories.

## Audit access to labelled data
SQL Server Audit and Azure SQL auditing record a `data_sensitivity_information` field for
statements that return classified columns:
```sql
SELECT event_time, server_principal_name, statement, data_sensitivity_information
FROM sys.fn_get_audit_file('<AUDIT_DIR>/*.sqlaudit', DEFAULT, DEFAULT)
WHERE data_sensitivity_information IS NOT NULL;
```

## Gotchas
- Labels are metadata only: they do not encrypt or mask. Pair with DDM, Always Encrypted, RLS.
- Labels move with the database (backups, bacpac); new columns are unlabelled until someone re-scans.
- Keep the classification script in source control and run it in the deployment pipeline.

## Verify
The report query lists every column flagged in the data inventory; a test query on a labelled
column produces an audit record with sensitivity info.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: SQL Data Discovery & Classification page and ADD SENSITIVITY CLASSIFICATION reference for SQL Server 2025 (SSMS discovery scans column names only, recommendations disabled in Purview policy mode, T-SQL classification and sys.sensitivity_classifications from SQL Server 2019 with columns information_type, label, rank, rank_desc, extended properties before 2019, permissions, LABEL/LABEL_ID/INFORMATION_TYPE/INFORMATION_TYPE_ID/RANK with NONE to CRITICAL, SSMS report export, Get-SqlSensitivityClassification), SQL Server 2019 What's New (data_sensitivity_information in the audit record). Removed as unconfirmed: the claim that SSMS migrates old extended-property labels, the Defender for Cloud recommendation statement and the dbatools inventory command.
Method: documentation only; no commands were run.
