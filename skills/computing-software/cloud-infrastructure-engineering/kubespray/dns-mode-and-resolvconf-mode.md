---
id: computing-software.cloud-infrastructure-engineering.kubespray.dns-mode-and-resolvconf-mode
name: dns-mode-and-resolvconf-mode
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [dns, dns-mode, resolvconf-mode, coredns, host-resolvconf, docker-dns]
level: practitioner
status: docs-checked
description: "Choose Kubespray dns_mode and resolvconf_mode and understand how host resolv.conf is edited during and after deployment."
sources:
  - https://kubespray.io/docs/advanced/dns-stack.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubespray configures a cluster DNS add-on authoritative for `dns_domain` and its `svc` and `default.svc` subdomains. Nodes outside the cluster, such as external storage or a separate etcd group, are left to you.

**dns_mode** sets cluster DNS:
- `coredns` (default): CoreDNS for all queries.
- `coredns_dual`: CoreDNS plus a secondary CoreDNS stack.
- `manual`: installs no CoreDNS; you set `manual_dns_server` for Pod DNS and install your own server later.
- `none`: no DNS at all, which leaves a non-functional cluster.

**resolvconf_mode** sets DNS for `hostNetwork: true` pods and non-Kubernetes containers:
- `host_resolvconf` (default): modifies the host `/etc/resolv.conf` and dhclient configuration. Before kubelet exists the file uses `upstream_dns_servers` and `nameservers`; after cluster DNS runs, the `kubernetes/dns_config` role reconfigures it to put cluster DNS first and the others as backups. Existing records, including resolvconf base/head/cloud-init files and dhclient entries, are purged.
- `docker_dns`: adds `--dns`, `--dns-search` and `--dns-opt` to the docker daemon (defaults ndots, `timeout:2`, `attempts:2`, overridable with `docker_dns_options`). Normal pods ignore these and use kubelet's cluster DNS.
- `none`: leaves `/etc/resolv.conf` alone; hostNetwork pods cannot resolve cluster service names.

`upstream_dns_servers` (used by all modes) serve as backups early in deployment; `nameservers` is only used by `host_resolvconf` and goes after them.

## Checked

2026-11-08. Cited pages re-read in full. Modes, role behaviour and variables were confirmed on the K8s DNS stack page, DNS modes sections.

Method: documentation only; no commands were run.
