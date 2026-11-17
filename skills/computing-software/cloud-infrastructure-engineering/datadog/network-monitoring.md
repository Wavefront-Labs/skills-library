---
id: computing-software.cloud-infrastructure-engineering.datadog.network-monitoring
name: network-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, network-monitoring, npm, network-performance-monitoring, flows]
level: practitioner
status: docs-checked
description: "Enable Cloud Network Monitoring in the system-probe to see traffic between hosts, containers and services."
sources: ["https://docs.datadoghq.com/network_monitoring/cloud_network_monitoring/setup/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Network Monitoring (CNM)
Goal: map dependencies and spot network issues.

```yaml
# /etc/datadog-agent/system-probe.yaml (Linux)
network_config:
  enabled: true
```

```
sudo -u dd-agent install -m 0640 /etc/datadog-agent/system-probe.yaml.example /etc/datadog-agent/system-probe.yaml
sudo systemctl restart datadog-agent
```

```yaml
# Kubernetes with Helm (chart v3.135.3 or later) values.yaml
datadog:
  networkMonitoring:
    enabled: true
```

- Linux data collection uses eBPF and needs kernel 4.4.0 or later (or eBPF features backported). Windows uses a network driver, Agent 7.27.1 or later; macOS and Windows containers are not supported.
- Install on a meaningful subset of hosts, at least 2, since CNM analyses traffic between endpoints.
- Use `system_probe_config` instead of `network_config` for Agents older than 7.24.1. The system-probe starts automatically with the Agent from 6.18 / 7.18.
- Docker needs `DD_SYSTEM_PROBE_NETWORK_ENABLED=true`, `DD_PROCESS_AGENT_ENABLED=true`, the `/sys/kernel/debug` mount, `apparmor:unconfined` and the capabilities SYS_ADMIN, SYS_RESOURCE, SYS_PTRACE, NET_ADMIN, NET_BROADCAST, NET_RAW, IPC_LOCK, CHOWN.
- Helm on GKE Autopilot, Container-Optimized OS and Bottlerocket needs extra values from the docs page. The Operator uses `features.npm.enabled: true` under the DatadogAgent spec.
- Containers: traffic aggregates by tags such as `container_name`, `task_name` and `kube_service`.
- DNS on non-standard ports (Agent 7.76.0 or later): add `dns_monitoring_ports` under `network_config`.
- SELinux: the RPM on CentOS/RHEL 7 bundles a policy; RHEL 8 and later run the Agent as `unconfined_service_t`. Other SELinux systems need the docs' custom policy steps.
- Failed connections (TCP resets, refusals, timeouts) are on by default from Agent 7.59; keep the same Agent version across hosts or failures are under-reported. Results appear on the CNM Analytics page.

Gotcha: the system-probe sidecar and Docker setup require elevated capabilities (SYS_ADMIN and others listed above) and an unconfined AppArmor profile, so expect a security review.

## Verify
- The Network page (CNM Analytics) shows traffic between your hosts after a restart.

## Checked
2026-11-09. Confirmed against the Cloud Network Monitoring setup page (kernel and OS support, system-probe config and file copy, Helm version and key, Docker flags and capabilities, Operator key, DNS ports option, SELinux notes, failed connections and the 7.59 default). Removed: the `systemctl restart ... datadog-agent-sysprobe` and `datadog-agent status | grep` commands, the "Infrastructure > Network" menu path and the Network Map wording, the `CAP_SYS_ADMIN` as only capability claim, the pilot-host, memory-growth and egress-review advice, and the DNS-monitoring-as-additional-option claim (DNS is documented on a separate page).
Method: documentation only; no commands were run.
