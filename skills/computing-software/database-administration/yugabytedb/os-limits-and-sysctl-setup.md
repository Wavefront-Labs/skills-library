---
id: computing-software.database-administration.yugabytedb.os-limits-and-sysctl-setup
name: os-limits-and-sysctl-setup
category: computing-software
field: database-administration
product: yugabytedb
tags: [ulimit, sysctl, limits-conf, vm-swappiness, transparent-hugepages, system-config, linux]
level: practitioner
status: docs-checked
description: "Linux settings for YugabyteDB nodes: ulimit values in limits.conf, sysctl tunables, hugepages, and distro-specific files for CentOS and Ubuntu desktop."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/manual-deployment/system-config.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/manual-deployment/install-software.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OS limits and sysctl setup

Apply these on every master and tserver node before starting processes.

`/etc/security/limits.conf` (the page's lines use `*` with `-`; log out and back in afterward, and restart running YB-Master and YB-TServer so they pick up changes):
- nofile 1048576
- nproc 12000
- core, data, fsize, rss, cpu and locks unlimited
- also sigpending 119934, memlock 64, msgqueue 819200 and stack 8192

On CentOS, `/etc/security/limits.d/20-nproc.conf` must also be configured to match (`*  soft  nproc  12000`). On a desktop distribution such as ubuntu-desktop, add `DefaultLimitNOFILE=64000` at the end of `/etc/systemd/user.conf` and `/etc/systemd/system.conf`. If you start processes with systemd and the limits are not propagated, set the `Limit*` directives in the Service section (for example `LimitNOFILE=1048576`, `LimitNPROC=12000`; use `infinity` for unlimited).

sysctl:
- On virtual machines: `vm.swappiness=0`, `vm.max_map_count=262144` (check with `sysctl vm.max_map_count`) and a `kernel.core_pattern` such as `/path/to/cores/core_%p_%t_%E`.
- On all nodes, including bare metal: `vm.overcommit_memory=1`. With 1 the kernel does not refuse memory requests based on its free-memory estimate and the OOM killer handles exhaustion. This matters most on ARM nodes whose kernel uses 64 KiB pages and is older than 5.2 (for example RHEL 8 for ARM and derivatives): with the default 0 they can refuse a request while about 8% of memory is still free and the YugabyteDB process stops.

Transparent hugepages should be enabled (the default): `/sys/kernel/mm/transparent_hugepage/enabled` should show `[always]`, `defrag` should be `defer+madvise` selected, and `khugepaged/max_ptes_none` should be 0; if not, change the kernel command line (on RHEL or CentOS with grub2, append `transparent_hugepage=always` to `GRUB_CMDLINE_LINUX`, rebuild grub.cfg and reboot). Configuring cgroups for multitenancy is optional.

YugabyteDB is not a PostgreSQL distribution: the tserver is multi-threaded, so the shared-memory and IPC kernel settings (shmmax, semaphores) that PostgreSQL needs are not required. Time synchronization is also configured on each node: chrony is the preferred NTP implementation, and YugabyteDB shuts down a YB-TServer or YB-Master when it detects clock skew larger than `--max_clock_skew_usec` (500 ms by default).

Install steps: download the tarball for your platform (x86_64 or el8-aarch64), verify the checksum, and extract it. Install a stable release for production; preview releases are for development and testing only. If you use third-party disk encryption software, it must be running before YugabyteDB services start, or restarting an encrypted node can corrupt data.

## Checked

2026-11-04. Confirmed against the System configuration page (limits.conf values, CentOS 20-nproc.conf, ubuntu-desktop DefaultLimitNOFILE, sysctl settings and which nodes they apply to, ARM 64 KiB overcommit warning, systemd Limit directives, transparent hugepage checks and grub steps, chrony and max_clock_skew_usec, cgroups optional, no shared-memory or IPC tuning needed) and the Install software page (x86_64 and aarch64 packages, checksum, stable release, disk encryption warning). Corrected: limits.conf entries are for `*`, not the yugabyte user; swappiness, max_map_count and core_pattern apply on virtual machines while overcommit applies on all nodes. Removed the `./bin/post_install.sh` claim, which is not on either cited page, and the reference to a separate clock sync skill.

Method: documentation only; no commands were run.
