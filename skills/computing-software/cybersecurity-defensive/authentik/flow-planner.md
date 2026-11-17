---
id: computing-software.cybersecurity-defensive.authentik.flow-planner
name: flow-planner
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, flow-planner, flow-plan, evaluate-when-planned, stage-bindings]
level: advanced
status: docs-checked
description: "How the authentik flow planner builds a per-session stage list and when stage binding policies are evaluated: at plan time or at run time."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/flow/planner/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: understand why a stage appears, is skipped, or ignores your policy.

## Planning steps
1. Verify the flow is usable in the current authentication context.
2. Evaluate policies bound directly to the flow.
3. Load stage bindings in order.
4. Evaluate stage-binding policies only where **Evaluate when flow is planned** is on.
5. Store the ordered stage list and flow context in the user's session.

The flow executor shows the first stage; on success the stage is removed and the next is shown until none remain.

## Two evaluation times
- **Evaluate when flow is planned**: policy runs at plan creation; a failing policy removes the stage from the plan.
- **Evaluate when stage is run** (default): policy runs immediately before the stage is shown; a failing policy skips the stage.
Both can be enabled on one binding.

Use plan-time when the policy needs nothing from earlier stages. Use run-time when it depends on context added by earlier stages. Example: a policy depending on `pending_user` must run at stage run time, because the Identification stage has not yet set it when the plan is built (unless it is already present).

## Session state and caching
Plans can be cached. The active plan lives in the HTTP session, so browser and API executors must keep the same session during a flow. After editing bindings or policies, start a new flow execution before troubleshooting, because an in-progress session may hold the old plan. Use the Flow Inspector to see the plan.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
