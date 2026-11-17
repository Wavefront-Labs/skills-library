---
id: computing-software.cloud-infrastructure-engineering.azure.reservation-split-merge-scope-renewal-and-owners
name: reservation-split-merge-scope-renewal-and-owners
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, reservations, reservation-split, auto-renew, reservation-owner, reservation-scope, reservation-administrator]
level: practitioner
status: docs-checked
description: "Operate Azure reservations after purchase: split, change scope, toggle instance size flexibility, set auto-renew, and manage who can administer them."
sources: ["https://learn.microsoft.com/azure/cost-management-billing/reservations/manage-reserved-vm-instance", "https://learn.microsoft.com/azure/cost-management-billing/reservations/reservation-renew", "https://learn.microsoft.com/azure/cost-management-billing/reservations/view-reservations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reservation operations

**Goal:** keep reservations fully utilised as workloads move, and never let a big one silently expire.

## Change scope
A reservation scope is a single subscription, a single resource group, or **shared** (subscriptions within the
billing context). Only subscriptions within the same billing context as the reservation can be selected, and when
moving from shared to single scope you can only select subscriptions where you are the owner.
Portal: Reservations > select the reservation > Settings > Configuration.

## Split
Splitting divides one reservation into two so some instances apply to another subscription (example in the docs:
10 instances scoped to subscription A, split to 7 and 3). After a split the original reservation ID is cancelled
and two new reservations are created with the same end date; the reservation order is not affected. The quantities
must add up to the instances in the reservation being split. Split can be done in the portal, PowerShell
(`Split-AzReservation -ReservationOrderId ... -ReservationId ... -Quantity 3,2`), CLI or API.

## Instance size flexibility (VMs)
Configuration > Optimize for: **instance size flexibility** applies the discount to other VMs in the same VM size
group, or **capacity priority** prioritises data centre capacity for your deployments. Shared scope always has
instance size flexibility on; capacity priority is only available with a single scope.

## Renewal
Auto-renew buys a replacement with the same SKU, region, scope, billing subscription, term and quantity. The
renewal price is available 30 days before expiry and can change between locking it and the renewal. The replacement is set
to auto-renew off. Renewal emails go out 30 days before expiry for terms of a year or more (5 days for shorter
terms) and again on the expiration date, to reservation owners, the reservation administrator and, for EA, notification contacts.
If auto-renew is on and you do not want it, turn it off manually.

## Who can manage
- Owner of the billing subscription used to purchase gets Azure RBAC access to the reservation order; owners can add others through Access control (IAM).
- Billing profile owners/contributors (MCA) can manage reservation purchases made with the profile; billing profile readers and invoice managers can view them.
- Tenant-wide Azure RBAC roles Reservations Administrator, Reservations Contributor and Reservations Reader; Reservation Purchaser on a subscription allows buying.
- A user cannot grant access to reservations in a different Microsoft Entra tenant.

## Gotchas
- A reservation scoped to a subscription that is cancelled or moved goes unused; review on every subscription change.
- Split, merge, partial refund and exchange create new reservations under the order.

## Verify
- [ ] Utilisation is reviewed regularly; every reservation has auto-renew decided and an owner.

## Checked

Method: docs-checked 2026-11-09 against the three cited pages, downloaded and searched for the relevant passages (scope, split, optimise-for, renewal conditions and notifications, role assignments). Dropped unconfirmed az reservations commands (add extension, update, split, merge), the "scope changes are not retroactive" and "within hours" claims, the Utilisation > 95% target, and the claim that renewal lets you choose term/quantity (docs say same SKU, region, scope, term and quantity). Corrected renewal notification timing (30 days and expiry date, not 7 days).
