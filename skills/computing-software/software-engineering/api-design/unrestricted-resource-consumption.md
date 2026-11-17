---
id: computing-software.software-engineering.api-design.unrestricted-resource-consumption
name: unrestricted-resource-consumption
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, resource-consumption, owasp-api-top-10, dos, payload-limits, page-size-limits, api-security]
level: practitioner
status: docs-checked
description: "Bound what one API request can cost (OWASP API4:2023): body size, page size, timeouts, upload limits, batching and third-party spend."
sources: ["https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/", "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unrestricted resource consumption (OWASP API4:2023)

Rate limits count requests; this risk is also about the cost of each request: network bandwidth, CPU, memory, storage, and paid downstream calls (email, SMS, phone calls, biometrics validation).

## Limits to set explicitly
OWASP says an API is vulnerable if at least one of these limits is missing or set inappropriately (too low or too high):

| Resource | Control |
|---|---|
| Execution time | execution timeouts |
| Process resources | maximum allocable memory, file descriptors and processes (containers or serverless make this easier) |
| Request body | define a maximum size for every incoming parameter and payload: string length, array element count, upload file size; reject over-size requests with 413 (REST Security Cheat Sheet) |
| Batched input | cap operations per client request (for example GraphQL batching) |
| Page size | cap records per page and validate server-side the query or body parameter that controls it |
| Per-operation frequency | throttle how often one client can run a single operation, such as validating an OTP or requesting password recovery |
| Third-party spend | spending limit for every provider or integration; billing alerts when a limit is not possible |
| Rate | rate limit per client within a timeframe, tuned to business needs, stricter on some endpoints; respond 429 |

## Scenarios from OWASP
- SMS reset flow: a script called `POST /initiate_forgot_password` tens of thousands of times, and the back end paid a per-message fee to the SMS provider each time.
- GraphQL batching: an array of `uploadPic` mutations in one request bypassed both the rate limit and the per-image size check and exhausted server memory.
- A cached file grew from under the cache service's 15GB limit to 18GB; with no cost alerts or spending cap the monthly bill rose sharply.

## Gotchas
- Request-count rate limiting does not bound work done inside one batched request.
- A 429 with `Retry-After` is friendlier than silent dropping; see the retry-after skill.
- Unbounded page-size or include parameters are a common hole; validate them server-side.
- Set limits in the proxy or gateway and also in the application, and check the product's own documentation for the exact directive names (not covered by the sources here).

Verify: send an oversize body, `?limit=1000000`, a deeply nested JSON document and a batch of many operations to staging and confirm each is refused quickly (413/400/429) without memory growth on the server.

## Checked
2026-11-08. Read in full: OWASP API Security Top 10 2023 page API4 (limit list, three scenarios, prevention list) and confirmed 413 for oversize requests and 429 for rate limiting in the OWASP REST Security Cheat Sheet. Removed: the nginx configuration block and its directive values, the example page-size figure of 100, and the compressed-body (zip bomb) gotcha, which are not on the cited pages.
Method: documentation only; no commands were run.
