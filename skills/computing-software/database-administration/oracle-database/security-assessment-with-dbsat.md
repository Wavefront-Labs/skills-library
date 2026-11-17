---
id: computing-software.database-administration.oracle-database.security-assessment-with-dbsat
name: security-assessment-with-dbsat
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, dbsat, security-assessment, cis-benchmark, stig, sensitive-data-discovery, oracle-security]
level: practitioner
status: draft
description: "Run Oracle DBSAT collect, report and discover to assess database security configuration and find sensitive data, then prioritise and track findings."
sources:
  - https://docs.oracle.com/en/database/oracle/security-assessment-tool/
  - https://www.oracle.com/database/technologies/security/dbsat.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security assessment with DBSAT

Database Security Assessment Tool: free from Oracle Support (Doc ID 2138254.1). Three parts:
**collector** (SQL + OS commands), **reporter** (analyses the collection, maps findings to CIS,
DISA STIG, GDPR and Oracle best practice), **discoverer** (finds sensitive columns by name/comment patterns).

## Collect
Run on the database server as the Oracle software owner (OS checks need it), with a user holding
the privileges listed in the docs (`CREATE SESSION`, `SELECT_CATALOG_ROLE`, `AUDIT_VIEWER`,
`CAPTURE_ADMIN`, `SELECT` on `SYS.REGISTRY$HISTORY`, `DV_SECANALYST` if Database Vault, etc.).
```bash
unzip dbsat.zip -d <DBSAT_DIR> && cd <DBSAT_DIR>
./dbsat collect -n dbsat_admin@//dbhost:1521/pdb1 pdb1_collect
# prompts for password and a zip encryption password (or -n for no encryption, avoid)
```
Run per PDB and for the CDB root. Output: `pdb1_collect.zip` (encrypted JSON).

## Report
Can run on any machine with Python and Java:
```bash
./dbsat report pdb1_collect
./dbsat report -a -g pdb1_collect     # -a include all checks, -g GDPR mapping
```
Produces HTML, Excel, JSON and text. Findings have risk levels: High, Medium, Low, Advisory,
Evaluate (needs human judgement), Pass. Typical highs: default passwords (`DBA_USERS_WITH_DEFPWD`),
users with powerful roles, `PUBLIC` execute on risky packages (`UTL_FILE`, `UTL_HTTP`),
`remote_os_authent`, no unified audit policies, unencrypted network, missing patches.

## Discover sensitive data
```bash
cp Discover/conf/sample_dbsat.config Discover/conf/pdb1.config
# set DB_HOSTNAME, DB_PORT, DB_SERVICE_NAME, schema scope, and pattern files to use
./dbsat discover -c Discover/conf/pdb1.config pdb1_discover
```
Reports columns matching patterns (names, emails, card numbers, national IDs) and counts rows:
input for redaction, TDE, masking and classification.

## Work the findings
1. Triage Highs first; record accepted risks with justification.
2. Script fixes (lock default accounts, revoke `PUBLIC` grants after impact testing, enable audit policies).
3. Re-run DBSAT and diff: `./dbsat diff` (newer releases) or compare JSON.
4. Schedule quarterly runs; keep reports encrypted (they map the attack surface).

## Gotchas
- Collector needs OS access for file permissions and listener checks; without it some checks are skipped ("Evaluate").
- Revoking `PUBLIC` execute on packages can break Oracle components; follow Oracle's guidance per package.

## Verify
Report shows no unaccepted High findings and the discover report is reviewed with data owners.
