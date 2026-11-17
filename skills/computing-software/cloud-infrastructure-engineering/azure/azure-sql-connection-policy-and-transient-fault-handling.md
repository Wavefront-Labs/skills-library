---
id: computing-software.cloud-infrastructure-engineering.azure.azure-sql-connection-policy-and-transient-fault-handling
name: azure-sql-connection-policy-and-transient-fault-handling
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-sql, connection-policy, redirect-mode, transient-fault-handling, retry-logic]
level: advanced
status: docs-checked
description: "Choose Azure SQL connection policy (Redirect vs Proxy), open the right ports, and implement retry logic for transient errors like 40613, 40197 and 49918."
sources: ["https://learn.microsoft.com/azure/azure-sql/database/connectivity-architecture", "https://learn.microsoft.com/azure/azure-sql/database/troubleshoot-common-connectivity-issues", "https://learn.microsoft.com/sql/connect/ado-net/configurable-retry-logic-sqlclient-introduction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL connectivity: policy and retries

**Goal:** fast, reliable connections to Azure SQL Database / Managed Instance that survive failovers and reconfigurations.

## Connection policy
| Policy | Path | Ports | Use |
|---|---|---|---|
| **Redirect** | Gateway on 1433 hands the client the node address; data flows directly to the node | 1433 plus **11000-11999** outbound to the `Sql.<region>` service tag | Lower latency, higher throughput; default inside Azure |
| **Proxy** | All traffic through the gateway | 1433 only | Simple firewalls, on-prem clients without the port range |
| Default | Redirect for connections from inside Azure, Proxy from outside | | |
```bash
az sql server conn-policy update -g rg -s sql1 ...   # see `az sql server conn-policy update --help` for the connection-type option
```
Managed Instance: the public endpoint uses port 3342.

## Transient errors to retry
`40613` (database not currently available), `40197` (service error processing request, often reconfiguration), `40501` (service busy), `10928/10929` (resource limits), and connection timeouts during failover. The troubleshooting article lists the full set of transient error numbers.

## Retry pattern
- Retry the **whole unit of work** (open connection, run transaction), not just the failed command, because a failover kills the connection.
- Exponential backoff between attempts, with a total retry budget that covers the failover time you expect.
- .NET Microsoft.Data.SqlClient configurable retry:
```csharp
var opts = new SqlRetryLogicOption { NumberOfTries = 5, DeltaTime = TimeSpan.FromSeconds(2), MaxTimeInterval = TimeSpan.FromSeconds(30) };
conn.RetryLogicProvider = SqlConfigurableRetryFactory.CreateExponentialRetryProvider(opts);
```
- Connection string: `ConnectRetryCount` and `ConnectRetryInterval` control idle connection resiliency.

## Gotchas
- Retrying non-idempotent writes can duplicate data; make writes idempotent or check-before-retry.
- SNAT exhaustion on App Service with many short connections looks like timeouts: use connection pooling and Redirect.
- Long DNS caching after failover group failover: use the listener and keep TTL respected.

## Verify
- [ ] `SELECT session_id, net_transport, client_net_address FROM sys.dm_exec_connections WHERE session_id=@@SPID` from the app.
- [ ] A planned failover test causes only retried, logged blips.

## Checked
2026-10-27. Confirmed on Microsoft Learn: connectivity-architecture (Redirect default for connections from inside Azure, Proxy, ports 1433 and 11000-11999, `Sql.<region>` service tag),
troubleshoot-common-connectivity-issues (error numbers 40613, 40197, 40501, 10928, 10929; exponential backoff; ConnectRetryCount and ConnectRetryInterval),
configurable-retry-logic-sqlclient-introduction (SqlRetryLogicOption NumberOfTries, DeltaTime, MaxTimeInterval; CreateExponentialRetryProvider; RetryLogicProvider), MI public endpoint port 3342.
Removed: error numbers 49918-49920 and 4221, numeric backoff and failover-time figures, EF Core snippet, Connect Timeout and retry values, the private-endpoint and MI redirect statements,
`az sql db failover` (not on the CLI reference), and the `--connection-type` value (flag table not readable on the stripped CLI page).

Method: documentation only; no commands were run.
