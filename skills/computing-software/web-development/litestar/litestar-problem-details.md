---
id: computing-software.web-development.litestar.litestar-problem-details
name: litestar-problem-details
category: computing-software
field: web-development
product: litestar
tags: [litestar, problem-details, rfc-9457, error-responses, exceptions, plugin, http-exception]
level: practitioner
status: docs-checked
description: "Return RFC 9457 problem details responses in Litestar with ProblemDetailsPlugin, ProblemDetailsException, HTTPException conversion and custom exception mapping."
sources: [https://docs.litestar.dev/latest/usage/plugins/problem_details.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar problem details (RFC 9457)

Goal: send machine-readable error responses per RFC 9457. Added in Litestar 2.9.0.

## Method

Register `ProblemDetailsPlugin(ProblemDetailsConfig())` (from `litestar.plugins.problem_details`), then raise `ProblemDetailsException` anywhere; it is converted into a problem details response.

```python
raise ProblemDetailsException(
    type_="https://example.com/probs/out-of-credit",
    title="You do not have enough credit.",
    detail="Your current balance is 30, but that costs 50.",
    instance="/account/12345/msgs/abc",
    extra={"balance": 30},
)

problem_details_plugin = ProblemDetailsPlugin(ProblemDetailsConfig())
app = Litestar(route_handlers=[purchase], plugins=[problem_details_plugin])
```

Convert every `HTTPException` (e.g. `NotFoundException(detail=..., extra={...})`) by enabling the flag:

```python
ProblemDetailsPlugin(ProblemDetailsConfig(enable_for_all_http_exceptions=True))
```

Convert non-HTTP exceptions with `exception_to_problem_detail_map`, a mapping from exception type to a callable returning a `ProblemDetailsException`. The docs tip says this can also override how an `HTTPException` is converted.

```python
def convert_purchase_not_allowed_to_problem_details(exc: PurchaseNotAllowedError) -> ProblemDetailsException:
    return ProblemDetailsException(
        type_="https://example.com/probs/out-of-credit",
        title="You do not have enough credit.",
        detail=exc.detail,
        instance=f"/account/{exc.account_id}/msgs/abc",
        extra={"balance": exc.balance},
    )

problem_details_plugin = ProblemDetailsPlugin(
    ProblemDetailsConfig(
        enable_for_all_http_exceptions=True,
        exception_to_problem_detail_map={PurchaseNotAllowedError: convert_purchase_not_allowed_to_problem_details},
    )
)
```

## Gotchas

- If `extra` is a `Mapping`, it is merged into the problem details response; otherwise it is included under the key `extra`.

## Verify

Raise `ProblemDetailsException` from a handler with the plugin registered; the response is a problem details document built from the fields passed (type, title, detail, instance, and `extra`).

## Checked

2026-11-07. Read the full cited page(s) (usage/plugins/problem_details.html) and the example files they include, and confirmed the claims in this skill against that text. Replaced an invented curl-style verify step with a statement of the page's behaviour.

Method: documentation only; no commands were run.
