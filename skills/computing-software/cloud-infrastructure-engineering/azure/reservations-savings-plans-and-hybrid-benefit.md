---
id: computing-software.cloud-infrastructure-engineering.azure.reservations-savings-plans-and-hybrid-benefit
name: reservations-savings-plans-and-hybrid-benefit
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, reservations, reserved-instances, savings-plan, azure-hybrid-benefit, ahb, commitment-discounts, instance-size-flexibility, reservation-utilization, reservation-exchange, reservation-refund, scope-shared, scope-single, capacity-reservation, dev-test-pricing, spot-vms, cost-optimisation, finops, rate-optimisation]
level: practitioner
status: draft
description: "Choose Azure commitment discounts: reservations vs compute savings plans, size flexibility, scope, utilisation alerts, exchanges, and stacking Hybrid Benefit and Dev/Test."
sources: ["Microsoft Learn - What are Azure Reservations", "Microsoft Learn - Azure savings plan for compute overview and decision guide", "Microsoft Learn - Virtual machine size flexibility with Reserved VM Instances", "Microsoft Learn - Self-service exchanges and refunds for Azure Reservations", "Microsoft Learn - Azure Hybrid Benefit for Windows Server, SQL Server and Linux"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reservations, savings plans and Hybrid Benefit — buy the discount that matches the workload

**Goal:** steady-state compute covered at 30–72 % off without owning commitments that
sit idle after the next re-architecture.

## 1. Which instrument
| Workload | Buy |
|---|---|
| Stable VM family in one region, 1–3 years | **Reserved VM Instance** (up to ~72 % 3-yr; size-flexible within family group) |
| Compute that moves between families/regions/services (VMs, App Service, Functions Premium, ACA, AKS nodes, Dedicated Hosts) | **Compute savings plan** (hourly £ commitment, up to ~65 %, applied automatically to the most-discounted eligible usage first) |
| SQL Database/MI vCores, Cosmos DB RUs, Storage reserved capacity, Databricks DBUs, App Service Isolated stamps, Redis, Synapse | Service-specific **reservations** |
| Windows/SQL licences with Software Assurance | **Azure Hybrid Benefit** — stacks on top of either |
| Fault-tolerant batch | **Spot** (no commitment, up to 90 % off, evictable) |
Rule of thumb: reservations for the floor you are certain about, a savings plan for the
flexible layer above it, pay-as-you-go/Spot for the rest. Reservations are applied
before savings plans.

## 2. Sizing the purchase
- Portal *Reservations > Purchase* shows recommendations from the last 7/30/60 days of usage
  at the chosen scope; Advisor *Cost* has the same with projected savings. Target
  **≥ 95 % utilisation** for reservations; a savings plan's recommendation already aims
  at the commitment that maximises savings net of waste.
- Buy in hourly *instances* (reservations: quantity of VMs; savings plan: £/hour). Pay
  **monthly** — no interest, same price, cancellable sooner in effect.
- **Instance size flexibility** (on by default): a `D4s_v5` reservation covers two
  `D2s_v5` or half a `D8s_v5`, by ratio within the family group. Flexibility is per
  region; it does *not* cross `v4 → v5`.

## 3. Scope
- **Shared** (billing-account-wide): default — maximises utilisation across subscriptions.
- **Single subscription / RG**: for chargeback; combine with *management group* scope when
  a business unit owns a subtree.
- Change scope anytime without penalty (`az reservations reservation update --applied-scope-type Shared`).

## 4. Operate it
- Utilisation: *Reservations* blade → each shows % used over 1/7/30 days. Set the built-in
  **utilisation alert** (< 80 %) or query `ReservationTransactions`/usage exports where
  `ChargeType == "Usage"` and `ReservationId != ""`.
- Under-used reservation: **exchange** (same type, equal-or-greater value; VM exchanges
  are being phased out in favour of savings plans — check the current policy) or **refund**
  (up to £50k/yr per billing account, 12 % early-termination fee).
- Expiry: enable *auto-renew* per reservation; renewal re-evaluates quantity. Alerts at
  30/7 days come to the reservation owner — add a group.
- Scope-level RBAC: *Reservation Purchaser* on the subscription, *Reservation Administrator*
  on the tenant to see all.

## 5. Hybrid Benefit and Dev/Test
- Windows VMs: `az vm update --license-type Windows_Server` (needs 8 or 16 core licences
  with SA per VM, mobility reported via licence attestation). SQL: `--license-type AHUB`
  on SQL VM / `LicenseType=BasePrice` on SQL DB/MI. RHEL/SLES: `--license-type RHEL_BYOS`.
- Set it at create time in IaC; a policy audit (*Virtual machines should use Hybrid Benefit*)
  finds the ones that aren't.
- **Dev/Test** offers (EA Dev/Test subscription or Visual Studio subscriber PAYG Dev/Test):
  Windows VMs billed at Linux rates, SQL/App Service discounts — only for non-production,
  requires Visual Studio subscribers as users.

## Gotchas
- Reservation applies to the *meter*, not the VM; a VM shut down (not deallocated) still consumes it. Deallocated VMs waste it — that's the "utilisation 60 %" story in dev subscriptions.
- Savings plans discount compute only, never licences, storage, networking or marketplace.
- Changing region or moving to Spot/low-priority removes reservation coverage.
- Resource group scope breaks if the RG is deleted — the reservation silently stops applying.
- An EA with *Reserved Instances* purchase disabled in enrollment settings blocks everyone from buying; ask the EA admin.

## Verify
- [ ] Every active reservation ≥ 90 % utilised on the 30-day view; utilisation alerts configured.
- [ ] Amortized cost view shows reservation/savings-plan coverage ≥ target (e.g. 70 %) of eligible compute.
- [ ] Policy audit for Hybrid Benefit shows 0 non-compliant Windows/SQL VMs with SA.
- [ ] Renewal owner is a group, and auto-renew is set per the FinOps decision log.
