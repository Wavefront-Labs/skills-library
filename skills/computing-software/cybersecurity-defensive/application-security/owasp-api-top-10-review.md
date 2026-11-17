---
id: computing-software.cybersecurity-defensive.application-security.owasp-api-top-10-review
name: owasp-api-top-10-review
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [api-security, owasp-api-top-10, bola, bfla, mass-assignment, api-review, ssrf, unsafe-api-consumption]
level: advanced
status: docs-checked
description: "Review an API against the OWASP API Security Top 10 2023: the vulnerability criteria for each risk turned into per-endpoint checks."
sources: ["https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa1-broken-object-level-authorization.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa2-broken-authentication.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa3-broken-object-property-level-authorization.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa4-unrestricted-resource-consumption.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa5-broken-function-level-authorization.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa7-server-side-request-forgery.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa8-security-misconfiguration.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa9-improper-inventory-management.md", "https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xaa-unsafe-consumption-of-apis.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OWASP API Top 10 (2023) review

**Goal:** an endpoint-by-endpoint assessment against the 2023 list. Build an endpoint table (method, path, auth, object
IDs, role) and record, per finding: endpoint, risk ID, request and response, impact and fix.

## Checks (criteria from each OWASP page)
- **API1 Broken Object Level Authorization**: does every function that takes a client-supplied record ID check that
  the logged-in user may perform the action on that record? Test with a second user's objects. Fix with a policy-based
  authorisation mechanism, preferably unpredictable GUIDs, and tests that block deployment on failure.
- **API2 Broken Authentication**: vulnerable if it permits credential stuffing or brute force on one account without
  captcha or lockout; permits weak passwords; sends tokens or passwords in the URL; lets users change email or password
  or do other sensitive operations without password confirmation; does not validate token authenticity; accepts
  unsigned or weakly signed JWTs (`{"alg":"none"}`); does not validate JWT expiry; stores plaintext or weakly hashed
  passwords; uses weak keys. Treat forgot or reset password as authentication. A microservice is also vulnerable if
  other microservices can reach it unauthenticated or tokens are weak or predictable. Batching (for example GraphQL)
  can bypass login rate limits.
- **API3 Broken Object Property Level Authorization**: does the response expose properties the user should not see
  (avoid generic `to_json()`/`to_string()`), and does the request bind client input into internal properties (mass
  assignment)? Add schema-based response validation.
- **API4 Unrestricted Resource Consumption**: missing or badly set execution timeouts, memory, file descriptors,
  processes, upload size, operations per request, records per page, or third-party spend limits.
- **API5 Broken Function Level Authorization**: is there a consistent authorisation module, denying by default, with
  admin functions checked by group or role?
- **API6 Unrestricted Access to Sensitive Business Flows**: does an endpoint expose a flow (purchasing, posting,
  reservations) that excessive automated access could harm, without restriction? Risk differs by business.
- **API7 SSRF**: does the API fetch a remote resource from a user-supplied URL without validation? Look at webhooks,
  file fetching from URLs, custom SSO and URL previews. The risk cannot always be fully eliminated, so weigh the
  business needs when choosing protection.
- **API8 Security Misconfiguration**: missing hardening or badly set cloud permissions; missing patches; unnecessary
  features (HTTP verbs, logging); inconsistent request handling across the server chain; no TLS; no security or cache
  control headers (for example missing `Cache-Control` let private data be cached); missing or wrong CORS; stack
  traces in errors.
- **API9 Improper Inventory Management**: unclear host purpose (environment, who may reach it, version), missing or
  stale documentation, no retirement plan per version, missing host inventory; and sensitive data flows to third
  parties without approval, inventory or visibility. Multiple running versions expand the attack surface.
- **API10 Unsafe Consumption of APIs**: unencrypted interactions with other APIs; no validation or sanitisation of
  third-party data; blindly following redirects; no limit on resources used to process responses; no timeouts.

## Gotchas
Testing with one account hides object-level flaws, so use two users; account for all authentication flows (mobile,
web, deep links) in API2.

## Verify
Every endpoint in the table has a result for each risk; findings are retested after the fix.

## Checked
Method: docs-checked 2026-11-09 against the ten OWASP API Security Top 10 2023 pages (raw markdown; the "Is the API
vulnerable" and prevention sections read). Removed unconfirmed claims and sources not read: the OWASP API Security
Testing Guide notes and ASVS V13, and the concrete tool and request details (Burp, ZAP, metadata IP, GraphQL
introspection and gateway rate limiting remarks).
