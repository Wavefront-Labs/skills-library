---
id: computing-software.software-engineering.api-design.unsafe-consumption-of-third-party-apis
name: unsafe-consumption-of-third-party-apis
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, unsafe-api-consumption, third-party-apis, owasp-api-top-10, input-validation, redirects, api-security]
level: practitioner
status: docs-checked
description: "Treat data from upstream and partner APIs as untrusted (OWASP API10:2023): use TLS, validate and sanitise responses, allow-list redirects, set timeouts."
sources: ["https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/", "https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unsafe consumption of APIs (OWASP API10:2023)

Developers tend to trust data from third-party APIs, especially those of well-known companies, more than user input, and adopt weaker transport, authentication and validation standards for them. A compromised or buggy upstream then becomes an injection or data-poisoning path.

## OWASP: the API may be vulnerable if it
- talks to other APIs over an unencrypted channel
- does not validate and sanitise data from other APIs before processing it or passing it to downstream components
- blindly follows redirections
- does not limit the resources available to process third-party responses
- has no timeouts for interactions with third-party services

## Practices
- Assess the security posture of providers when evaluating them.
- Use TLS for every integration, including "internal" partners.
- Validate and sanitise every upstream response before use, as you would user input: check type, length, range and format with allow-list rules, apply size and nesting limits in the parser, and use parameterised queries rather than string-built SQL. The cheat sheet says data from internal APIs and partner feeds must be validated when it crosses a trust boundary (scenario #1: an SQL injection payload stored at the third-party service ran in the caller's database; scenario #3: a repository named with an SQL payload).
- Do not blindly follow redirects: keep an allow-list of well-known locations an integrated API may redirect you to. Scenario #2: a compromised provider answered `308 Permanent Redirect` with an attacker's `Location`, and the client replayed the same request, including sensitive data, to that server.
- Set timeouts and limit the resources (for example response size) spent processing third-party responses.

## Gotchas
- Webhook payloads are upstream data too: verify the signature first (see webhook-signatures).
- Pagination or "next" links returned by a partner are upstream data; apply the same host allow-list before following them.

Verify: point the client at a stub that returns oversized, wrongly typed and redirecting responses; confirm each is rejected without a crash or outbound request to the redirect target.

## Checked
2026-11-08. Read in full: OWASP API Security Top 10 2023 page API10 (vulnerability list, three scenarios, prevention list). Also read in full: OWASP Input Validation Cheat Sheet (allow-lists, parser size and nesting limits, parameterised queries, validating data from internal APIs and partner feeds). Removed: the Python snippet (library calls and specific timeout and size values were not confirmed), certificate pinning (not on the page), least-privilege and secret-manager advice, circuit breaker and alerting advice.
Method: documentation only; no commands were run.
