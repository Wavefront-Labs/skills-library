---
id: computing-software.database-administration.oracle-database.monitoring-data-guard-lag
name: monitoring-data-guard-lag
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, data-guard, apply-lag, dataguard-stats, transport-lag, dgmgrl, alerting]
level: practitioner
status: docs-checked
description: "Monitor Oracle Data Guard transport and apply lag with V$DATAGUARD_STATS and the broker, set lag thresholds, and interpret common lag causes."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-DATAGUARD_STATS.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dgbkr/oracle-data-guard-broker-properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring Data Guard lag

## Standby view
```sql
SELECT name, value, unit, time_computed, datum_time
FROM v$dataguard_stats
WHERE name IN ('transport lag', 'apply lag', 'apply finish time', 'estimated startup time');
```
- **transport lag**: redo generated on the primary but not yet received on the standby ->
  potential data loss (RPO) if the primary dies now.
- **apply lag**: redo received but not yet applied -> staleness of an Active Data Guard reader
  and part of failover time.
- **apply finish time**: estimated time to apply what is already received (adds to RTO).
- `datum_time` is when the standby last got data from the primary; if it stops advancing the
  lag values are stale (connection broken): alert on `SYSDATE - datum_time` too.

`V$DATAGUARD_STATS` returns no rows on a primary and has a `CON_ID` column (0 = whole CDB).

## Broker
```
DGMGRL> SHOW CONFIGURATION LAG;
DGMGRL> SHOW DATABASE 'stby' 'TransportLagThreshold';
DGMGRL> EDIT DATABASE 'stby' SET PROPERTY TransportLagThreshold = 300;   -- seconds; 0 = no warning
DGMGRL> EDIT DATABASE 'stby' SET PROPERTY ApplyLagThreshold = 900;
DGMGRL> VALIDATE DATABASE 'stby';
```
Exceeding a threshold generates a warning status for that member, which monitoring can pick up
from `SHOW CONFIGURATION`. Both property values are in seconds.

## Causes of lag
| Symptom | Likely cause |
|---|---|
| transport lag growing, apply lag small | network bandwidth/latency, ASYNC transport falling behind, primary redo bursts (batch loads, index rebuilds) |
| transport fine, apply lag growing | standby I/O slower than primary, apply serialized, heavy queries on ADG standby competing |
| apply lag jumps then stays | recovery stopped: check the apply process and the standby alert log |
| lag only during nights | RMAN backups or batch jobs on the standby/primary |
| `apply lag` equal to `DelayMins` | intentional delay configured (`DelayMins` is minutes of apply delay, default 0) |

## Alerting suggestions
- transport lag > RPO budget for 5 min (e.g. 60 s for ASYNC).
- apply lag > staleness budget for readers.
- `datum_time` older than 2 min.
- Broker configuration status not SUCCESS.

## Checked
2026-11-01. Confirmed against the 19c V$DATAGUARD_STATS reference (metric names, datum_time staleness, no rows on a primary) and the Data Guard broker properties page (TransportLagThreshold and ApplyLagThreshold in seconds, 0 disables the warning; DelayMins in minutes, default 0). Removed: ORA error numbers, V$MANAGED_STANDBY and V$DATAGUARD_PROCESS queries, v$dg_broker_config, RAC apply version gate, dead Data Guard concepts source.
Method: documentation only; no commands were run.

## Verify
Generate redo on the primary (`ALTER SYSTEM SWITCH LOGFILE` plus a test insert) and watch
transport/apply lag return to a few seconds; stop transport in a test (`DEFER` destination) to
see the alert fire.
