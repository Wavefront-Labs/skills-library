---
id: computing-software.cybersecurity-defensive.application-security.api-rate-limiting-and-quotas
name: api-rate-limiting-and-quotas
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [api-security, api-rate-limiting, resource-consumption, quotas, throttling, 429, pagination-limits]
level: practitioner
status: docs-checked
description: "Protect APIs from unrestricted resource consumption: rate limits, payload and pagination caps, execution limits, spending limits and 429 responses."
sources: ["https://raw.githubusercontent.com/OWASP/API-Security/master/editions/2023/en/0xa4-unrestricted-resource-consumption.md", "https://datatracker.ietf.org/doc/html/rfc6585"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API rate limiting and resource consumption limits

**Goal:** no single caller can exhaust CPU, memory, storage, bandwidth or paid third-party services (OWASP API4:2023
Unrestricted Resource Consumption).

## Limits an API needs
OWASP lists these as the limits whose absence or poor tuning makes an API vulnerable:
- execution timeouts
- maximum allocable memory
- maximum number of file descriptors
- maximum number of processes
- maximum upload file size
- number of operations in a single client request (for example GraphQL batching)
- number of records per page in a response
- spending limit with third-party service providers

## Prevention (OWASP API4:2023)
- Limit memory, CPU, restarts, file descriptors and processes, using containers or serverless code.
- Define and enforce a maximum size on all incoming parameters and payloads: string length, array element count,
  upload size (whether stored locally or in cloud storage).
- Rate limit how often a client can interact with the API in a timeframe, tuned to business needs; some endpoints need
  stricter policies.
- Limit how often a single client or user can run a single operation, for example validating an OTP or requesting
  password recovery without visiting the one-time URL.
- Validate query string and body parameters server-side, especially the one controlling the number of records returned.
- Configure spending limits for all service providers; where that is not possible, configure billing alerts.

## Examples worth testing
- A password-reset flow that triggers a paid SMS per call can cost thousands of dollars in minutes if unlimited.
- Per-request rate limiting is bypassed when a GraphQL endpoint accepts a batch of operations in one request, so limit
  operations per request too.
- Large files that outgrow a cache limit (the OWASP example: a 15 GB cache cap, file grows to 18 GB) can raise cloud bills
  sharply when no cost alerts or cost cap exist.

## Responding to limits (RFC 6585)
The `429 Too Many Requests` status means the user has sent too many requests in a given time. The response SHOULD
include details explaining the condition and MAY include a `Retry-After` header saying how long to wait. The RFC does
not define how the server identifies the user or counts requests (per resource, server-wide, or across servers; by
credentials or a cookie). Responses with 429 MUST NOT be stored by a cache. Servers are not required to use 429.

## Verify
Requests past the limit receive 429 (with `Retry-After` if you set it); oversize bodies and page sizes are rejected;
batched operations are capped; third-party spend has a cap or alert.

## Checked
Method: docs-checked 2026-11-09 against the OWASP API Security Top 10 2023 API4 page (raw markdown, read in full) and
RFC 6585 section 4. Removed unconfirmed claims and sources not read: NGINX, API Gateway, Envoy and Kong specifics,
`RateLimit-*` headers and the IETF draft, IP-versus-identity keying and NAT advice, per-replica counting, CDN and
origin gotchas, and load-test tooling.
