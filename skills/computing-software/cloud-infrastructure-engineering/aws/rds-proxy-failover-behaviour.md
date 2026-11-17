---
id: computing-software.cloud-infrastructure-engineering.aws.rds-proxy-failover-behaviour
name: rds-proxy-failover-behaviour
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds-proxy, proxy-failover, aurora-failover, multi-az, connection-resilience]
level: advanced
status: docs-checked
description: "Understand and test how RDS Proxy handles Aurora and Multi-AZ failovers: preserved idle connections, dropped transactions, DNS bypass and client retry design."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.howitworks.html#rds-proxy-failover", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraHighAvailability.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failover through RDS Proxy

## 1. What the proxy changes
- Without a proxy, existing connections are disrupted and the application must reopen them; clients are exposed to
  DNS propagation delay, local DNS caching, connection timeouts and uncertainty about which instance is the writer.
- The proxy keeps accepting connections at the same IP address and directs them to the new primary, so clients
  are not subject to those DNS effects. While the writer is unavailable the proxy queues incoming requests.
- **Idle client connections stay open** across the failover (the User Guide: most connections stay alive).
- **Connections in the middle of a transaction or SQL statement are cancelled**; the application must retry them.
- The User Guide's failover section describes Multi-AZ RDS configurations; for Aurora, confirm behaviour on the
  Aurora User Guide RDS Proxy pages and by testing.

## 2. Client design
- Retry idempotent operations on connection errors with backoff and a bounded number of attempts.
- `ConnectionBorrowTimeout` (default 120 s, range 0 to 300) only applies when the proxy has opened its maximum
  connections and all are busy; keep it shorter than your API timeout so callers fail fast enough.
- Readers: use a proxy endpoint with `--target-role READ_ONLY` (values `READ_WRITE`, `READ_ONLY`; SQL Server
  proxies support only `READ_WRITE`).

## 3. Test it
```bash
# loop writes through the proxy in one terminal
while true; do psql "host=<PROXY_ENDPOINT> ..." -c "insert into heartbeat values (now())" || echo FAIL $(date +%T); sleep 0.5; done
# trigger failover in another
aws rds failover-db-cluster --db-cluster-identifier app --target-db-instance-identifier app-2
```
Measure the gap of FAIL lines; compare with a run against the cluster endpoint directly.
Multi-AZ DB instances: `aws rds reboot-db-instance --force-failover`.

## 4. Proxy availability
The default proxy endpoint is provisioned across only two Availability Zones chosen from the proxy's
configured subnets (any two if more are configured), so choose subnets in AZs where your clients run.

## Verify
- [ ] Failover test shows write gap within target and idle connections still usable afterwards.

## Checked
Date: 2026-10-27. Sources: RDS User Guide rds-proxy.howitworks (Failover section) and rds-proxy (endpoint AZ
placement); botocore `rds` model (`ConnectionBorrowTimeout` default 120, range 0 to 300 and when it applies;
`TargetRole` values; `ForceFailover`, `failover-db-cluster` operations present). Removed the unconfirmed DNS delay
figures, retry counts and pinned-session claim. The dead Aurora fault injection source URL was replaced with the Aurora high availability page.
Method: documentation only; no commands were run.
