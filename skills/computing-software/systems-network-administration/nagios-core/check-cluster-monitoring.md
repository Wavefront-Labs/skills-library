---
id: computing-software.systems-network-administration.nagios-core.check-cluster-monitoring
name: check-cluster-monitoring
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, clusters, check-cluster, service-cluster, host-cluster, servicestateid, hoststateid, redundant-services]
level: advanced
status: docs-checked
description: "Monitor redundant services or HA host groups in Nagios Core with check_cluster fed by on-demand state ID macros, with notifications disabled on members."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/clusters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster monitoring with check_cluster

- **Service cluster:** redundant services (five DNS servers). **Host cluster:** HA hosts where one takes over.
- Monitor each member individually with notifications DISABLED (still visible in the status CGI), then monitor the cluster as a whole with notifications ENABLED.
- `check_cluster` reads cached member states, it does not recheck them. It ships with the Nagios Plugins project.

## Commands
```
check_cluster --service -l $ARG1$ -w $ARG2$ -c $ARG3$ -d $ARG4$
check_cluster --host    -l $ARG1$ -w $ARG2$ -c $ARG3$ -d $ARG4$
```
`-l` label, `-w`/`-c` thresholds, `-d` comma-separated state IDs (check the plugin's `--help` for exact semantics).

## Service cluster example
```
check_service_cluster!"DNS Cluster"!0!1!$SERVICESTATEID:host1:DNS Service$,$SERVICESTATEID:host2:DNS Service$,$SERVICESTATEID:host3:DNS Service$
```
One non-OK member = WARNING, two or more = CRITICAL, all OK = OK.

## Host cluster example
```
check_host_cluster!"Super Host Cluster"!0!1!$HOSTSTATEID:host1$,$HOSTSTATEID:host2$,$HOSTSTATEID:host3$
```
Attach this service to the Nagios host, not a cluster member.

Macro syntax: `computing-software.systems-network-administration.nagios-core.on-demand-macros`.

## Checked

2026-11-04. Confirmed on the Clusters page: service cluster and host cluster definitions, monitor each element with notifications disabled and the cluster with notifications enabled, check_cluster reads cached states from the status file and is in the Nagios Plugins project, both command definitions, both example check_command lines with on-demand state ID macros, WARNING for one non-OK and CRITICAL for two or more, and attaching the host cluster service to the Nagios host. Nothing removed.

Method: documentation only; no commands were run.
