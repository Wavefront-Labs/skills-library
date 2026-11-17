---
id: computing-software.cybersecurity-defensive.keycloak.authz-policy-types-role-time-aggregated
name: authz-policy-types-role-time-aggregated
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, authorization-policies, role-policy, time-policy, aggregated-policy]
level: practitioner
status: docs-checked
description: "Pick Keycloak authorization policy types: role (with required roles), time windows, and aggregated policies combined without circular references."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/authorization_services/topics/policy-aggregated-policy.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# authz policy types role time aggregated
Policies are the conditions that permissions evaluate. Three built-ins from the authorization guide:

**Role policy**: *Realm Roles* and *Client Roles* (select a Client first). By default roles are not required and access is granted if the user holds any of them; mark a role *Required* and access is granted only if the user holds all required roles (realm and client roles can be combined). *Fetch Roles*: by default only roles in the token sent with the authorization request are checked; when enabled the policy ignores token roles and checks any role associated with the user. The docs use required roles to enforce, for example, user consent for a client acting on the user's behalf (via client scope mapping).

**Time policy**: *Start time* (access only if the current time is later than or equal), *Expire time* (access only if earlier than or equal), and *Repeat* on *Day of Month*, *Month*, *Year*, *Hour* or *Minute*, each a value or a range (inclusive).

**Aggregated policy**: a policy of policies for reuse. The docs example: a Confidential Resource reachable only by users from the keycloak.org domain from a certain range of IP addresses; create a domain policy and a network policy and aggregate them. Settings: *Name*, *Description*, *Apply Policy*, *Decision Strategy* and *Logic*. Strategies: `Unanimous` (default; all policies positive), `Affirmative` (at least one positive), `Consensus` (more positive than negative decisions; a tie is negative). A circular dependency prevents creating or updating the policy.

Every policy has a unique *Name* and a *Logic* of positive (default, result kept) or negative (result negated), for example a role policy with negative logic grants only users who do not hold the role.

## Checked
2026-11-03. Confirmed against authorization_services/topics policy-role-policy.adoc, policy-role-policy-required-role.adoc, policy-time-policy.adoc, policy-aggregated-policy.adoc and policy-logic.adoc. Removed (not on the pages): server clock and NTP gotcha, the "easy to misread" warning, and the Evaluate-tab Verify step.
Method: documentation only; no commands were run.
