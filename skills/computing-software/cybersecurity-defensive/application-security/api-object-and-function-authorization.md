---
id: computing-software.cybersecurity-defensive.application-security.api-object-and-function-authorization
name: api-object-and-function-authorization
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [api-security, api-authorization, bola, bfla, object-level-authorization, policy-enforcement, abac, idor]
level: advanced
status: docs-checked
description: "Implement object-, function- and property-level authorisation in APIs: central deny-by-default checks on every request and tests that prove it."
sources: ["https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa1-broken-object-level-authorization.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa5-broken-function-level-authorization.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa3-broken-object-property-level-authorization.md", "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API object and function level authorisation

**Goal:** every request is checked for both "may this caller use this operation" (function level, API5:2023) and
"may this caller touch this specific object" (object level, API1:2023), plus which properties (API3:2023).

## Function level (API5)
- Have a consistent, easy-to-analyse authorisation module invoked from all business functions, often provided by
  components outside the application code.
- The enforcement mechanism should deny all access by default and require explicit grants to specific roles for every
  function.
- Review endpoints for function-level flaws with the business logic and group hierarchy in mind.
- Administrative controllers should inherit from an abstract administrative controller that checks the user's
  group or role; admin functions inside regular controllers need the same checks.

## Object level (API1)
- Use an authorisation mechanism based on user policies and hierarchy, and check in every function that uses
  client-supplied input to access a record that the logged-in user may perform the action on that record.
- Random, unpredictable GUIDs for record IDs are preferred, but the Authorization Cheat Sheet is explicit that
  obscuring or randomising IDs is generally not sufficient by itself: do not let a user access a resource because they
  guessed its identifier.
- Avoid exposing identifiers when possible: some objects can be retrieved from the authenticated user's identity and
  attributes (a securely implemented JWT or server-side session).
- Check access for the specific object on every request; access to one object of a type does not mean access to all.
  This is CWE-639 (Authorization Bypass Through User-Controlled Key), a form of IDOR.

## Property level (API3)
- Make sure the user may access every property you expose.
- Avoid generic serialisers such as `to_json()` and `to_string()`; choose the properties to return.
- Avoid automatic binding of client input to internal objects (mass assignment); allow changes only to properties the
  client should update.
- Add schema-based response validation as an extra layer, and keep returned structures to the minimum the endpoint
  needs.

## General principles (Authorization Cheat Sheet)
- Validate permissions on every request, whether AJAX, server-side or other, using global, application-wide
  configuration rather than per-method annotations that can be missed.
- Deny by default, and prefer explicit configuration over framework defaults.
- Never rely on client-side checks; enforce server-side, at the gateway or in serverless functions.
- Handle failed checks safely and centrally, and do not leak sensitive details in error messages.
- Prefer ABAC and ReBAC over plain RBAC for fine-grained and multi-tenant decisions.
- Review permissions periodically for privilege creep.

## Tests
Write tests of the authorisation mechanism and do not deploy changes that make them fail (OWASP API1). Cover: user B
cannot read, update or delete user A's object; a normal user cannot call each admin function; default access is
denied; failed checks end safely.

## Verify
Every route maps to an explicit permission, cross-user tests exist and pass in CI, and responses contain only
intended properties.

## Checked
Method: docs-checked 2026-11-09 against the OWASP API Security Top 10 2023 pages API1, API3 and API5 (raw markdown,
prevention sections read) and the OWASP Authorization Cheat Sheet (read in full). Removed unconfirmed claims and
sources not read: the Open Policy Agent documentation, framework-specific code (Spring, ASP.NET Core, Express), SQL
and ORM query filters, 404-versus-403 advice, UUIDv4 specifics, and the batch, nested route, GraphQL and caching
gotchas.
