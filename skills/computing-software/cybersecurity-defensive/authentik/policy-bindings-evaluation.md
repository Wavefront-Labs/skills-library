---
id: computing-software.cybersecurity-defensive.authentik.policy-bindings-evaluation
name: policy-bindings-evaluation
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, policy-bindings, policy-engine-mode, negate, failure-result, timeout]
level: practitioner
status: docs-checked
description: "How authentik evaluates policy bindings: targets, Any vs All, order, negate, timeout, failure result, execution logging and direct user or group bindings."
sources:
  - https://docs.goauthentik.io/customize/policies/bindings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: predict whether a flow, stage binding, application or source passes.

## Targets
Flow (can the user start or continue it), stage binding (does that stage run in that flow), application (can the user access it), source (usable for login or enrollment). A policy on a stage in a flow is bound to the stage binding, not the reusable stage definition. A user binding passes when the current user matches; a group binding when the user is a member.

## Evaluation rules
- **Policy engine mode** per target: `Any` (default) or `All`.
- Bindings evaluate in ascending order; disabled bindings are skipped.
- No applicable bindings means pass.
- **Negate** flips pass or fail only, messages are unchanged ("everyone except this group").
- **Timeout** (default 30 seconds) stops slow policies, relevant to expression policies calling external systems.
- **Failure Result**: pass or fail when a policy errors. Fail closed for sensitive access; fail open only when availability matters more.
- **Execution logging** on a policy logs every run, not just failures, for debugging.

## Patterns
- Static rule: bind a group directly; runtime context (network, source, prompt data, history): bind a policy.
- Run a stage for some users only: bind to the stage binding, not just the flow.
- Validate input: attach validation policies to the Prompt stage (Password, Password Uniqueness, Expression) for complexity, history, matching fields, email domain.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/customize/policies/bindings/.
Nothing was removed.
Method: documentation only; no commands were run.
