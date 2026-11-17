---
id: computing-software.database-administration.sql-server.availability-groups-on-linux-with-pacemaker
name: availability-groups-on-linux-with-pacemaker
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, pacemaker-ag, read-scale-availability-group, sql-server-linux, cluster-type-external, cluster-type-none, pcs, mssql-server-ha]
level: sme
status: docs-checked
description: "Build SQL Server availability groups on Linux under Pacemaker (CLUSTER_TYPE EXTERNAL), and clusterless read-scale AGs (CLUSTER_TYPE NONE) with manual failover."
sources:
  - https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-availability-group-cluster-rhel
  - https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-availability-group-configure-rs
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/read-scale-availability-groups
  - https://learn.microsoft.com/en-us/sql/linux/business-continuity/availability-groups/cluster-pacemaker
  - https://learn.microsoft.com/en-us/sql/linux/business-continuity/availability-groups/failover-high-availability
  - https://learn.microsoft.com/en-us/sql/linux/business-continuity/availability-groups/configure
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/perform-a-planned-manual-failover-of-an-availability-group-sql-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Availability groups on Linux with Pacemaker, and read-scale AGs

## Common prep on every node
```bash
sudo /opt/mssql/bin/mssql-conf set hadr.hadrenabled 1 && sudo systemctl restart mssql-server
```
Endpoints authenticate with **certificates** (no Windows domain): create a master key and
certificate on each node, exchange `.cer`/`.pvk` files, `CREATE ENDPOINT hadr_endpoint ... AUTHENTICATION = CERTIFICATE dbm_cert`.

## Pacemaker-managed AG (RHEL example)
```sql
CREATE AVAILABILITY GROUP [ag1] WITH (CLUSTER_TYPE = EXTERNAL)
FOR REPLICA ON
 N'node1' WITH (ENDPOINT_URL = N'tcp://node1:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT, FAILOVER_MODE = EXTERNAL, SEEDING_MODE = AUTOMATIC),
 N'node2' WITH (ENDPOINT_URL = N'tcp://node2:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT, FAILOVER_MODE = EXTERNAL, SEEDING_MODE = AUTOMATIC),
 N'node3' WITH (ENDPOINT_URL = N'tcp://node3:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT, FAILOVER_MODE = EXTERNAL, SEEDING_MODE = AUTOMATIC);
ALTER AVAILABILITY GROUP [ag1] GRANT CREATE ANY DATABASE;
-- pacemaker login on every node
CREATE LOGIN pacemakerLogin WITH PASSWORD = '<SECRET>';
GRANT ALTER, CONTROL, VIEW DEFINITION ON AVAILABILITY GROUP::ag1 TO pacemakerLogin;
GRANT VIEW SERVER STATE TO pacemakerLogin;
```
Credentials file on each node: `/var/opt/mssql/secrets/passwd` (login on line 1, password line 2, mode 400).
```bash
sudo yum install -y pacemaker pcs fence-agents-all resource-agents   # set a password for the hacluster user and start pcsd first (see the cluster article)
sudo yum install -y mssql-server-ha
sudo pcs cluster setup sqlcluster node1 node2 node3 && sudo pcs cluster start --all
sudo pcs property set stonith-enabled=true          # configure a real fencing agent
sudo pcs resource create ag_cluster ocf:mssql:ag ag_name=ag1 meta failure-timeout=60s promotable notify=true
sudo pcs resource create virtualip ocf:heartbeat:IPaddr2 ip=10.1.0.70
sudo pcs constraint colocation add virtualip with promoted ag_cluster-clone INFINITY with-rsc-role=Promoted
sudo pcs constraint order promote ag_cluster-clone then start virtualip
```
Automatic failover needs at least three replicas: three synchronous, or two synchronous plus a configuration-only
replica (`AVAILABILITY_MODE = CONFIGURATION_ONLY`; any edition can host it, and on Express the endpoint `ROLE` must be `WITNESS`).
The Pacemaker resource agent sets `REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT` itself.
Manual failover is done through Pacemaker, not T-SQL (with `CLUSTER_TYPE = EXTERNAL`, `FAILOVER_MODE` must be `EXTERNAL`), and the target must be synchronous:
`sudo pcs resource move ag_cluster-clone --master node2 && sleep 30 && sudo pcs resource clear ag_cluster-clone`
(the move leaves a location constraint; `--lifetime=30S` makes it temporary). SQL Server 2025 CU3+ also offers a preview v2 agent (`ocf:mssql:agv2`); v1 stays the supported production agent.
Production requires fencing (STONITH); the tutorial's `stonith-enabled=false` is for testing only. Known issue in the docs: with the AG as a cluster resource, forced failover with data loss to an asynchronous replica does not work.

## Read-scale AG (CLUSTER_TYPE = NONE)
No cluster manager, no automatic failover, not high availability: for offloading reads and manual DR; SQL Server 2017+ on Windows and Linux.
```sql
CREATE AVAILABILITY GROUP [rs_ag] WITH (CLUSTER_TYPE = NONE)
FOR REPLICA ON
 N'node1' WITH (ENDPOINT_URL = N'tcp://node1:5022', AVAILABILITY_MODE = ASYNCHRONOUS_COMMIT, FAILOVER_MODE = MANUAL, SEEDING_MODE = AUTOMATIC,
                SECONDARY_ROLE (ALLOW_CONNECTIONS = ALL)),
 N'node2' WITH (ENDPOINT_URL = N'tcp://node2:5022', AVAILABILITY_MODE = ASYNCHRONOUS_COMMIT, FAILOVER_MODE = MANUAL, SEEDING_MODE = AUTOMATIC,
                SECONDARY_ROLE (ALLOW_CONNECTIONS = ALL));
```
Manual failover without data loss (documented procedure): make the primary and target `SYNCHRONOUS_COMMIT` and wait for SYNCHRONIZED; set `REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT = 1`; run `ALTER AVAILABILITY GROUP rs_ag OFFLINE` on the primary and any secondaries not taking part; run `ALTER AVAILABILITY GROUP rs_ag FORCE_FAILOVER_ALLOW_DATA_LOSS` on the target; run `ALTER AVAILABILITY GROUP rs_ag SET (ROLE = SECONDARY)` on the old primary; then `ALTER DATABASE <db> SET HADR RESUME` per database on the new primary and re-create any listener.

## Verify
`sudo pcs status` shows one Promoted replica and the VIP with it; `sys.dm_hadr_database_replica_states` healthy on all nodes; a `pcs resource move` drill succeeds.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: Linux Pacemaker, AG-configure and failover articles for SQL Server 2025 (mssql-conf set hadr.hadrenabled 1, certificate-authenticated mirroring endpoints, CLUSTER_TYPE = EXTERNAL with FAILOVER_MODE = EXTERNAL, GRANT CREATE ANY DATABASE, pacemaker login grants ALTER/CONTROL/VIEW DEFINITION on the AG plus VIEW SERVER STATE, credentials file /var/opt/mssql/secrets/passwd mode 400, pcs resource create ocf:mssql:ag with failure-timeout and promotable notify, IPaddr2 resource, colocation and ordering constraints, stonith guidance, three-replica minimum, configuration-only replica, resource move and clear, known forced-failover issue), planned-failover page (read-scale CLUSTER_TYPE = NONE manual failover steps), read-scale page (SQL Server 2017+, no HA). Wrong in the draft: the read-scale role switch order (it omitted OFFLINE and put SET ROLE before the forced failover), `--promoted` is not the documented move syntax (the docs use `--master`), the replica count rule was tied to REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT which the agent sets itself, and dnf was used where the docs use yum.
Method: documentation only; no commands were run.
