---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.patch-management
name: patch-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, management-baseline, patch-management, image-pipeline, immutable-infrastructure, ssm-patch-manager]
level: practitioner
status: draft
description: "Set a cloud patch and image management strategy: immutable golden images versus in-place patching, tooling, cadence, compliance reporting and exceptions."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager.html", "https://learn.microsoft.com/azure/update-manager/overview", "https://cloud.google.com/compute/vm-manager/docs/patch", "https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Patch and image management strategy

## Two models
- **Immutable**: build golden images (EC2 Image Builder, Azure VM Image Builder, Packer)
  monthly or on critical CVE; roll instances via autoscaling refresh. Preferred for
  stateless fleets and containers (rebuild images on base updates).
- **In-place**: patch running VMs with AWS Systems Manager Patch Manager, Azure Update
  Manager, Google VM Manager OS patch management. For stateful or long-lived servers.

## Steps
1. **Policy**: severity-based SLAs (e.g. critical/exploited within 7 days, high 30 days),
   aligned with vulnerability management.
2. **Baselines and rings**: patch baselines per OS; deploy to dev, then a canary production
   ring, then the rest; maintenance windows per workload.
3. **Images**: pipeline with hardening (CIS), scanning, tests, versioning, distribution to
   regions/accounts; deprecate images older than N days via policy.
4. **Containers**: rebuild on base image updates; scan registries; redeploy.
5. **Compliance reporting**: patch compliance dashboards by account and team; exceptions
   with expiry.
6. **Managed services** shift patching to the provider; know their maintenance windows and opt-in upgrades.

## Gotchas
- Instances launched from old images are unpatched on day one; enforce image age.
- Reboots required by patches cause outages on single-instance workloads.

## Verify
- [ ] Patch compliance above target per severity SLA.
- [ ] No running instance from an image older than the allowed age.
