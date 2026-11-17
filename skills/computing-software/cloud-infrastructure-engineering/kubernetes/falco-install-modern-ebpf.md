---
id: computing-software.cloud-infrastructure-engineering.kubernetes.falco-install-modern-ebpf
name: falco-install-modern-ebpf
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, runtime-security, falco-install, modern-ebpf, falco, helm]
level: practitioner
status: docs-checked
description: "Install Falco with the modern eBPF driver via Helm, confirm it loads, trigger a test alert and route events through Falcosidekick."
sources: ["https://falco.org/docs/setup/kubernetes/", "https://falco.org/docs/concepts/event-sources/kernel/", "https://falco.org/docs/concepts/rules/overriding/", "https://falco.org/docs/concepts/rules/exceptions/", "https://github.com/falcosecurity/charts/tree/master/charts/falco", "https://github.com/falcosecurity/falcosidekick"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Falco with the modern eBPF driver

## Driver choice
- `modern_ebpf`: the modern eBPF probe is embedded in Falco (CO-RE), so no driver build or download is
  needed. It needs a kernel that exposes BTF and the required capabilities (usually kernels 5.8 or newer,
  sometimes backported to older ones). The docs mark it as the default driver.
- `kmod`: the kernel module, for kernels where the modern probe does not work. In the Helm chart
  `driver.kind` accepts `kmod`, `modern_ebpf` or `auto` (the chart default).

## Install
```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts && helm repo update
helm install falco falcosecurity/falco -n falco --create-namespace \
  --set driver.kind=modern_ebpf \
  --set tty=true \
  --set falcosidekick.enabled=true \
  --set falcosidekick.webui.enabled=true
```
Runs as a DaemonSet on every node. Use the chart's `tolerations` value for tainted node pools so no node is blind.

## Confirm it loaded
```bash
kubectl -n falco logs ds/falco
```
Check the startup log for the driver Falco opened. If the kernel lacks BTF or the needed capabilities, use `kmod`.

## Test alert
```bash
kubectl run falco-test --image=alpine:3.20 --restart=Never -- sh -c 'sleep 5; cat /etc/shadow; sleep 3600'
kubectl -n falco logs ds/falco | grep -i 'sensitive file'
```
Expect a `Read sensitive file untrusted` alert (a rule in the default ruleset) with container and Kubernetes fields.

## Outputs
Falcosidekick forwards to outputs such as Slack, Loki and Elasticsearch, and to Falco Talon. Set
`falcosidekick.config.slack.webhookurl` and `falcosidekick.config.slack.minimumpriority` to avoid noise.
With Falcosidekick, `json_output` must be true and the chart's `http_output` enabled.

## Verify
Every node runs a Ready Falco pod (`kubectl -n falco get ds falco`), and the test event reaches the
chosen output.

## Checked

Checked on 2026-10-26 against `falcosecurity/falco-website` docs (`setup/kubernetes`, `concepts/event-sources/kernel`; pushed 2026-10-24), the Falco Helm chart (`charts/falco/values.yaml`, `README.md`), the Falco default ruleset (`falcosecurity/rules`) and `falcosidekick` `config_example.yaml`.
Confirmed: `helm install ... --set tty=true falcosecurity/falco`; modern eBPF probe embedded, BTF requirement, kernel 5.8 guidance, listed as default; chart `driver.kind` options and `auto` default; `tolerations` value; `falcosidekick.enabled` and `falcosidekick.webui.enabled`; Slack `webhookurl` and `minimumpriority`; rule `Read sensitive file untrusted`.
Removed as unconfirmed: the legacy `ebpf` driver (not offered by the chart), the exact startup log line and the `BTF not found` message.

Method: documentation only; no commands were run.
