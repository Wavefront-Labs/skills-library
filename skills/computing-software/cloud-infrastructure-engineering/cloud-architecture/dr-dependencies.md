---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.dr-dependencies
name: dr-dependencies
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, disaster-recovery, dr-dependencies, dr-shared-services, identity-dr, dns-dr, cicd-dr, recovery-dependencies]
level: advanced
status: draft
description: "Make shared dependencies survive the disaster too: identity, DNS, secrets, CI/CD, artefacts, monitoring, IaC state and people access in the DR region."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html", "https://learn.microsoft.com/azure/reliability/disaster-recovery-overview", "https://cloud.google.com/architecture/dr-scenarios-planning-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DR for shared dependencies

## Checklist
| Dependency | DR question |
|---|---|
| Identity (IdP, SSO) | Can engineers sign in if the IdP or its region is down? Break-glass accounts? |
| DNS | Authoritative DNS on a global/anycast provider; records pre-created for DR endpoints |
| Secrets / KMS | Replicated secrets and multi-region keys available in DR |
| Artefacts | Images, packages, AMIs replicated to DR region |
| IaC state & pipelines | Terraform state backend reachable; pipelines/runners can run from DR |
| Monitoring / logging | Observability not solely in the failed region |
| Network | Hybrid connectivity to DR region (VPN/interconnect) in place |
| Third parties | Partner allow-lists include DR egress IPs; certificates valid for DR hostnames |
| People / comms | Contact lists, status page and chat available off-platform |

## Steps
1. List dependencies per workload DR plan; mark which region/provider hosts them.
2. For each, implement replication or an alternative and record in the runbook.
3. Include dependencies in DR tests (actually block the primary region, don't just start DR).

## Gotchas
- DR test that silently pulls images from the primary region registry.
- Password manager or wiki with runbooks hosted in the failed environment.

## Verify
- [ ] DR test with primary region network-isolated succeeds.
