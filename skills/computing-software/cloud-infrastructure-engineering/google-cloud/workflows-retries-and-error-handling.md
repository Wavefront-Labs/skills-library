---
id: computing-software.cloud-infrastructure-engineering.google-cloud.workflows-retries-and-error-handling
name: workflows-retries-and-error-handling
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workflows, workflows-retry-policy, workflows-error-handling, try-except, raise, http-default-retry]
level: practitioner
status: docs-checked
description: "Handle failures in Cloud Workflows: try/retry/except, built-in and custom retry predicates with backoff, raising custom errors, and the HttpError map fields."
sources: ["https://cloud.google.com/workflows/docs/reference/syntax/catching-errors", "https://cloud.google.com/workflows/docs/reference/syntax/retrying", "https://cloud.google.com/workflows/docs/reference/syntax/raising-errors"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Workflows retries and error handling

## try / retry / except
```yaml
main:
  steps:
    - call_api:
        try:
          call: http.post
          args:
            url: https://api.example.com/orders
            body: '${order}'
          result: resp
        retry:
          predicate: '${custom_retry}'
          max_retries: 5
          backoff: {initial_delay: 2, max_delay: 60, multiplier: 2}
        except:
          as: e
          steps:
            - known:
                switch:
                  - condition: '${"HttpError" in e.tags and e.code == 409}'
                    next: already_done
            - reraise:
                raise: '${e}'
    - already_done:
        return: "ok"

custom_retry:
  params: [e]
  steps:
    - what:
        switch:
          - condition: '${"HttpError" in e.tags and (e.code == 429 or e.code >= 500)}'
            return: true
    - otherwise:
        return: false
```
A retry policy is a predicate (which errors to retry) plus `max_retries` and a `backoff` with
`initial_delay`, `max_delay` and `multiplier` (seconds).

## Built-in policies
- `retry: '${http.default_retry}'`: predicate `http.default_retry_predicate`, `max_retries: 5`,
  backoff 1 s initial, 60 s max, multiplier 1.25. Retries HTTP 429, 502, 503, 504, connection
  errors, connection failures and timeout errors.
- `retry: '${http.default_retry_non_idempotent}'`: predicate
  `http.default_retry_predicate_non_idempotent`, same configuration; retries only HTTP 429 and 503 or
  connection failures. Use it for non-idempotent steps.
- You can combine a default predicate with your own retry values.

## Error map
For an `HttpError` (status >= 400) the map has `tags` (contains `HttpError`), `message`, `code`
(HTTP status), `headers` and `body`.

## Raising
An error can be a string or a map with keys you choose:
```yaml
- check:
    switch:
      - condition: '${resp.body.status != "ACCEPTED"}'
        raise:
          code: 422
          message: '${"rejected " + resp.body.reason}'
```

## Gotchas
- Retry wraps only the `try` block; keep it minimal so side effects are not repeated.
- Unhandled errors fail the execution; `gcloud workflows executions describe` shows the failure.

## Verify
- [ ] A mock endpoint returning 503 twice then 200 succeeds; a 400 goes to the `except` branch.

## Checked
2026-10-28. Confirmed against the Workflows syntax pages Catch errors, Retry steps and Raise errors: retry policy fields, both default policies with their predicates, retried status codes and backoff values, `HttpError` map attributes, string or map raise. Removed: the `auth: {type: OIDC}` argument, error tags other than `HttpError`, connector retry advice, execution and HTTP timeout figures.
Method: documentation only; no commands were run.
