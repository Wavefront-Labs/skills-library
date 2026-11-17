---
id: computing-software.ai-ml-engineering.llm-application-engineering.unbounded-consumption-denial-of-wallet
name: unbounded-consumption-denial-of-wallet
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, unbounded-consumption, denial-of-wallet, rate-limits, cost-control, owasp-llm-top-10]
level: practitioner
status: docs-checked
description: "Defend against unbounded consumption (OWASP LLM10): per-user quotas, input and output caps, agent loop limits, budget alerts, abuse detection and model extraction signals."
sources:
  - https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/
  - https://platform.claude.com/docs/en/api/rate-limits
  - https://platform.claude.com/docs/en/build-with-claude/token-counting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unbounded consumption and denial of wallet (OWASP LLM10)

**Threats (OWASP LLM10:2025):** variable-length input floods, denial of wallet (high-volume operations exploiting pay-per-use pricing), continuous input overflow beyond the context window, resource-intensive queries, model extraction via the API, functional model replication (fine-tuning another model on synthetic data from yours) and side-channel attacks.

## Controls (OWASP mitigation list)
- **Input validation:** strict size limits on inputs. For Claude, the token counting endpoint is free to use but has its own requests-per-minute limits by usage tier, so count large inputs before sending.
- **Rate limiting and user quotas:** limit requests a single source can make per period; apply per user, API key and tenant, stricter for anonymous tiers.
- **Resource allocation management:** monitor and manage allocation dynamically so no single user or request consumes excessive resources.
- **Timeouts and throttling** for resource-intensive operations.
- **Limit queued and total actions** and scale with load balancing, rather than fanning out unlimited parallel calls.
- **Limit exposure of logits and logprobs:** restrict or obfuscate `logit_bias` and `logprobs` in API responses you expose.
- **Sandboxing:** restrict the LLM's access to network resources, internal services and APIs (also limits side-channel risk).
- **Logging, monitoring and anomaly detection** of resource use to spot unusual consumption.
- **Watermarking** of outputs to detect unauthorized use; **glitch token filtering** of output before it enters the context window.
- **Graceful degradation** under heavy load, keeping partial functionality.
- **Provider-side backstops:** Anthropic enforces monthly organization spend limits by tier, lets you set your own lower spend limit, and when a cap is reached API requests return HTTP 429 until the next month starts (UTC) or the limit is raised; that 429 carries no `retry-after` header, so retries fail.

## Practitioner additions (not from the cited pages)
- Output caps: a sensible `max_tokens` per route rather than the model maximum.
- Agent limits: max iterations, max tool calls, wall-clock timeout and a token budget per run, with a kill switch for runaway sessions.
- Per-feature and per-user cost dashboards and daily budget alerts.

## Abuse detection
Flag accounts with extreme volume, repetitive templated prompts, systematic coverage of the input space (extraction attempts), or many max-length requests; throttle or require verification.

## When budgets are hit
Return clear errors, fall back to cheaper models for low-priority routes, or queue work for batch processing.

## Verify
- [ ] Load test with an abusive client pattern: quotas trigger, other tenants unaffected, alert fires.

## Checked
Method: docs-checked 2026-11-09 against the OWASP LLM10:2025 page (read in full), the Claude rate-limits page (spend-limit sections, by keyword search) and the token-counting page (free-to-use statement, by keyword search). The practitioner additions section is unsourced guidance. Dropped: the prompt-caching control (not in pages read).
