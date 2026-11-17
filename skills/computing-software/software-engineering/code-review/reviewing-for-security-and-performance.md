---
id: computing-software.software-engineering.code-review.reviewing-for-security-and-performance
name: reviewing-for-security-and-performance
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, security-review, sql-injection, authorization, secrets, n-plus-one, performance-review, idor, ssrf, input-validation, owasp]
level: advanced
status: draft
description: "A checklist of what a security- and performance-aware review catches beyond logic correctness: injection, broken authz, secrets, N+1 queries, unbounded loops."
sources: ["OWASP Top 10", "personal review experience catching production incidents at review time"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing for security and performance — the checks correctness review skips

**Goal:** catch the bug classes that pass every unit test and still cause an incident
or a breach, by reviewing for a specific checklist instead of only "does this do what
the PR says."

## 1. Injection — anywhere user input reaches an interpreter
- SQL: string-built queries (`"SELECT * WHERE id=" + id`) instead of parameterized
  queries/prepared statements — the single most common finding in review. ORMs
  mostly prevent this but a raw-query escape hatch (`.exec(rawSql)`) reintroduces it.
- Shell: `subprocess.run(cmd, shell=True)` with any interpolated input; prefer
  argument lists (`shell=False`) so the shell never re-parses the string.
- Template/HTML: unescaped user content rendered into HTML (XSS) — check the
  template engine's autoescape is actually on for the context used (some disable it
  for specific trusted blocks, which user input must never flow into).
- Deserialization of untrusted data with a format that can execute code on load
  (Python `pickle`, Java native serialization, YAML's `!!python/object`) — these
  should never touch anything from outside the process boundary.

## 2. Authorization — every endpoint checks the RIGHT thing
- Authentication (who are you) is not authorization (can you do this) — a review
  catching "endpoint requires login" but not "endpoint checks the logged-in user owns
  *this* resource ID" misses IDOR (insecure direct object reference), the most common
  real-world authz bug: `GET /invoices/123` works for anyone logged in, not just the
  owner.
- Check authorization at the layer that can't be bypassed (server-side, on every
  request) — a check only in the UI, or only on the "happy path" endpoint while a
  bulk/export/admin variant skips it, is a real and common gap.
- Role checks that compare against a client-supplied field (a hidden form field for
  "role", a JWT claim the client could have influenced) instead of a server-trusted
  source are a bypass waiting to happen.

## 3. Secrets and sensitive data
- No literal API keys, passwords, or connection strings in the diff, including test
  fixtures and comments — grep `(?i)(api[_-]?key|secret|password|token)\s*=\s*['"]`
  as a review heuristic, not a complete check.
- Logging: does this log a password, full credit card number, or auth token at any
  level (including debug)? Logs usually have weaker access control than the database.
- New third-party calls: does the data sent (even just an email or user ID) belong
  going to that vendor, or is it an unreviewed data-sharing decision riding on an
  unrelated PR?

## 4. SSRF and outbound requests built from user input
If user input can shape a URL the server then fetches (`fetch(userProvidedUrl)` —
webhook configuration, image-by-URL, PDF-from-URL), check the code validates against
an allowlist and blocks internal/metadata addresses (`169.254.169.254`,
`localhost`, private IP ranges) — otherwise a user can make the server reach internal
services on their behalf.

## 5. Performance footguns that only show up at scale
- **N+1 queries**: a loop that calls the DB/an API once per item instead of batching
  — fine for a 3-item list in a demo, an incident at 10,000. Look for a query/fetch
  call textually inside a `for`/`map` over a collection that came from another query.
- **Unbounded loops/pagination**: any endpoint that returns "all" of something
  without a limit, or a loop that pages through an external API without a cap, is a
  latent timeout/OOM once the data grows.
- **Synchronous call in a hot path that could be async/batched** — one API call per
  request where a batch endpoint exists.
- **Missing index implied by a new query shape** — a new `WHERE`/`ORDER BY` column
  added to an existing hot query without checking it's indexed.

## Gotchas
- A security fix in review is easy to rubber-stamp as "looks safer now" without
  verifying the *original* exploit path is actually closed — ask for the specific
  input that used to break it and confirm it's now rejected.
- Rate limiting and input size limits are often missing on review precisely because
  nothing in a happy-path test exercises them — they're a review-time catch, not a
  test-time one, unless the team has load/abuse tests.
- "We'll fix the N+1 query later" tickets frequently never get prioritized until the
  incident — flag it as blocking if the endpoint is on a path with real growth, not
  "nice to have."

## Verify
- [ ] Every new query with interpolated input uses parameterization, confirmed by
      reading the actual query construction, not just the ORM call site.
- [ ] Every new endpoint's authorization check is traced to a server-trusted identity,
      not a client-supplied field.
- [ ] No secret, password, or full PII appears in the diff, including test fixtures
      and log statements.
- [ ] Any new loop over a collection that calls an external system was checked for
      N+1 and for an upper bound.

Related: computing-software.software-engineering.code-review.reviewing-a-diff,
computing-software.software-engineering.api-design.rest-resource-design-and-versioning
