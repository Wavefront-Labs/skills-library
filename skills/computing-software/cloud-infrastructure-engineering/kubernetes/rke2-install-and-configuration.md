---
id: computing-software.cloud-infrastructure-engineering.kubernetes.rke2-install-and-configuration
name: rke2-install-and-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, rke2, cluster-provisioning, air-gapped, cis-benchmark]
level: practitioner
status: docs-checked
description: "Install and configure RKE2 servers and agents via config.yaml, join HA servers, choose CNI and CIS profile, and upgrade with the system-upgrade-controller."
sources: ["https://docs.rke2.io/install/quickstart", "https://docs.rke2.io/install/configuration", "https://docs.rke2.io/install/ha", "https://docs.rke2.io/upgrades/automated", "https://docs.rke2.io/reference/ingress_migration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RKE2 install and configuration

RKE2 (Rancher's hardened distribution) ships containerd, embedded etcd, Canal by default, and
CIS-oriented defaults. The default CNI is Canal; the default ingress controller depends on version
(ingress-nginx before v1.36, Traefik for new clusters from v1.36 per the ingress migration guide).

## First server
```bash
mkdir -p /etc/rancher/rke2
cat > /etc/rancher/rke2/config.yaml <<'EOF'
token: <shared-secret>
tls-san: [rke2.example.internal]
cni: cilium
profile: cis                 # needs the host etcd user and the CIS sysctl file applied; see the hardening guide
write-kubeconfig-mode: "0600"
EOF
curl -sfL https://get.rke2.io | INSTALL_RKE2_VERSION=<version> sh -    # or INSTALL_RKE2_CHANNEL=stable|latest|testing
systemctl enable --now rke2-server
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml PATH=$PATH:/var/lib/rancher/rke2/bin
```

## Additional servers (HA, odd count) and agents
```yaml
# /etc/rancher/rke2/config.yaml on servers 2 and 3
server: https://rke2.example.internal:9345
token: <shared-secret>
tls-san: [rke2.example.internal]
```
Agents: same `server`/`token`, install with `INSTALL_RKE2_TYPE=agent`, enable `rke2-agent`.
Port 9345 is the supervisor (registration); 6443 the API. Config changes need a service restart.
On the first server, `tls-san` should name the fixed registration address; without `token`, RKE2 generates one at `/var/lib/rancher/rke2/server/node-token`.

## Customising bundled charts
Files in `/var/lib/rancher/rke2/server/manifests/` are applied automatically; a `HelmChartConfig` there
(namespace `kube-system`) overrides values of bundled charts. `disable:` accepts items such as
`rke2-coredns`, `rke2-metrics-server` and `rke2-snapshot-controller`; choose the ingress controller
with `ingress-controller: none|traefik|ingress-nginx` (the first value is the default class).

## Upgrades
Manual: rerun the installer with the new channel/version, restart servers one at a time, then
agents. Automated: system-upgrade-controller with `Plan` objects (`upgrade.cattle.io/v1`, image
`rancher/rke2-upgrade`; server plan with `concurrency: 1` and `cordon: true`, agent plan with
`prepare` args `prepare server-plan`). Do not skip minor versions.

## Operations
- etcd snapshots: `rke2 etcd-snapshot save`, scheduled via `etcd-snapshot-schedule-cron`.
- Logs: `journalctl -u rke2-server`. `kubectl`, `crictl` and `ctr` are installed in `/var/lib/rancher/rke2/bin/`
  (not on PATH). Generated containerd config: `/var/lib/rancher/rke2/agent/etc/containerd/config.toml`
  (override with a template in the same directory).

## Verify
`kubectl get nodes -o wide`; `kubectl -n kube-system get helmcharts`; kubeconfig is written to `/etc/rancher/rke2/rke2.yaml`.

## Checked

2026-10-26, against k3s-io/docs and rancher/rke2-docs on main (latest commits 2026-10-23/24; docs mention RKE2 v1.37 and containerd 2.0 era releases). Confirmed: `config.yaml` keys (`token`, `server`, `tls-san`, `cni`, `profile`, `write-kubeconfig-mode`, `disable`, `ingress-controller`), ports 9345/6443, agent install type and service, installer variables (`INSTALL_RKE2_CHANNEL` accepts stable, latest, testing), manifests directory and HelmChartConfig, Plan fields, CIS sysctl and etcd-user requirements, binary and kubeconfig locations. Wrong or stale: `INSTALL_RKE2_CHANNEL=v1.33` (channels are stable/latest/testing), `disable: rke2-ingress-nginx` (not a valid item now; use `ingress-controller`), containerd socket and crictl.yaml paths (unconfirmed, removed). Version and Rancher-managed caveats: if the cluster is imported into Rancher, Rancher manages the upgrade controller.

Method: documentation only; no commands were run.
