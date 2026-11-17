---
id: computing-software.cybersecurity-defensive.authentik.flow-inspector
name: flow-inspector
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, flow-inspector, troubleshooting, flow-plan, debugging]
level: practitioner
status: docs-checked
description: "Use the authentik Flow Inspector to step through a running flow, view next stage, plan history and context, and know its permission caveats."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/flow/inspector/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: watch a flow execute and see its plan and context to debug stage-binding policies and lost state.

## Open it
- Admin interface > **Flows and Stages > Flows** > click the flow > under **Execute flow** click **Use inspector**. It opens in a new tab with the Inspector on the right.
- Or append `?inspector` to the flow URL.
- Users with the permission **Can inspect a Flow's execution** (directly or via a role) see an Inspector button at the top right of the default flow executor. Superusers always can.
- Debug mode enables it for everyone including unauthenticated users; that is for authentik development only. Prefer granting the permission.

## Warning
The flow runs normally. A User Write stage will really write user data.

## What it shows
- **Next stage**: planned next stage with name, kind and ID. Run-time-evaluated stages may still be skipped.
- **Plan history**: stages run, the active one, and those still to come.
- **Current plan context**: for example `pending_user` after an identification stage. The data is not cleaned, so a typed password appears here.
- **Session ID**: use to debug flows restarting or losing state.

## Failure
A "Bad request" when launching usually means a policy bound directly to the flow denies access, or you lack view permission on that flow.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
