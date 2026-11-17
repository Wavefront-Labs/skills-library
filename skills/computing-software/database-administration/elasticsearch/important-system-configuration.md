---
id: computing-software.database-administration.elasticsearch.important-system-configuration
name: important-system-configuration
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, opensearch, elasticsearch-setup, vm-max-map-count, bootstrap-memory-lock, file-descriptors, swap, bootstrap-checks, limitnofile, disable-swapping, tcp-retransmission-timeout]
level: practitioner
status: docs-checked
description: "Set the OS settings Elasticsearch bootstrap checks demand in production: vm.max_map_count, file descriptors, threads, memory lock or no swap, and how to read check failures."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/bootstrap-checks.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/vm-max-map-count.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/setup-configuration-memory.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/setting-system-settings.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/system-config-tcpretries.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/executable-jna-tmpdir.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/file-descriptors.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Important system configuration

**Goal:** nodes pass bootstrap checks and never get paged out or run out of mmaps.

Bootstrap checks become **fatal** once a node binds to a non-loopback address
(production mode). Typical startup failure:
`bootstrap check failure [1] of [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]` (the bootstrap check minimum; Elastic now recommends `1048576`).

## Settings
```bash
# mmapped Lucene files
echo 'vm.max_map_count=1048576' > /etc/sysctl.d/99-elasticsearch.conf && sysctl --system
# swap: disable, or minimise
swapoff -a     # and remove swap from /etc/fstab
echo 'vm.swappiness=1' >> /etc/sysctl.d/99-elasticsearch.conf
```
systemd override (`systemctl edit elasticsearch`):
```ini
[Service]
LimitNOFILE=65535
LimitNPROC=4096
LimitMEMLOCK=infinity       # only if using bootstrap.memory_lock
TimeoutStartSec=900          # Elasticsearch already sets 900s; only extend it on systemd older than 238
```
Alternative to disabling swap: `bootstrap.memory_lock: true` in elasticsearch.yml
plus `LimitMEMLOCK=infinity`; check `GET _nodes?filter_path=**.mlockall` is true.

Also:
- JVM heap: Elasticsearch sizes it automatically from node roles and memory. If you override it, `-Xms` = `-Xmx`, no more than 50% of RAM and under the compressed-oops threshold (26 GB is safe on most systems); set it in a file under `jvm.options.d/`.
- Temp dir must allow exec (JNA): set `ES_TMPDIR` if `/tmp` is `noexec`.
- TCP retransmission timeout: Linux defaults to 15 retransmissions (`net.ipv4.tcp_retries2=15`), which take over 900 seconds, so a dead peer is noticed only after many minutes. Elastic recommends `sysctl -w net.ipv4.tcp_retries2=5` (about 13 seconds), persisted in `/etc/sysctl.conf`. It applies to all TCP connections on the host, so weigh it if the host talks to external systems over poor networks.
- Docker/Kubernetes: `vm.max_map_count` is a **host** setting (init container or node tuning);
  ECK documents a privileged init container for it.

## Gotchas
- `ulimit` in a shell does not apply to systemd services; use the unit override.
- RPM and Debian packages already default the file descriptor limit to 65535; check effective values, not assumptions.

## Verify
```bash
curl -s 'localhost:9200/_nodes/stats/process?filter_path=**.max_file_descriptors'
curl -s 'localhost:9200/_nodes?filter_path=**.mlockall'
sysctl vm.max_map_count
```
Node starts without bootstrap-check errors in the log.

## Checked

Checked 2026-10-25 against elastic/docs-content `main` (Stack 9.x docs). Confirmed: bootstrap check minimum `262144` with recommended `1048576`; nofile 65535 and nproc 4096; swap options (`swapoff -a`, `vm.swappiness=1`, `bootstrap.memory_lock` with `LimitMEMLOCK=infinity`, `mlockall` check); `ES_TMPDIR` for `noexec` /tmp; `tcp_retries2=5` and the timing (15 retransmissions over 900 s; 5 is about 13 s); `TimeoutStartSec` default 900s. Corrected the recommended `vm.max_map_count` and the retransmission timing. The Verify `_nodes/stats/process` filter_path was not re-read.

Method: documentation only; no commands were run.
