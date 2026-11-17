---
id: computing-software.cloud-infrastructure-engineering.rancher.cluster-config-k3s-form-yaml-options
name: cluster-config-k3s-form-yaml-options
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [k3s, cluster-configuration, machine-pool, service-cidr, secrets-encryption, etcd-snapshots, traefik]
level: advanced
status: docs-checked
description: "Configure Rancher-provisioned K3s clusters by form or YAML: auto replace, drain, secrets encryption, CIDRs, add-ons, etcd snapshots."
sources:
  - https://ranchermanager.docs.rancher.com/reference-guides/cluster-configuration/rancher-server-configuration/k3s-cluster-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Edit a K3s cluster from **Cluster Management** via **Edit Config** (a form for the commonly changed options) or **Edit as YAML**, where you edit options under `rkeConfig`. For anything not on the form, a K3s config file can set any option available at K3s install.

**Machine pool options:** pool name, machine count, roles (etcd, control plane, worker); under Advanced, **Auto Replace** (how long nodes may be unreachable before being deleted and replaced), **Drain Before Delete**, Kubernetes node labels and taints.

**Cluster basics:**

- Kubernetes version and the default Pod Security Admission template.
- **Encrypt Secrets** uses an AES-CBC key; if disabled afterwards, previously encrypted secrets are unreadable until encryption is enabled again.
- Project Network Isolation (if the network provider supports it), SELinux, and toggles for CoreDNS, the Klipper service load balancer, Traefik ingress and local storage. If CoreDNS is not installed you must supply another DNS provider.
- Metrics Server: if enabled, open port 10250 for inbound TCP.

**etcd:** recurring automatic snapshots with configurable frequency, and whether etcd metrics are exposed publicly or only inside the cluster.

**Networking:** Cluster CIDR defaults to `10.42.0.0/16` and Service CIDR to `10.43.0.0/16`, with IPv4, IPv6 and dual-stack forms. The caution on the page: **the Service CIDR must be configured when the cluster is first created**; it cannot be enabled on an existing cluster after it starts.

Add-On Config applies extra manifests at startup, and Agent Environment Vars sets variables on K3s agents.

## Checked

2026-11-09. Read the cited K3s Cluster Configuration Reference page in full and checked every claim against it (form and YAML editing, machine pool options, Encrypt Secrets, add-on toggles, port 10250, etcd options, CIDR defaults and Service CIDR caution). No claims removed.

Method: documentation only; no commands were run.
