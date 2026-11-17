---
id: computing-software.cloud-infrastructure-engineering.kubespray.cilium-hubble-bandwidth-host-firewall-and-restarts
name: cilium-hubble-bandwidth-host-firewall-and-restarts
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [cilium, hubble, bandwidth-manager, host-firewall, policy-audit, rolling-restart]
level: advanced
status: docs-checked
description: "Enable Cilium Hubble, bandwidth manager, host firewall and audit mode in Kubespray, and size the rolling-restart timeouts."
sources:
  - https://kubespray.io/docs/CNI/cilium.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Hubble** (`k8s-net-cilium.yml`):

```yml
cilium_enable_hubble: true ## enable support hubble in cilium
cilium_hubble_install: true ## install hubble-relay, hubble-ui
cilium_hubble_tls_generate: true ## install hubble-certgen and generate certificates
```

Validate with `kubectl port-forward -n kube-system svc/hubble-ui 12000:80` and open localhost port 12000. Metrics: `cilium_enable_hubble_metrics: true` with `cilium_hubble_metrics` listing `dns`, `drop`, `tcp`, `flow`, `icmp`, `http`.

**Bandwidth manager** (`cilium_enable_bandwidth_manager: true`) supports the `kubernetes.io/egress-bandwidth` annotation, needs a v5.1.x or newer kernel, and is disabled for pods selected by L7 egress policies.

**Host firewall**: `cilium_enable_host_firewall: true`. Off by default since it can break cluster connectivity. **Policy audit mode**: `cilium_policy_audit_mode: true` enforces nothing, to validate host policies first; off by default and not for production.

**Rolling restart.** cluster.yml restarts the Cilium DaemonSet, and BPF compilation makes pod start slow, scaling with nodes and endpoints. Raise the defaults:

```yaml
cilium_rolling_restart_wait_retries_count: 30
cilium_rolling_restart_wait_retries_delay_seconds: 10
```

Count times delay should be at least nodes times the pod start time (measure by restarting one pod). Higher has no drawback. The default CPU 100m:500m is conservative and slows startup, so consider raising the limit.

## Checked

2026-11-08. Cited pages re-read in full. Each option and the timeout guidance were confirmed on the Cilium page, Hubble through Upgrade considerations sections.

Method: documentation only; no commands were run.
