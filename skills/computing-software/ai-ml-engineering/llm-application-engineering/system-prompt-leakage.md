---
id: computing-software.ai-ml-engineering.llm-application-engineering.system-prompt-leakage
name: system-prompt-leakage
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, system-prompt-leakage, owasp-llm-top-10, llm-security, secrets-management, canary-tokens]
level: practitioner
status: docs-checked
description: "Address OWASP LLM07 system prompt leakage: assume prompts are public, keep secrets and authorization out of them, detect extraction with canaries, and limit impact."
sources:
  - https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/
  - https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak
  - https://genai.owasp.org/llm-top-10/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# System prompt leakage (OWASP LLM07)

**Goal:** nothing bad happens when the system prompt is extracted - because sooner or later it will be.

## The real risk
Leaking prompt text itself is usually minor (competitors see your phrasing). The damage comes from what the prompt contains or what it is relied on for:
- credentials, API keys, internal URLs, connection strings;
- authorization rules and role or permission structures that the application does not enforce elsewhere;
- filtering criteria that tell attackers exactly what to avoid;
- internal business logic or confidential data about customers.

## Rules
1. **No secrets in prompts.** Tools fetch credentials server-side; the model never sees them.
2. **No security decisions in prompts.** Access control, rate limits, transaction limits are enforced in code (tool layer, API gateway). The prompt may describe them for good UX; enforcement is elsewhere.
3. **Minimal sensitive context:** include only data the current user may see.
4. **Treat the prompt as semi-public:** write it so publication would be embarrassing at worst.

## Reducing extraction (defence in depth, not a guarantee)
- Instruct the model not to reveal internal instructions; OWASP notes training or instructing a model this way is not a guarantee, so an independent system should inspect output.
- Put context in the system prompt, separate from user queries, and leave out proprietary details the model does not need (extra content reduces adherence to "no leak" instructions, per Anthropic).
- Output screening and post-processing (regular expressions, keyword filtering, or a prompted LLM filter) to catch leaks; Anthropic suggests trying monitoring of this kind first. A unique random marker string in the prompt that you block or flag in output is one way to implement it.
Leak-proofing makes the task more complex and can degrade performance elsewhere; test prompts thoroughly.

## Detect and respond
Log and alert on marker hits and extraction-style queries. Audit prompts and outputs periodically for leaks. Rotate anything sensitive that was ever in a prompt.

## Verify
- [ ] Grep of all prompts and templates finds no secrets, tokens or internal hostnames.
- [ ] Every rule stated in the prompt that matters for security is also enforced in code (test with the prompt removed).
- [ ] Leak detection tested with an extraction attack.

## Checked
2026-11-01. Confirmed against the OWASP LLM07:2025 System Prompt Leakage page (prompt is not a secret or security control; no credentials, roles or limits in it; enforce controls outside the LLM; external guardrails inspecting output) and Anthropic's "Reduce prompt leak" page (post-processing, avoid unnecessary proprietary details, audit regularly, leak-proofing can degrade performance, try monitoring first). Removed: the claim that current models follow no-reveal instructions fairly well, the mid-conversation system message advice, the n-gram overlap and example canary string, and the example extraction phrases.
Method: documentation only; no commands were run.
