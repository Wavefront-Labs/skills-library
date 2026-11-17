---
id: computing-software.systems-network-administration.apache-guacamole.batch-import
name: batch-import
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, batch-import, import-connections, csv, json, yaml, bulk-connections, reset-permissions]
level: practitioner
status: docs-checked
description: "Bulk-create Guacamole connections and groups from CSV, JSON or YAML: required fields, group paths, users, parameters and errors."
sources:
  - https://guacamole.apache.org/doc/gug/batch-import.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch import of connections

Admin only; the auth module must support dynamic connection/group creation. Use **Import** on the connections tab and upload the file.

Fields: required `name`, `protocol`; optional `group` (path like `ROOT/Parent/Child`) or `parentIdentifier`, `users`, `groups`, parameters (`hostname`, `username`, ...), attributes (e.g. `guacd-encryption`).

CSV: header row names fields; one connection per row; append ` (attribute)` or ` (parameter)` to a column to disambiguate; multiple users separated by `;` (escape with a backslash).
```csv
name,protocol,username,password,hostname,group,users,groups,guacd-encryption (attribute)
conn1,vnc,alice,<PASSWORD>,conn1.example.com,ROOT,user1;user2,Team A,none
```
JSON (YAML is the same structure):
```json
[{"name":"conn1","protocol":"vnc",
  "parameters":{"username":"alice","password":"<PASSWORD>","hostname":"conn1.example.com"},
  "group":"ROOT","users":["user1"],"groups":["Team A"],
  "attributes":{"guacd-encryption":"none"}}]
```
Behaviour:
- Missing users and groups are created.
- Updating an existing connection keeps its permissions unless **Reset permissions** is checked.
- Result: count imported; per-connection errors listed; unparseable file gives a format error.

Verify: the UI reports the expected count and the new connections appear in the right groups.

## Checked

2026-11-08. Read the whole of the batch import page (batch-import.html) and confirmed the Import button, required name and protocol, group path versus parentIdentifier, semicolon-separated users with backslash escape, the attribute and parameter column suffixes, JSON and YAML structure, automatic creation of missing users and groups, Reset permissions, and success and failure reporting. Nothing removed.
Method: documentation only; no commands were run.
