---
id: computing-software.qa-testing-engineering.test-automation.wiremock-http-stubbing
name: wiremock-http-stubbing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [wiremock, service-virtualization, http-stubbing, stub-mappings, fault-simulation, stateful-stubs, wiremock-scenarios, stub-fault-injection]
level: practitioner
status: docs-checked
description: "Stub HTTP dependencies with WireMock: JSON stub mappings, request matching, response templating, stateful scenarios, fault and delay injection, and request verification."
sources:
  - https://wiremock.org/docs/stubbing/
  - https://wiremock.org/docs/simulating-faults/
  - https://wiremock.org/docs/stateful-behaviour/
  - https://wiremock.org/docs/docker/
  - https://wiremock.org/docs/verifying/
  - https://wiremock.org/docs/standalone/java-jar/
  - https://wiremock.org/docs/junit-jupiter/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WireMock HTTP stubbing

**Goal:** replace real HTTP dependencies with controllable stubs for integration and system tests.

## Run
```bash
docker run -d -p 8080:8080 wiremock/wiremock:3.13.2 --verbose
```
Inside the official image, WireMock reads stub mappings from `mappings` and response bodies from `__files` under its in-container root; the Docker page shows the exact `-v` mount target for it. Standalone, `--root-dir` sets that root. Point the app's dependency URL at `http://localhost:8080`. Java tests can use the `@WireMockTest` JUnit 5 extension (random HTTP port by default; stubs and request log reset before each test method).

## Stub mapping
```json
{
  "request": { "method": "POST", "urlPath": "/payments",
    "headers": { "Content-Type": { "contains": "json" } },
    "bodyPatterns": [ { "matchesJsonPath": "$.amount" } ] },
  "response": { "status": 402, "jsonBody": { "error": "declined" },
    "headers": { "Content-Type": "application/json" } },
  "priority": 1
}
```
Priority: 1 is highest; a stub without one gets 5. Use a low-priority catch-all (for example 10) for unknown URLs.

Response templating (Handlebars) is off by default: start with `--global-response-templating` for every stub, or `--local-response-templating` and enable it per stub. Read the templating page for helper syntax before using it.

## Faults and delays
- Fixed: `"fixedDelayMilliseconds": 2000` in `response`.
- Random: `"delayDistribution": {"type":"lognormal","median":80,"sigma":0.4}` (long-tail latency) or `{"type":"uniform","lower":15,"upper":25}`.
- Slow body: `"chunkedDribbleDelay": {"numberOfChunks":5,"totalDuration":1000}`.
- Corrupt replies: `"fault": "EMPTY_RESPONSE"`, `MALFORMED_RESPONSE_CHUNK`, `RANDOM_DATA_THEN_CLOSE`, `CONNECTION_RESET_BY_PEER`. The last works properly only on *nix; on Windows it tends to hang rather than reset.

## Stateful scenarios
A scenario is a state machine that starts in `Started`. Add `"scenarioName"`, `"requiredScenarioState"` and `"newScenarioState"` to stubs, for example a 503 stub that moves `retry` from `Started` to `failed-once`, then a 200 stub that requires `failed-once`. `GET /__admin/scenarios` shows state; `POST /__admin/scenarios/reset` resets all.

## Admin API
`POST /__admin/mappings` (add at runtime), `POST /__admin/requests/count` (verify calls with a criteria document), `GET /__admin/requests/unmatched` (debug), `POST /__admin/reset` (remove stubs and request log).

## Gotchas
- Stubs drift from the real API; generate from OpenAPI or verify with contract tests.
- Overlapping matchers: use `priority` and check unmatched requests.

## Verify
Unmatched request list is empty after a test run, and fault stubs make the app show its error handling.

## Checked
2026-10-31. Confirmed against the WireMock docs pages listed in `sources`: the Docker image's in-container root for `mappings` and `__files` (the exact `-v` mount target is on the Docker page; the literal path is kept out of this file to satisfy the lint machine-path rule), the official image tag form, `--root-dir`, `--verbose`, `--global-response-templating` and `--local-response-templating`, `@WireMockTest` behaviour (random port, reset before each test method), `matchesJsonPath` form, priority default of 5 (1 highest), delay and lognormal/uniform/chunked settings, the four fault names and the Windows caveat, scenario `Started` state and field names, and the admin endpoints listed. Removed: the Testcontainers module claim, templating helper examples, the `$[?(@.amount > 1000)]` filter, and the old `3.9.1` pin, none of which the pages confirm.
Method: documentation only; no commands were run.
