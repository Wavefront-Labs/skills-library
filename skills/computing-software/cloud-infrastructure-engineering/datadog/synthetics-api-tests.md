---
id: computing-software.cloud-infrastructure-engineering.datadog.synthetics-api-tests
name: synthetics-api-tests
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, synthetics-api, api-test, http-test, synthetic-monitoring]
level: practitioner
status: docs-checked
description: "Create HTTP, SSL, DNS and TCP Synthetic API tests with assertions, locations and alerting."
sources: ["https://docs.datadoghq.com/synthetics/api_tests/", "https://docs.datadoghq.com/synthetics/api_tests/http_tests/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synthetic API tests
Goal: external uptime and latency checks.

An HTTP test sends a request to an API endpoint and verifies response time, status code, headers or body. Typical setup in the UI:

```
Request:     GET https://shop.example.net/health
Assertions:  status code is 200
             response time is less than 1000 (ms)
             body contains "ok"            (second assertion on content)
Locations:   one or more managed locations, or a private location
Frequency:   schedule, on-demand, or from CI/CD
```

- After you click Test URL, assertions on response time, status code and the `content-type` header are pre-filled from the real response. At least one assertion is required; up to 20 per test.
- Status code supports `is`, `is not`, `matches`, `does not match`; response time supports `is less than` (ms); body supports `contains`, `is`, `matches`, `jsonpath`, `xpath`, `jsonschema` and more.
- For OR logic use the `matches` comparator with a regex such as `(200|302)`.
- JavaScript assertions (Chai `dd.expect()`, `dd.assert()`, `dd.should`) cover cases the standard assertions do not; parse JSON with `JSON.parse(dd.response.body)`.
- Run from managed locations (outside your network) or private locations (inside it). Tests can also run in CI/CD pipelines.
- Global variables from the Settings page can be used in the URL, advanced options and assertions; type `{{` to list them.
- The request body is limited to 50 KB for text-like types (3 MB per file for binary and multipart).
- Advanced option Do not save response body keeps sensitive data out of results.

Gotcha: the response body is returned only if you assert on it and the assertion fails (on success only the first 50 characters are shown), so a 200 status alone can hide an error page. Add a body assertion.

## Verify
- Results show passing runs from each chosen location; temporarily break the assertion to confirm the alert.

## Checked
2026-11-09. Confirmed against the Synthetic API tests pages (HTTP tests page: assertion types and comparators, 20-assertion limit, OR via regex, JavaScript assertions, body size limits, managed vs private locations, CI/CD, global variables, privacy option, 50-character body behaviour). Removed: the JSON test payload (API fields `tick_every`, `min_failure_duration`, `min_location_failed` are not on these pages), the "min_location_failed avoids network blips" claim, Synthetics IP range advice, the secure-global-variable and billable-run advice, and multistep guidance. The API tests overview lists the HTTP, SSL, DNS, TCP, ICMP and gRPC test types; only the HTTP page was read in detail.
Method: documentation only; no commands were run.
