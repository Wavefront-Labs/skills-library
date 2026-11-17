---
id: computing-software.qa-testing-engineering.test-automation.schemathesis-openapi-testing
name: schemathesis-openapi-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [schemathesis, openapi-testing, property-based-testing, api-testing, fuzzing]
level: practitioner
status: verified
description: "Generate API tests from an OpenAPI schema with Schemathesis: CLI and pytest usage, checks, stateful links, auth, hooks and CI reports, against environments you own."
sources:
  - https://schemathesis.readthedocs.io/en/stable/
  - https://spec.openapis.org/oas/v3.1.0
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema-based API testing from OpenAPI (Schemathesis)

**Goal:** thousands of generated requests that check the API conforms to its own OpenAPI contract and does not 500.

## CLI
```bash
pip install schemathesis
st run https://staging.example.test/openapi.json \
  --checks all \
  -H "Authorization: Bearer $TOKEN" \
  --max-examples 50 \
  --report junit --report-dir reports
```
(Verified on Schemathesis 4.32.2. Older 3.x releases used `--hypothesis-max-examples` and `--junit-xml`; check `st run --help` for your version.)
`--checks all` selects every check; `st run --help` (4.32.2) lists them: not_a_server_error, status_code_conformance, content_type_conformance, response_headers_conformance, response_schema_conformance, negative_data_rejection, positive_data_acceptance, missing_required_header, unsupported_method, allow_header_conformance, use_after_free, ensure_resource_availability, ignored_auth, object_level_authorization. The default set is smaller than `all`.
On Windows set `PYTHONUTF8=1` (the CLI crashed with a cp1252 `UnicodeEncodeError` printing its header otherwise), and in Git Bash set `MSYS_NO_PATHCONV=1` so `'^/orders'` is not rewritten to a Windows path.

## pytest integration
```python
import schemathesis
schema = schemathesis.openapi.from_url("https://staging.example.test/openapi.json")   # 3.x: schemathesis.from_uri

@schema.parametrize()
def test_api(case):
    case.call_and_validate(headers={"Authorization": f"Bearer {TOKEN}"})
```
For ASGI/WSGI apps load the schema from the app object to test in-process without a server.

## Stateful testing
Define OpenAPI `links` (e.g. `POST /orders` -> `GET /orders/{id}` using `$response.body#/id`); Schemathesis chains calls to find bugs across operations (create then fetch then delete).

## Tuning
- Restrict operations: `--include-path-regex '^/orders'`, `--exclude-method DELETE`.
- Hooks (`schemathesis.hook`) to filter generated data or add valid ids.
- Reproduce failures: output includes a curl command (secret headers shown as `[Filtered]`) and `st replay <id>`; pin generation with `--seed`. A run against a small FastAPI app reported ST201 "Schema-violating request accepted" (a string `qty` field accepted `false`) with the curl line; `--include-path-regex` and `--exclude-method` work, and a filter matching no operation only warns ("Unmatched filters").

## Gotchas
- Generates destructive requests; run only on disposable environments you own.
- A loose schema (no `required`, no formats) finds little; strictness of the schema is the oracle.
- Rate limits and WAFs block bursts; lower concurrency (`--workers 1`) or allowlist the runner.

## Verify
Run produces a JUnit report in CI, every failure has a curl reproduction, and fixes land either in the API or the schema.
