---
id: computing-software.database-administration.yugabytedb.replace-failed-master
name: replace-failed-master
category: computing-software
field: database-administration
product: yugabytedb
tags: [yb-master, change-master-config, master-quorum, replace-master, list-all-masters, standby-master]
level: practitioner
status: docs-checked
description: "Replace a failed YB-Master by starting a standby with an empty master_addresses, adding it with change_master_config, then removing the dead master."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/troubleshoot/cluster/replace_master.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/troubleshoot/cluster/recover_server.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Replace a failed master

Scenario: masters M1, M2 and M3, with M1 failed and M4 as the replacement. Master RPC port is 7100.

1. Start M4 in standby mode, which means it does not join any quorum yet:
```
./bin/yb-master --master_addresses="" --fs_data_dirs=<data_dirs> [other usual flags]
```
2. Add it to the existing quorum:
```
yb-admin --master_addresses M1:7100,M2:7100,M3:7100 change_master_config ADD_SERVER M4 7100
```
3. Remove the failed one. List all masters including M4 so yb-admin can find the leader if M4 wins an election:
```
yb-admin --master_addresses M1:7100,M2:7100,M3:7100,M4:7100 change_master_config REMOVE_SERVER M1 7100
```
4. Verify:
```
yb-admin --master_addresses M2:7100,M3:7100,M4:7100 list_all_masters
```

If the old master is already dead (VM terminated), do the REMOVE step first and ADD afterward.

Tservers learn of the new master in memory after ADD_SERVER and need no restart. By default (until issue 1542 is implemented) a tserver only knows the masters in its startup `--tserver_master_addrs`; as long as one of those is still in the active quorum it can propagate the new quorum by heartbeat, but if none are, the tserver cannot join the cluster. Update `--tserver_master_addrs` (and the config file) on every tserver to the new set, here `M2:7100,M3:7100,M4:7100`, so a future restart works.

## Checked

2026-11-04. Confirmed against the Replace a failed YB-Master page and the Recover failed YB-TServer and YB-Master page (both read from raw GitHub because the originally cited URLs used wrong paths and returned 404): standby start with empty master_addresses, ADD_SERVER then REMOVE_SERVER, listing M4 so yb-admin can find the leader, list_all_masters, REMOVE-first order for an already-dead master, and the tserver --tserver_master_addrs behaviour. Removed 'change masters one at a time and run list_all_masters between changes', which the pages do not say. Source URLs corrected to replace_master.md and recover_server.md.

Method: documentation only; no commands were run.
