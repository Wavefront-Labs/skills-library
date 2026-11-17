---
id: computing-software.cybersecurity-defensive.authentik.bindings-overview
name: bindings-overview
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, bindings, flow-stage-binding, policy-binding, entitlements, targets]
level: practitioner
status: docs-checked
description: "Understand authentik bindings: policy versus flow-stage bindings, every target type, reusable stages, and the evaluate-at-plan or at-run options."
sources:
  - https://docs.goauthentik.io/add-secure-apps/bindings-overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: know what a binding connects and where to attach checks.

Two main kinds:
- **Policy binding**: attaches a policy, user or group to a target. Targets: Flow, Flow-stage binding, Application, Application entitlement, Source, Device, Device access group, Notification rule, RAC endpoint.
- **Flow-stage binding** (stage binding): attaches a stage to a flow and sets its order. The flow planner uses these to build the flow plan.

Stages are not themselves policy targets. Because the same stage can sit in many flows, each flow-stage binding carries its own order, policies, users, groups and evaluation settings, so one stage behaves differently per flow.

## Rules
- Target **Policy engine mode** `Any` or `All`; bindings run in ascending order; options Negate, Timeout, Failure Result.
- A policy bound directly to a flow runs before the flow starts, so user or group checks on the flow itself cannot pass in authentication or enrolment flows until the user has been identified elsewhere.
- No applicable bindings means pass.
- Stage-binding evaluation: **Evaluate when flow is planned** and/or **Evaluate when stage is run**; at least one must be enabled.

## Common uses
Restrict an application by binding a group or policy (default is open to all). Run MFA only for certain users by binding to the stage binding. Use application entitlements to scope access inside an application after access is granted.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
