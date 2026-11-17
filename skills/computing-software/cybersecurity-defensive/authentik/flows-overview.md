---
id: computing-software.cybersecurity-defensive.authentik.flows-overview
name: flows-overview
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, flows, stages, designation, flow-basics, denied-action]
level: practitioner
status: docs-checked
description: "Create and configure an authentik flow: designation, authentication, compatibility mode, denied action, policy engine mode, layout, import/export."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/flow/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build a flow, a sequence of stages (identification, password, login) that authentik executes to authenticate, enrol or otherwise process a user.

## Create a flow
1. Admin interface > **Flows and Stages > Flows** > **New Flow**.
2. Set **Name** (admin list), **Title** (shown to the end user), **Slug** (appears in the URL) and **Designation** (a flow has a single purpose).
3. After creating it, bind stages to it and, optionally, policies.

A standard login flow is Identification stage (username or email), Password stage (checked against the stored hash), Login stage (attaches the pending user to the session).

## Settings that matter
- **Authentication**: whether the flow requires initial authentication, a superuser, a redirect from a Redirect stage, or an outpost.
- **Compatibility mode**: enable for password managers and mobile devices. The default UI uses Lit and Shadow DOM, which many password managers cannot handle; compatibility mode uses a polyfill and renders a traditional DOM.
- **Denied action** (when a policy denies access): `MESSAGE_CONTINUE` shows a message if no `?next` is set, otherwise redirects; `MESSAGE` always shows the error; `CONTINUE` always redirects to `?next` or the default interface.
- **Policy engine mode**: succeed if any policy passes, or only if all pass.
- **Layout** and **Background** (a flow background overrides the brand default).

## Which flow is used
authentik first checks the default flow configured in the active Brand. If none, policies of all flows with the matching designation are checked, and the first match sorted by `slug` is used.

## Stage-binding policy timing
By default stage-binding policies are evaluated right before the stage is shown. Enable **Evaluate when flow is planned** to evaluate them when the flow starts (see the flow-planner skill).

## Import and export
Flows export as blueprint YAML (since 2022.8; legacy JSON can still be imported). Imports are blueprints and may contain policies, users and groups, so only import from trusted sources and review first.

Gotcha: policies bound to a flow cannot match users or groups where no user is authenticated yet.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
