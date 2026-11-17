---
id: computing-software.qa-testing-engineering.test-case-design.ui-navigation-screen-flow-models
name: ui-navigation-screen-flow-models
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [screen-flow-model, state-transition-testing, ui-navigation, model-based-testing, e2e-testing]
level: practitioner
status: docs-checked
description: "Model UI navigation as a screen-flow state machine: screens as states, user actions as events, back/refresh/deep links, and derive navigation tests."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://graphwalker.github.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UI navigation and screen-flow state models

**Goal:** systematically cover navigation paths in web and mobile apps, including the ones users take by accident.

## Model
- **States:** screens or significant screen states (Login, Home, Cart(empty), Cart(items), Checkout-Address, Checkout-Payment, Confirmation, Error).
- **Events:** user actions (tap, submit, back button, swipe), system events (session timeout, push notification deep link, network loss).
- **Guards:** logged in or not, feature flag, role.

## Events testers forget
| Event | Expected question |
|---|---|
| Browser/OS back button | returns to sensible screen? resubmits form? |
| Refresh / reload | state preserved? duplicate POST? |
| Deep link into the middle of a flow | redirects to login then back? missing prerequisites handled? |
| Session timeout mid-flow | data kept after re-login? |
| Open in new tab / two tabs | conflicting state? |
| App backgrounded and killed | restored to which screen? |

## Deriving tests
1. Draw the screen graph (whiteboard, or a GraphWalker model).
2. Cover all screens (state coverage), then all navigation edges (transition coverage), then high-risk pairs (1-switch, e.g. Payment -> Back -> Payment).
3. Invalid transitions: direct URL to `/checkout/confirmation` without an order should redirect, not crash.
4. Implement with page objects whose methods return the next page object; the type system then mirrors the model.

## Gotchas
- SPAs with client-side routing break back/refresh in ways server-rendered pages did not; test both.
- Modal dialogs are states too; back button should close them on mobile.
- Keep the model at the level of screens, not every widget, or it becomes unmaintainable.

## Verify
The screen graph exists, every edge has a test or a documented reason, and back/refresh/deep-link cases are included for each multi-step flow.

## Checked

2026-10-28 Confirmed against: GraphWalker site (models are directed graphs of vertices and edges; edges can carry guards). Removed or generalised: the XState mention (not in the fetched pages). The rest of the skill is test-design advice without figures or named APIs.

Method: documentation only; no commands were run.
