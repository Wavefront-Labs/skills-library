---
id: computing-software.database-administration.oracle-database.incident-packaging-with-ips
name: incident-packaging-with-ips
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, incident-packaging, adrci, ips, ora-00600, ora-07445, tfa, oracle-support]
level: practitioner
status: docs-checked
description: "Package Oracle critical errors (ORA-00600, ORA-07445) for Oracle Support with ADRCI IPS or TFA diagcollect, including correlated traces, and upload the zip to the SR."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/diagnosing-and-resolving-problems.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-adr-command-interpreter-adrci.html
  - https://docs.oracle.com/en/engineered-systems/health-diagnostics/autonomous-health-framework/ahfug/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incident packaging with IPS

ADR groups each critical error into a **problem** (by error key, e.g. `ORA 600 [kcbz_check_objd]`)
and **incidents** (each occurrence, with its own trace dump). Oracle Support wants the incident
package, not a lone trace file.

## Find the incident
```bash
adrci
adrci> show homes
adrci> set home diag/rdbms/orcl/ORCL
adrci> show problem
adrci> show incident -mode brief -p "problem_key='ORA 600 [kcbz_check_objd]'"
adrci> show incident -mode detail -p "incident_id=24577"
```

## Package
Quick path (one command, creates the zip with correlated files):
```bash
adrci> ips pack incident 24577 in /tmp
# or by problem
adrci> ips pack problem 3 in /tmp
```
Step-by-step when you need to add files (e.g. application logs, OS logs):
```bash
adrci> ips create package incident 24577 correlate all
adrci> ips add file /var/log/messages package 1
adrci> ips generate package 1 in /tmp
```
`correlate basic|typical|all` controls how many related incidents/traces from around the same time are included.

## Before uploading
- Check the zip for sensitive data (trace dumps can contain row data and bind values).
- Upload to the SR in My Oracle Support; note the incident ID and the first-failure time in the SR.
- Search MOS with the error's first arguments (`ORA-600 [kcbz_check_objd]`) for known bugs first.

## Housekeeping
Incidents fill the ADR: `adrci> purge -age 43200 -type incident` (minutes) or set `SHORTP_POLICY` / `LONGP_POLICY` in hours.

## Verify
The zip contains the incident trace, alert log extract and correlated traces; the SR has the package attached.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: ips pack incident, ips create package ... correlate basic|typical|all, ips generate package <n> in <path>, purge -age <minutes> -type incident, SHORTP_POLICY / LONGP_POLICY (Database Utilities, ADRCI).

Removed or corrected: v$diag_problem/v$diag_incident remark, ips pack time, incremental generation, the whole TFA/AHF section and tfactl masking options (not in the cited pages).

Method: documentation only; no commands were run.
