---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.os-configuration-management
name: os-configuration-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, management-and-monitoring, configuration-management, ansible, systems-manager, azure-machine-configuration, desired-state]
level: practitioner
status: draft
description: "Manage OS configuration at scale in cloud: desired-state tools, baseline drift detection and remediation, immutable images vs in-place config, and fleet targeting."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html", "https://learn.microsoft.com/azure/governance/machine-configuration/overview", "https://cloud.google.com/compute/docs/os-configuration-management", "https://docs.ansible.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OS configuration management at scale

## Steps
1. **Prefer immutable**: bake configuration into golden images (Packer, EC2 Image Builder,
   Azure VM Image Builder) and replace instances; use in-place config only for long-lived
   servers.
2. **Pick a desired-state tool**: Ansible (agentless, push or via AWX/AAP), cloud-native
   (AWS Systems Manager State Manager associations, Azure Machine Configuration with Arc for
   hybrid, Google VM Manager OS policies), or Puppet/Chef/DSC where already embedded.
3. **Baseline as code**: CIS-aligned settings, agents (monitoring, EDR), time sync, log
   forwarding; version in git with review.
4. **Target fleets by tags/labels** (environment, role, OS) not by host lists.
5. **Drift**: run in audit mode first, report compliance per rule, then enable remediation in
   rings (dev, a prod canary, all prod).
6. **Report compliance** centrally (Systems Manager compliance, Azure Policy guest
   configuration results) and alert on regressions.

## Gotchas
- Auto-remediation that restarts services during business hours; schedule apply windows.
- Hybrid servers need an agent and identity (SSM hybrid activation, Azure Arc) before tooling works.

## Verify
- [ ] Compliance reported for every server against the baseline.
- [ ] Remediation rolled out through rings.
