---
id: computing-software.ai-ml-engineering.llm-application-engineering.token-counting-and-budget-control
name: token-counting-and-budget-control
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, token-counting, count-tokens, context-budget, max-tokens, history-truncation, llm-cost]
level: practitioner
status: docs-checked
description: "Count and control tokens with the Claude count_tokens endpoint: what it covers, tokenizer changes between models, window budgets, trimming and usage monitoring."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/token-counting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token counting and budget control

**Goal:** requests fit the context window, costs are predictable, and long inputs are trimmed deliberately rather than failing.

## Count with the right tokenizer
- **Claude:** `client.messages.count_tokens(model=..., system=..., messages=...)` (the `messages/count_tokens` endpoint) counts a message, including system prompt, tools, images, thinking blocks and PDFs, before you send it. The count is an estimate and the real figure can differ by a small amount; tokens added automatically by Anthropic for system optimisations may be included but are not billed.
- **Recount per model:** Claude 4.7 and later models and Claude Mythos Preview use a newer tokenizer that produces roughly 30 percent more tokens for the same text. Count the same request against the old and the new model and compare `input_tokens`; do not reuse counts or cost estimates from an older model.
- **Not supported by the endpoint:** server tools (web search, web fetch, code execution, tool search; the advisor tool is the exception), the MCP connector, and `image` or `document` blocks with a `url` or `file` source return `invalid_request_error`. Send images and PDFs as base64 to count them; for server tools and MCP, read the `usage` object in the Messages API response instead.
- **Thinking:** the current assistant turn's thinking counts toward input tokens; thinking from earlier turns counts only on models that keep all prior turns.
- **Caching:** counting does not use prompt caching even if you include `cache_control` blocks.
- **Cost and limits:** counting is free, with its own requests-per-minute limits by usage tier (Start 5,000, Build 10,000, Scale 20,000) independent of message creation limits.
- Other providers: use their own tokenizers; the sources here do not cover them.

## Budget the window
```
context window >= system + tools + retrieved docs + history + user message + max_tokens (output)
```
Allocate explicit budgets per component (e.g. docs 60%, history 25%, rest fixed) and enforce them:
- **History:** keep the system prompt and recent turns; summarise or drop older turns.
- **Retrieved documents:** fewer, better chunks (rerank, dedupe) instead of truncating mid-document.
- **Tool results:** cap size; return summaries plus IDs the model can fetch on demand.
Never silently truncate a user's document; tell the user or chunk/summarise explicitly.

## Output caps
`max_tokens` caps the response length per request. Set it per route from the observed output length distribution (author's suggestion, for example p99 x 1.5) and check the stop reason in the response for truncation. These points are not covered by the sources read.

## Monitor actual usage
Log the `usage` object from every response with route and feature tags, and alert on per-request token growth (for example an agent loop accumulating history). This is the author's practice; the sources only state that `usage` reports tokens for server-tool and MCP requests.

## Verify
- [ ] Token counts measured with the provider/model's tokenizer, not character estimates.
- [ ] Per-component budgets enforced with deliberate trimming strategies.
- [ ] `max_tokens` truncations monitored per route.

## Checked

Confirmed against the Claude Token counting guide: the endpoint, unsupported inputs, estimate wording, tokenizer change, thinking, caching, pricing and rate limits (the long multi-language code listings were not read line by line). Removed the tiktoken, OpenAI and Hugging Face guidance, the context-windows source (page not read), and unconfirmed claims about compaction, HTTP timeouts and the 4-characters-per-token rule. The window budget formula and component percentages are the author's guidance, not source text.

Method: docs-checked 2026-11-09 against https://docs.claude.com/en/docs/build-with-claude/token-counting (served from platform.claude.com)
