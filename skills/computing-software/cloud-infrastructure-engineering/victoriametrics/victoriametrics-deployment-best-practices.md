---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-deployment-best-practices
name: victoriametrics-deployment-best-practices
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [best-practices, swap, ext4, kubernetes-resources, upgrades, file-descriptors]
level: practitioner
status: docs-checked
description: "Apply VictoriaMetrics host guidance: swap, filesystem, open files, Kubernetes resources and safe upgrades."
sources: ["https://docs.victoriametrics.com/victoriametrics/bestpractices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics deployment best practices

Install and run the latest release. Tuning is not required: flag defaults adapt automatically to CPU and RAM. Raise the OS open-files limit so more connections and data files can stay open.

Swap: disable it on vmstorage and single-node hosts because it causes latency spikes. On systemd Linux:

```text
sed -i '/\sswap\s/s/^/#/' /etc/fstab
systemctl mask swap.target
```

then reboot. Check the Troubleshooting (major page faults) and Resource usage (memory pressure) panels in the official Grafana dashboards.

Filesystem: use ext4 (others should work). Above 1TB on one ext4 partition, create it with `mkfs.ext4 -O 64bit,huge_file,extent -T huge`.

Platforms: Linux, FreeBSD, OpenBSD and Solaris/SmartOS are production-ready, Windows is experimental, macOS is for testing and development only.

Kubernetes: set requests equal to limits for stateful components such as vmstorage to avoid restarts, and avoid fractional CPU units because VictoriaMetrics needs integer thread counts and rounds down.

Upgrades and downgrades are safe unless release notes say otherwise, and skipping versions is also safe unless noted. Procedure: send SIGINT, wait for the process to exit (a few seconds), start the new version.

Backups: use vmbackup and vmrestore, with vmbackupmanager to automate. Cluster restarts follow the vmstorage, vminsert, vmselect order.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
