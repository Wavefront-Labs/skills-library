---
id: computing-software.cybersecurity-defensive.authentik.policies-overview
name: policies-overview
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, policies, policy-types, geoip, reputation, event-matcher]
level: practitioner
status: docs-checked
description: "Overview of authentik policies and bindings, and how to choose between Event Matcher, Expression, GeoIP, Password and Reputation policies."
sources:
  - https://docs.goauthentik.io/customize/policies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick the right policy type and understand the three-part model: a **policy** (one check), a **binding** (where it applies) and the **target** (combines bindings with Any or All). Users and groups can be bound directly where policies are, as simple allow/deny checks.

| Type | Use when |
| --- | --- |
| Event Matcher | react to events (action, app, model, client IP, AKQL queries), mostly notifications |
| Expression | custom Python logic; most flexible |
| GeoIP | allow or deny by country or ASN, or check travel distance (impossible travel) |
| Password | complexity, HIBP exposure, zxcvbn strength; usually a Prompt stage validation policy |
| Password Expiry | expire after N days; deny login or mark the password unusable |
| Password Uniqueness | prevent reuse (Enterprise) |
| Reputation | react to failed logins, e.g. show a CAPTCHA only to low-reputation requests |

The standalone Have I Been Pwned policy is deprecated; use the Password policy, which includes the check.

Prefer a built-in type when it fits (a GeoIP policy is easier to manage than a hand-written country expression), and reach for Expression only when it does not. Policies bind to flows, stage bindings, applications and sources; see the policy-bindings-evaluation skill for evaluation rules.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
