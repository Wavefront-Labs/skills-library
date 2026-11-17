---
id: computing-software.cybersecurity-defensive.security-architecture.ai-system-security-review
name: ai-system-security-review
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [ai-system-security-review, llm-security, owasp-llm-top-10, prompt-injection, nist-ai-rmf, mitre-atlas, rag-security]
level: advanced
status: draft
description: "Security-review an LLM/AI system: prompt injection paths, tool permissions, RAG data access control, output handling, model supply chain, logging and abuse monitoring."
sources: ["https://genai.owasp.org/llm-top-10/", "https://www.nist.gov/itl/ai-risk-management-framework", "https://atlas.mitre.org/", "https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AI system security review

## Map the system
User inputs, system prompt, model (hosted API / self-hosted weights), retrieval sources (RAG), tools/
plugins/agents with their credentials, output consumers (UI, code execution, emails, other systems).

## Review points (OWASP LLM Top 10 2025 aligned)
| Area | Questions |
|---|---|
| Prompt injection (direct and indirect) | Can untrusted content (web pages, emails, documents in RAG) reach the prompt? Assume it can override instructions. |
| Excessive agency | Which tools can the model call, with whose credentials? Least privilege, per-user delegated auth, human approval for destructive/financial actions |
| Sensitive information disclosure | Does RAG enforce the *requesting user's* document permissions at retrieval time? Are secrets in the system prompt? |
| Improper output handling | Is output rendered as HTML (XSS), executed as code/SQL/shell, or used in URLs (data exfil via markdown images)? Treat output as untrusted input |
| Supply chain | Model provenance, weights hashes, pickle-format risk (prefer safetensors), third-party plugins |
| Data and model poisoning | Who can write to fine-tune or RAG corpora? |
| Unbounded consumption | Rate limits, token caps, cost alerts |
| System prompt leakage | Design assuming the system prompt is public |

## Controls
- Isolation: run tool execution in sandboxes; no ambient credentials.
- Content provenance: mark retrieved content as data, but do not rely on delimiters alone.
- Logging: prompts, retrieved document IDs, tool calls and outputs (with privacy review) for investigation.
- Red-team tests: indirect injection via a planted document, exfil via rendered image URL, tool misuse.

## Gotchas
- "The model will refuse" is not a control; constrain what tools can do.
- Vector stores often lack per-document ACLs; filter by user entitlements before retrieval.

## Verify
- [ ] Indirect-injection test cannot trigger a privileged tool call without approval.
- [ ] RAG returns no documents the test user cannot open directly.
