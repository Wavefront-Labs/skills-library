---
id: computing-software.database-administration.sql-server.azure-sql-connection-policy-and-connectivity-troubleshooting
name: azure-sql-connection-policy-and-connectivity-troubleshooting
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql, connection-policy-redirect, connection-policy-proxy, transient-faults, retry-logic, connectivity, error-40613]
level: practitioner
status: docs-checked
description: "Choose Azure SQL connection policy (Redirect vs Proxy), open the right ports, add transient-fault retry logic, and diagnose common connection errors."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/connectivity-architecture
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/troubleshoot-common-errors-issues
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/troubleshoot-common-connectivity-issues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL connection policy and connectivity troubleshooting

## Policies
| Policy | Path | Ports |
|---|---|---|
| Redirect | gateway (1433) hands the client the node's address; later traffic goes direct | 1433 + 11000-11999 to the region's SQL ranges |
| Proxy | all traffic through the gateway | 1433 only |
| Default | Redirect from inside Azure, Proxy from outside | |
Redirect is recommended for the lowest latency and highest throughput. Set explicitly:
```bash
az sql server conn-policy update -g <rg> -s <server> --connection-type Redirect
```
Existing private endpoints on the Default policy use Proxy over port 1433; Redirect with private
link needs a wider port range, see the private-link page.

## Transient faults
Reconfigurations (scaling, patching, failover) drop connections for seconds. Every client needs retry:
- `ConnectRetryCount` (default 1, range 0-255) and `ConnectRetryInterval` (default 10 s, range 1-60) cover connection open.
- Command-level retries for transient errors 40613, 40197, 40501 and 10928 with exponential backoff.
- Idempotent writes or transaction re-run, never blind replay of half-done work.
Maintenance windows reduce the timing surprise but not the need for retries.

## Error table
| Error | Meaning |
|---|---|
| 40615 | client IP not allowed by firewall (message shows the IP seen) |
| 18456 | login failed; check the database name (contained users need `Initial Catalog`) |
| 40613 | database not currently available (reconfiguration) - retry |
| 10928 | request limit for the service objective reached |
| 40544 | database reached max size |
| 40501 | service busy (throttled) - back off |
| Timeout at connect from on-premises | outbound 1433 blocked, or Redirect ports blocked |

## Diagnose
```bash
nslookup <server>.database.windows.net          # public gateway or private endpoint IP?
Test-NetConnection <server>.database.windows.net -Port 1433
```
Inside the database: `SELECT * FROM sys.event_log` (in master, SQL Database) for connectivity events
(filter `event_category = 'connectivity'`).

## Gotchas
- TLS 1.2 is the lowest minimal TLS version Azure SQL Database supports (server minimal TLS version setting).

## Verify
Application survives a planned failover with only retried errors in its logs.

## Checked
2026-10-28. Confirmed against the connectivity-architecture, private-link and transient-fault pages: Redirect default inside Azure and Proxy default from outside, Redirect ports 11000-11999, Redirect recommended for lowest latency and highest throughput, existing private endpoints on the Default policy use Proxy over 1433, ConnectRetryCount (default 1) and ConnectRetryInterval (default 10 s), errors 40613, 40197, 40501, 10928, 40544, 40615, sys.event_log, minimal TLS version 1.2. The az command passed check_commands.
Removed unconfirmed claims: private endpoints behaving like Redirect (the page says the opposite for existing endpoints), the Managed Instance port sentence, error codes 49918-49920, 4221, 10929 and 18456 states 132-133, 47073 meaning, dm_exec_connections columns, Resource Health, proxy idle-timeout and long-running connection gotchas.
Method: documentation only; no commands were run.
