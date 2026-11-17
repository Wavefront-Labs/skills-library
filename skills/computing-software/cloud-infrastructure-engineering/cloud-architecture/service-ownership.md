---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.service-ownership
name: service-ownership
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, operational-excellence, service-ownership, service-catalogue, backstage, you-build-it-you-run-it]
level: practitioner
status: docs-checked
description: "Establish workload ownership and a service catalogue: named owners, metadata kept with code, Backstage catalogue behaviour, tiers as local policy, and finding orphans."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/organization.html", "https://backstage.io/docs/features/software-catalog/", "https://learn.microsoft.com/azure/well-architected/operational-excellence/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workload ownership and service catalogue

## Steps
1. **Every application, workload, platform and infrastructure component has an identified owner**, and each process
   and procedure has an owner for its definition and owners for its performance (AWS Well-Architected, Organization).
   Prefer a team over a person. When ownership is undefined you risk both missed actions and redundant, conflicting efforts.
2. **Catalogue entry** per service: owner team, criticality tier, on-call link, repository, runbooks, dashboards,
   SLOs, dependencies, data classification, accounts and lifecycle state (field list is local practice).
3. **Tooling**: the Backstage Software Catalog tracks ownership and metadata for all software (services, websites,
   libraries, data pipelines). Its source of truth is metadata YAML files stored with the code in source control, usually
   in the repository root though any location works. Components can be registered manually, created from Backstage
   Software Templates (auto-registered), or integrated from an external source; static catalog configuration with
   `catalog.locations` (type `url`) also works. Teams update metadata through their normal Git workflow and Backstage
   shows the change after a short while. Any software, including SaaS, can be registered to track ownership.
4. **Tiers** drive requirements. Define per tier what is required (on-call, redundancy, DR testing); the values are your
   own policy.
5. **Ownerless resources**: the Backstage catalogue exists to make owners discoverable and avoid orphan software;
   reconcile it with account and tag data and give orphans an adoption or decommission deadline (local practice).
6. **Reorganisations**: treat ownership transfer as a checklist item when teams change.

## Gotchas
- Hand-maintained catalogues go stale; keep the metadata next to the code so owners update it in their normal workflow.
- Shared ownership is no ownership.
- The Backstage "Unprocessed Entities" feature helps admins find entities that failed to process.

## Verify
- [ ] Every production service has an owner and tier in the catalogue.
- [ ] Alert routing matches catalogue on-call mappings.

## Checked
2026-11-08. Confirmed against the AWS Well-Architected Organization page (identified owners for each application,
workload, platform and infrastructure component; consequences of undefined ownership) and the Backstage Software
Catalog page (metadata YAML in source control, registration routes, `catalog.locations` with type `url`, team-owned
updates, SaaS registration, Unprocessed Entities). Removed: `catalog-info.yaml` file name and the `kind`, `spec.owner`,
`spec.lifecycle` and `spec.system` fields (not on this page), the "you build it, you run it" attribution and the tier 1
requirements. The Azure operational excellence landing page adds nothing checkable.
Method: documentation only; no commands were run.
