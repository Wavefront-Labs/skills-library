---
id: computing-software.cybersecurity-defensive.cloud-security.falco-runtime-detection
name: falco-runtime-detection
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-workload-protection, falco, runtime-security, ebpf, syscall-monitoring, kubernetes-runtime-detection, falcosidekick, container-escape-detection]
level: advanced
status: docs-checked
description: "Deploy Falco for runtime threat detection on Linux hosts and Kubernetes: driver choice, least-privilege capabilities, rule file structure and where to tune rules."
sources: ["https://falco.org/docs/setup/kubernetes/", "https://falco.org/docs/concepts/event-sources/kernel/", "https://falco.org/docs/concepts/rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime detection with Falco

**Goal:** detect malicious behaviour inside running containers and on nodes in real time by
evaluating kernel (syscall) events against rules.

## Install (Kubernetes)
The Falco Operator is now the recommended deployment method on Kubernetes; the Helm chart remains fully
supported. The default Helm install adds Falco to every node as a DaemonSet and needs Falco to be privileged.
```
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
helm install --replace falco --namespace falco --create-namespace --set tty=true falcosecurity/falco
```
Nodes must be Linux, x86_64 or ARM64. Configuration is passed as Helm values (see the Falco Helm chart docs).
Check the chart's breaking-changes page before upgrading.

## Drivers (syscall event source)
- **Modern eBPF probe** (the default): embedded in Falco, uses CO-RE; set `engine.kind` to `modern_ebpf`.
  It needs BPF ring buffer support and a kernel exposing BTF; kernels 5.8 and later usually qualify, though
  features can be backported.
- **Kernel module**: installed with the deb/rpm package or via falcoctl; needs full privileges and cannot
  run with Linux capabilities alone.
- Least privilege for the modern eBPF probe: CAP_SYS_RESOURCE and CAP_SYS_PTRACE plus either CAP_SYS_ADMIN
  or the finer CAP_SYS_BPF and CAP_SYS_PERFMON (kernel 5.8+).

## Rules
A rules file is YAML with three element types: rules (conditions that generate an alert, with an output
string), macros (reusable condition snippets) and lists (collections of items). Optional
`required_engine_version` and `required_plugin_versions` track compatibility. Falco ships default rules and
lets you add your own, override rules, add exceptions, and disable or load rules selectively by tag; see the
Falco rules guides for syntax. Write custom rules in a separate file rather than editing upstream ones.

## Gotchas
- Detection only unless paired with a response tool.
- Falco has guides for dropped system call events and performance tuning under Kernel Events.

## Verify
- [ ] Falco pods are Ready on every node (`kubectl wait pods --for=condition=Ready --all -n falco`).
- [ ] A generated sample event produces an alert (Falco documents sample event generation).

## Checked
2026-11-01. Confirmed on the Falco Kubernetes (Helm), Kernel Events and Rules concept pages: Operator
recommendation, Helm commands, DaemonSet and privilege requirement, node OS and architecture, driver options and
requirements, capability list, rules file elements. Removed (not on those pages): `driver.kind` and
Falcosidekick Helm settings, the custom rule example and its fields, default rule list, Falcosidekick and Falco
Talon routing detail, the audit log plugin, managed-node restrictions, the `falco_events_dropped` metric, and
the tuning period advice.
Method: documentation only; no commands were run.
