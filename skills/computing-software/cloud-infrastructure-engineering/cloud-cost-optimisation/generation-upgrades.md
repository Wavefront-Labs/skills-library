---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.generation-upgrades
name: generation-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-optimisation, generation-upgrades, arm-migration, graviton, instance-modernisation, price-performance, multi-arch-images]
level: practitioner
status: docs-checked
description: "Cut cost by moving to newer instance generations and ARM (Graviton): candidate selection, multi-arch images, performance testing and staged rollout."
sources: ["https://github.com/aws/aws-graviton-getting-started", "https://www.finops.org/framework/capabilities/workload-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modernising for cost: newer generations and ARM

The FinOps Workload Optimization capability notes that providers regularly release modernised
offerings such as new compute generations and new service tiers with better price-performance, and
that each release should prompt a review of existing usage. Not every opportunity needs immediate
action; weigh the savings against the full cost of the change (labour, disruption, complexity).
Validate price-performance with your own workload.

## Candidate selection
1. List spend by instance family and generation; older generations are the first review targets.
2. AWS Graviton guidance: the quickest workloads to move are Linux-based and built from open-source
   components or in-house code you can rebuild. Check licensed software with its vendor for arm64
   support.
3. AWS managed services offered on Graviton tend to be straightforward to adopt, in some cases
   needing no change (see the Graviton managed services page).
4. Inventory the stack first: operating system, container images, libraries and runtimes, build and
   test tooling, and monitoring or security agents.

## Steps
1. **Multi-arch images**: check each container image you consume for arm64 support; many images
   are multi-architecture, which simplifies mixed-architecture clusters. Amazon ECR supports
   multi-arch images.
2. Provide an arm64 environment: an arm64 AMI, and for ECS or EKS add Graviton instances (EKS node
   groups use the arm64 EKS optimised AMI).
3. Test and run performance tests on both architectures with representative load.
4. Update infrastructure as code, then roll out with a canary or blue-green deployment.
5. In Kubernetes, the well-known node label `kubernetes.io/arch` (for example `amd64`) can be used
   in node selectors to steer pods to a given architecture.
6. Re-rightsize after migration, then review commitments.

## Gotchas
- Upgrading software versions first, in the existing x86 environment, changes fewer variables at
  once; more current software is more likely to reach full Graviton performance.
- Some tools call the architecture AArch64 and others arm64; search packages under both names.
- Dedicated Graviton guidance exists per language (Java, Python, .NET, Node.js, Go and others);
  the repository's .NET migration skill lists the move to Linux for Windows and .NET Framework applications.

## Verify
- [ ] Old-generation spend share is trending down.
- [ ] Cost per request before and after for migrated services.

## Checked

Method: docs-checked 2026-11-09 against the aws-graviton-getting-started README and transition-guide.md (raw GitHub), the Kubernetes labels reference (kubernetes.io/arch entry) and the FinOps Workload Optimization page (modernisation section).
Removed as unconfirmed: Azure Cobalt and Google Axion claims (Microsoft and Google docs unreadable), "ARM is typically priced lower" and generation examples (m4/c4, Dv2), the docker buildx command, Karpenter weighting, JVM version advice, regional price-difference claim, and the list of ARM-friendly languages.
