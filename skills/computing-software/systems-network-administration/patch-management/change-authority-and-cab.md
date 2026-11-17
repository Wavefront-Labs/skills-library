---
id: computing-software.systems-network-administration.patch-management.change-authority-and-cab
name: change-authority-and-cab
category: computing-software
field: systems-network-administration
product: patch-management
tags: [cab, change-advisory-board, change-authority, peer-review, change-enablement, itil-4]
level: practitioner
status: draft
description: "Set up change authorities and a change advisory board that adds value: delegated approval by risk, CAB agenda and membership, automated approvals, and avoiding approval theatre."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement
  - https://itrevolution.com/product/accelerate/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Change authority and CAB

**Goal:** approvals made by the people best placed to judge risk, as fast as the risk allows.

## Change authority by risk (ITIL 4)
ITIL 4 decentralises: the **change authority** is whoever is assigned to authorise a given type and risk of change.
| Change class | Authority |
|---|---|
| Standard | Pre-authorised (template owner) |
| Normal, low risk | Peer review or team lead |
| Normal, medium | Service owner(s) of affected services |
| Normal, high / cross-service | CAB |
| Emergency | Emergency change authority (named small group) |
Document this mapping in the change policy.

## CAB that works
- **Members**: change manager (chair), owners of affected services, security, operations/on-call, service desk; invite implementers for their changes.
- **Agenda** (weekly, 30-60 min): high-risk changes for the coming period; conflicts in the change schedule; failed/backed-out changes and PIR outcomes; emergency changes since last meeting (retrospective review); standard change template reviews.
- **Inputs**: RFCs complete before the cutoff; the forward schedule of change.
- **Outputs**: authorise, reject, or request more information, recorded on each change.

## Automated approvals
For changes delivered by pipelines with tests, peer-reviewed code and automated rollback, the pipeline evidence can serve as authorisation (logged automatically). Research (Accelerate/DORA) found heavyweight external approval boards correlate with slower delivery without improving stability.

## Gotchas
- CAB rubber-stamping dozens of low-risk changes wastes time and hides the risky ones; push low-risk changes down.
- Approval by people who cannot assess the technical risk adds delay, not safety.

## Verify
Change data shows approval lead time by class and failure rate by class; high-risk changes reviewed by CAB have lower failure rates than before.
