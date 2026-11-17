---
id: computing-software.database-administration.yugabytedb.manual-deployment-masters-and-tservers
name: manual-deployment-masters-and-tservers
category: computing-software
field: database-administration
product: yugabytedb
tags: [manual-deployment, yb-master, yb-tserver, flagfile, master-addresses, tserver-master-addrs, verify-deployment, ports]
level: practitioner
status: docs-checked
description: "Start masters and tservers by hand with the required flags, then verify the deployment: UI ports, log locations, and per-service bind addresses."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/manual-deployment/start-masters.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/manual-deployment/verify-deployment.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/default-ports.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manual deployment of masters and tservers

Start masters first, then tservers.

Start masters first; the number of master nodes must equal the replication factor and `--master_addresses` should list that many addresses. Run `./bin/post_install.sh` on each node first. Flags used in the page's yb-master example:
- `--master_addresses` (all master RPC endpoints, port 7100)
- `--rpc_bind_addresses`
- `--fs_data_dirs`
- `--placement_cloud`, `--placement_region`, `--placement_zone`

The number of tservers must equal or exceed the RF for tables to be created. Flags used in the page's yb-tserver example:
- `--tserver_master_addrs` (the same master list)
- `--rpc_bind_addresses`, `--fs_data_dirs` and the placement flags
- `--enable_ysql`
- `--pgsql_proxy_bind_address` (default 0.0.0.0:5433) and `--cql_proxy_bind_address` (default 0.0.0.0:9042)
- `--time_source=clockbound` is optional, for highly accurate clocks (needs system configuration)

Put the flags in a file (for example master.conf) and pass `--flagfile` instead of command line flags. The page suggests a cron entry to restart a process that goes down.

Verification:
- Master UI at port 7000 on any master; the Masters tab should list all masters with one LEADER, and `/tablet-servers` should show every tserver ALIVE.
- Tserver UI is on port 9000. Clients connect to YSQL on 5433 and YCQL on 9042 on any tserver node; the YCQL webserver is 12000 and YSQL's is 13000.
- Check the INFO logs `yb-data/master/logs/yb-master.INFO` and `yb-data/tserver/logs/yb-tserver.INFO`, which sit inside the first `--fs_data_dirs` directory (masters should show one Raft LEADER and followers; tservers should log registering with the master).

For multi-AZ deployments the default placement policy treats all nodes as equal regardless of the `--placement_*` flags, so also run `yb-admin modify_placement_info <cloud.region.zone,...> <RF>` and check `http://<any-master-ip>:7000/cluster-config`. In a single zone, use the same placement values on every node.

## Checked

2026-11-04. Confirmed against the manual deployment start-masters/start-tservers page (flags in the yb-master and yb-tserver examples, masters equal RF, tservers at least RF, flagfile, INFO log locations, modify_placement_info and cluster-config check, clockbound), the verify-deployment page (master UI, client ports 5433 and 9042, port table) and default-ports. Removed the `ysqlsh -h` and `ycqlsh` connection lines (not on these pages) and the claim that the placement flags are strictly required; the page uses them in its examples and says a multi-AZ policy must be set with modify_placement_info.

Method: documentation only; no commands were run.
