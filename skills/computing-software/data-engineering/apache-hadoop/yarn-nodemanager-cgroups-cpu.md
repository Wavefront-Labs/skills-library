---
id: computing-software.data-engineering.apache-hadoop.yarn-nodemanager-cgroups-cpu
name: yarn-nodemanager-cgroups-cpu
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, cgroups, cpu-limits, nodemanager, linuxcontainerexecutor]
level: advanced
status: docs-checked
description: "Limiting YARN container CPU with cgroups: LinuxContainerExecutor settings, hierarchy and mount options, percentage-physical-cpu-limit and strict-resource-usage."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/NodeManagerCgroups.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NodeManager cgroups

Cgroups lets YARN limit container resource usage; CPU is the page's example. The settings below go in yarn-site.xml.

- `yarn.nodemanager.container-executor.class` = `org.apache.hadoop.yarn.server.nodemanager.LinuxContainerExecutor`
- `yarn.nodemanager.linux-container-executor.resources-handler.class` = `org.apache.hadoop.yarn.server.nodemanager.util.CgroupsLCEResourcesHandler`. Using the LCE does not force cgroups, and DefaultLCEResourcesHandler will not work.
- `...cgroups.v2.enabled` (default false): try the cgroup v2 structure; falls back to v1 if no unified hierarchy is mounted. `...cgroups.v2.mount-path` is needed only when v1 and v2 are both in use.
- `...cgroups.hierarchy`: cgroup path for YARN processes, no commas. With mount=false and write access to the parent, YARN creates it; if it already exists, grant YARN recursive write permission.
- `...cgroups.mount`: whether LCE tries to mount cgroups if not found; not supported with cgroup v2.
- `...cgroups.mount-path` (optional): cgroups root; must exist and be readable and writable by YARN before the NodeManager starts. For v1 it holds a subdirectory per comma-separated subsystem, such as `<path>/cpu,cpuacct`; valid names are cpu, cpuacct, cpuset, memory, net_cls, blkio, freezer, devices.
- `yarn.nodemanager.linux-container-executor.group`: Unix group of the NodeManager; must match container-executor.cfg.

CPU limits (once cgroups are enabled):
- `yarn.nodemanager.resource.percentage-physical-cpu-limit`: hard upper limit on combined container CPU, e.g. 60 means containers together do not exceed 60%.
- `...cgroups.strict-resource-usage`: true stops a container using more than allocated even when CPU is spare; false lets it use spare CPU. The percentage limit applies either way.

Mount options:
- Already mounted (newer systems such as RHEL7 or Ubuntu 16, or mounted by the admin before YARN starts): set mount=false and leave the rest at defaults; YARN finds mount points in `/proc/mounts`.
- Mounted by YARN: deprecated for security reasons; container-executor.cfg `feature.mount-cgroup.enabled=0` is the default. Mount cgroups before launching YARN.
- Mounted or linked but not in `/proc/mounts` (lxcfs or another filesystem): set mount-path to the cgroups root and mount=false; YARN tries this path first.

Security: in non-secure mode the LCE runs jobs as "nobody" by default. `...nonsecure-mode.local-user` = yarn runs them as yarn; additionally `...nonsecure-mode.limit-users` = false runs them as the submitting user.

## Checked

Method: 2026-11-08, read the project's NodeManagerCgroups markdown source in full against this skill. Removed an unsupported "Verify" step and the claim that the page excludes memory limits (not stated); added the v2 settings and non-secure-mode user table from the page. Other claims were unchanged.
