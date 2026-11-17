---
id: computing-software.software-engineering.code-review.reviewing-error-handling-and-edge-cases
name: reviewing-error-handling-and-edge-cases
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, error-handling-review, edge-cases, exceptions, resilience, defensive-programming]
level: practitioner
status: draft
description: "Review error handling and edge cases: swallowed exceptions, missing timeouts, partial failure, retries, resource cleanup, boundary inputs and user-facing error messages."
sources: ["https://google.github.io/eng-practices/review/reviewer/looking-for.html#functionality", "https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html", "https://go.dev/blog/error-handling-and-go"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing error handling and edge cases

## Error handling checklist
- **Swallowed errors**: `except Exception: pass`, empty `catch {}`, `_ = err` in Go, `.catch(() => {})`.
  Ask: what happens to the caller and the data when this fails? At minimum log with context and
  re-raise or return an error.
- **Catch scope**: catching broad exceptions hides bugs (`KeyError` from a typo treated as "not
  found"). Catch the specific exception around the specific call.
- **Context preserved**: wrapped errors keep the cause (`raise ... from e`, `%w`, inner exception);
  messages include ids and inputs (not secrets).
- **Timeouts** on every network call, lock acquisition and external process.
- **Retries**: only idempotent operations, bounded, with backoff and jitter; not nested at
  multiple layers.
- **Partial failure**: a loop that processes 1000 items and fails on item 500. Is work committed,
  rolled back, resumable? Is the batch job idempotent if re-run?
- **Resource cleanup** on error paths: files, connections, locks, temp files (`with`, `using`,
  `try-with-resources`, `defer`).
- **Error responses**: correct status codes (4xx client vs 5xx server), no stack traces or internal
  details to users, consistent error format.
- **Fail closed** for security checks: an exception during authorization must deny, not allow.
- Panics/`unwrap()`/`!!`/`.get()` on Optional in non-test code: justified or replaced.

## Edge cases to probe (ask "what if...?")
Empty, one, many, maximum; null/None/undefined; zero, negative, overflow; duplicate entries;
unicode, very long strings, whitespace; time zones, DST transitions, leap days, end-of-month;
concurrent calls for the same entity; slow or unavailable dependency; first run with no data;
permissions missing; feature flag off.

## How to comment
Ask with a concrete scenario: "If `fetch_rates()` times out here, the order is saved with
`rate=None` and the invoice job crashes later. Should we fail the request instead?" Request a test
for the edge case rather than only a code change.
