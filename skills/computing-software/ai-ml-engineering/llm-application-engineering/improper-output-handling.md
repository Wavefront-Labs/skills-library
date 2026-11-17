---
id: computing-software.ai-ml-engineering.llm-application-engineering.improper-output-handling
name: improper-output-handling
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, improper-output-handling, owasp-llm-top-10, xss, sql-injection, output-validation]
level: practitioner
status: docs-checked
description: "Treat LLM output as untrusted input (OWASP LLM05): context-aware encoding, parameterized queries, no direct shell/eval, validation of output passed to backend functions, CSP."
sources:
  - https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Improper output handling (OWASP LLM05)

**Principle:** model output can be steered by prompt input (including indirect prompt injection), so it is like giving users indirect access to extra functionality. Treat the model like any other user (zero trust) and validate what it passes downstream.

## Sinks and defenses
| Sink | Risk | Defense |
|---|---|---|
| HTML / JavaScript / Markdown shown to users | XSS | encode output for the context it lands in; if HTML must be kept, sanitize it (the OWASP XSS cheat sheet recommends DOMPurify and says to keep it patched); strict Content Security Policy |
| SQL | injection | parameterized queries or prepared statements for all database operations involving model output |
| Shell / exec / eval | remote code execution | never feed model output directly to a shell, `exec` or `eval` |
| File paths | path traversal | sanitize before building paths from model output |
| Email templates | phishing, XSS in mail clients | escape model output before putting it in templates |
| Backend functions and extensions | privilege misuse | validate model responses before they reach backend functions; extensions should validate their inputs; do not grant the LLM more privileges than end users have |

## Validation layer
Parse structured outputs, validate types and your own policy limits (for example a maximum refund amount), and reject or escalate on failure. OWASP points to ASVS for input validation and output encoding guidance.

## Monitor
Log LLM outputs and watch for unusual patterns that may indicate exploitation; OWASP lists missing monitoring and missing rate limiting or anomaly detection as impact amplifiers.

## Verify
- [ ] Red-team tests inject payloads into retrieved docs (script tags, SQL fragments) and confirm none execute or render unsafely.

## Checked
2026-11-01. Confirmed against OWASP LLM05:2025 Improper Output Handling (zero-trust treatment of the model, context-aware encoding, parameterized queries, CSP, logging and monitoring, exec/eval, path traversal and email template examples) and the OWASP XSS Prevention Cheat Sheet (DOMPurify recommendation and patching). Removed: bleach, the markdown-image exfiltration example, sandbox container advice, read-only SQL role and timeout advice, the pydantic code sample, and the approval and rate-limit rows, none of which the cited pages state.
Method: documentation only; no commands were run.
