---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cwpp-selection
name: cwpp-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, infrastructure-protection, cwpp, cnapp, workload-protection, edr, agentless-scanning]
level: practitioner
status: draft
description: "Select and roll out a cloud workload protection platform: agent vs agentless coverage, VM/container/serverless support, CNAPP fit, EDR integration and rollout."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/defender-for-servers-overview", "https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html", "https://cloud.google.com/security-command-center/docs/security-command-center-overview", "https://www.gartner.com/en/information-technology/glossary/cloud-workload-protection-platforms-cwpp"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud workload protection platform

## Steps
1. **Define coverage needs**: VMs (Linux/Windows), containers and Kubernetes, serverless
   functions, hybrid servers; vulnerability management, malware detection, runtime threat
   detection, file integrity monitoring, hardening assessment.
2. **Agentless vs agent**: agentless snapshot scanning (Defender agentless, Inspector
   agentless EC2 scan, Wiz/Orca style) gives fast full coverage for vulnerabilities and
   secrets but no real-time prevention; agents/sensors (EDR, eBPF) give runtime detection and
   response. Most estates need both.
3. **CNAPP fit**: if you also need CSPM, CIEM and IaC scanning, a CNAPP suite reduces
   correlation work; native tools (Defender for Cloud, Inspector+GuardDuty, SCC) suit
   single-cloud estates.
4. **Evaluate**: detection efficacy on a test range, false positive rate, performance
   overhead, OS coverage, multi-cloud support, SIEM integration, licensing unit (per host,
   per vCPU, per workload).
5. **Rollout**: auto-deploy agents via policy (Azure Policy, SSM, DaemonSets), measure
   coverage percentage per account, alert on unprotected workloads.

## Gotchas
- Two overlapping agents on one host cause performance issues and conflicting quarantines.
- Agentless-only means no blocking of an active attack.

## Verify
- [ ] Coverage report: percent of workloads protected per environment.
- [ ] Detections flowing into SIEM with severity mapping.
