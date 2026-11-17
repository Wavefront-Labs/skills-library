---
id: computing-software.ai-ml-engineering.llm-application-engineering.llm-request-logging-pii-retention
name: llm-request-logging-pii-retention
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, llm-request-logging, pii-redaction, data-retention, observability, privacy]
level: practitioner
status: docs-checked
description: "Log LLM requests and responses responsibly: what to capture, redacting PII and secrets before storage, access controls, retention schedules and provider data retention settings."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/zero-data-retention
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Request/response logging with PII controls and retention

**Tension:** prompts and outputs are essential for debugging and evals, and they are full of personal and confidential data.

## What to log
- Always (metadata): request id, timestamp, route/feature, model id, prompt version, token usage (input/output/cache), latency, stop reason, tool calls (names), error codes, user/tenant id (pseudonymized).
- Content (prompts, retrieved context, outputs, tool arguments/results): log with redaction, sampling and access controls; or only for opted-in/internal traffic.

## Redaction pipeline
- Run PII detection (a PII detection library or service, regex for keys/tokens/cards) before writing to log storage; replace with typed placeholders (`<EMAIL_1>`) keeping consistency within a trace.
- Never log secrets: scrub API keys, auth headers, passwords from tool arguments.
- Keep a reversible vault only if a business need is approved; otherwise irreversible.

## Access and retention
- Separate content logs from metrics; restrict content to a small group with audited access.
- Retention by data class, set by your policy and legal basis: longer for metadata, shorter for redacted content, eval-promoted examples kept only with consent/legal basis.
- Support deletion requests: index logs by user id to find and delete.
- Provider side: check provider data retention terms (standard retention, zero-data-retention arrangements where available and approved). Anthropic's API and data retention page describes its standard handling and ZDR eligibility per feature.

## Tooling
Capture metrics everywhere and content only where approved; make content capture a switch, off by default.

## Verify
- [ ] Sample of stored logs scanned for PII/secrets shows none; retention jobs verified to delete on schedule.

## Checked
2026-11-01. Confirmed against Anthropic's API and data retention page: standard retention differs from zero data retention (ZDR) arrangements, and feature eligibility is listed per feature. Removed: retention periods, tool names and the OpenTelemetry content-capture claim (the cited OTel page only says the conventions moved; OWASP page blocked). The rest is process guidance with no figures.
Method: documentation only; no commands were run.
