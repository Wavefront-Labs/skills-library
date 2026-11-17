---
id: computing-software.database-administration.yugabytedb.yb-ctl-local-development-clusters
name: yb-ctl-local-development-clusters
category: computing-software
field: database-administration
product: yugabytedb
tags: [yb-ctl, local-cluster, development, num-shards-per-tserver, placement-info, listen-ip, test-cluster]
level: intro
status: docs-checked
description: "Create and manage local multi-node YugabyteDB clusters for development with yb-ctl, including flags, node operations and the macOS port 7000 conflict."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-ctl.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# yb-ctl local development clusters

yb-ctl administers local clusters for development and learning, simulating a multi-node cluster on one host. For multi-host clusters use the Deploy instructions. It manages a cluster only if that cluster was created with yb-ctl. Run it from the YugabyteDB home directory as `./bin/yb-ctl [ command ] [ flags ]`.

Lifecycle commands: `create` (no flags gives a 1-node cluster), `start` (starts the existing cluster, or creates and starts one), `stop`, `destroy`, `status`, `restart` (all at once), `wipe_restart`.

Node commands: `add_node`, `remove_node`, `start_node`, `stop_node`, `restart_node` (each takes a node number except `add_node`). Each accepts an optional `--master` flag meaning the server is a yb-master. `stop_node` and `remove_node` currently behave identically.

Common flags:
- `--rf <n>` (also `--replication_factor`): replicas per tablet, default 1; use an odd number, and at least 3 for fault tolerance. It also sets the default number of masters. The initial `create` makes as many nodes as the replication factor.
- `--master_flags "key=value,key2=value2"` and `--tserver_flags "..."` pass flags to the processes, for example `--tserver_flags "ysql_enable_auth=true"`
- `--placement_info cloud.region.zone,...` (default `cloud1.datacenter1.rack1`)
- `--num_shards_per_tserver <n>` shards (tablets) per tserver for each table (default 2)
- `--listen_ip` applies to 1-node clusters only (default 127.0.0.1); `--listen_ip=0.0.0.0` gives external access to the database APIs and admin UIs
- `--data_dir` (default `$HOME/yugabyte-data/`) cannot be changed after creation

Example, a 3-node cluster with custom flags:
```
./bin/yb-ctl --rf 3 create --master_flags "log_cache_size_limit_mb=128,log_min_seconds_to_retain=20" --tserver_flags "log_segment_size_mb=128"
```

macOS Monterey enables AirPlay receiving by default, which listens on port 7000 and makes `yb-ctl start` fail. Start with `--master_flags "webserver_port=7001"`, or disable AirPlay receiving, start the cluster, then optionally re-enable it.

`restart` loses custom flags and placement information unless you pass them again as for `create`. `wipe_restart` stops all nodes, removes the data directories and restarts with the same node count, and also loses custom flags and placement. `destroy` removes the cluster.

## Checked

2026-11-09: purpose, restriction to yb-ctl-created clusters, commands, flags and defaults, the macOS port conflict and the restart/wipe_restart behaviour confirmed against the yb-ctl reference page (yugabyte-db docs admin/yb-ctl.md; the Overview, Commands, Flags, macOS and restart sections were read, remaining example sections searched). Removed the claim that production should use manual deployment, Kubernetes or yugabyted, and the automatic-splitting example flags, neither of which appears on the page.

Method: docs-checked 2026-11-09 against yugabyte-db docs admin/yb-ctl.md
