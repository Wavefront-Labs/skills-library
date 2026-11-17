---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.brownfield-landing-zone
name: brownfield-landing-zone
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, brownfield-landing-zone, landing-zone-migration, existing-subscriptions, control-tower-enroll, caf-brownfield, incremental-guardrails]
level: advanced
status: draft
description: "Transition an existing cloud estate into a governed landing zone: assess, map to target hierarchy, enroll accounts, introduce policy in audit then enforce, and move networks."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/enterprise-scale/transition", "https://docs.aws.amazon.com/controltower/latest/userguide/enroll-account.html", "https://cloud.google.com/architecture/landing-zones"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Brownfield landing-zone transition

## Steps
1. **Assess current state**: accounts/subscriptions, owners, hierarchy, identity, networks
   (overlapping CIDRs), policies, logging, security tooling, spend.
2. **Target design**: standard landing-zone architecture; map each existing account to a target
   OU/management group (platform, corp, online, sandbox, decommission).
3. **Foundations first**: central logging, security tooling, identity federation - these can apply
   to existing accounts without moving workloads.
4. **Enroll / move** accounts into the hierarchy (AWS Control Tower enroll account; Azure move
   subscriptions under management groups - check RBAC and policy impact first).
5. **Policies in audit mode**; report violations; remediate with owners; then switch to deny.
6. **Network**: connect to the hub where CIDRs allow; re-IP or NAT where they overlap; migrate
   to the new topology app by app.
7. **Close the gap**: new workloads only via vending; legacy accounts brought to standard over time.

## Gotchas
- Moving a subscription changes inherited RBAC and policy instantly - production breakages.
- Control Tower enrollment requires prerequisites (e.g. no conflicting AWS Config recorders) -
  pre-check.
- Overlapping IP space is the slowest part; start planning it early.

## Verify
- [ ] Every account in the target hierarchy with central logging.
- [ ] Violations trending to zero before enforcement.
