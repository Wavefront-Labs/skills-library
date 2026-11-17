---
id: computing-software.ai-ml-engineering.llm-application-engineering.pii-redaction-for-llm-apps
name: pii-redaction-for-llm-apps
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, guardrails, pii-redaction, presidio, data-leakage, pseudonymization, privacy]
level: practitioner
status: docs-checked
description: "Prevent PII leakage in LLM apps: detect and redact with Presidio, reversible pseudonymisation, scrubbing logs and traces, access controls and output checks."
sources:
  - https://raw.githubusercontent.com/microsoft/presidio/main/docs/samples/python/presidio_notebook.ipynb
  - https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PII redaction and data leakage controls

## Where PII leaks
OWASP LLM02:2025 covers PII, financial details, health records, confidential business data, credentials and legal documents, disclosed through model output; its scenarios include a user receiving another user's personal data because of inadequate sanitisation, an attacker bypassing input filters via prompt injection to extract sensitive data, and sensitive data included in training. Practitioner view of the paths: prompts and uploads to the provider API; retrieved documents shown to the wrong user; prompts and outputs copied into logs, traces, eval sets and analytics; fine-tuning data.

## OWASP mitigations (LLM02)
- Sanitise data so user data does not enter training; scrub or mask sensitive content first. Strict input validation to detect and filter sensitive inputs.
- Least-privilege access controls; restrict the data sources the model can reach and manage runtime data orchestration securely.
- Tokenization and redaction: preprocess with pattern matching to detect and redact confidential content before processing.
- Conceal the system preamble; avoid leaking sensitive details through error messages and configuration.
- Clear policies on data retention, usage and deletion, with user opt-out of training; user education. Restrictions in the system prompt help but may be bypassed by prompt injection, so do not rely on them alone.
- Federated learning, differential privacy and homomorphic encryption are listed as advanced options.

## Detect and redact with Presidio
From Presidio's sample notebook: install `presidio_analyzer` and `presidio_anonymizer` plus a spaCy model (`python -m spacy download en_core_web_lg`).
```python
from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
analyzer = AnalyzerEngine()
results = analyzer.analyze(text=text, language="en")   # all configured recognizers; or entities=["PHONE_NUMBER"]
anonymizer = AnonymizerEngine()
clean = anonymizer.anonymize(
    text=text, analyzer_results=results,
    operators={"DEFAULT": OperatorConfig("replace", {"new_value": "<REDACTED>"})}).text
```
- The anonymizer offers five operator types: replace (default), redact, mask, hash and encrypt; per-entity operators can differ (the notebook masks PHONE_NUMBER and redacts TITLE).
- Custom recognisers: `PatternRecognizer(supported_entity="...", deny_list=[...])` (regexes via patterns also supported) added with `analyzer.registry.add_recognizer(...)`. Use them for internal ids such as customer numbers (practitioner advice: built-ins will not know them).
- NER-based detection will miss some entities and flag some wrongly (practitioner advice); measure recall and precision on your own data.

## Reversible pseudonymisation (practitioner advice)
When the model must reason about entities but the provider should not see them, replace them with stable placeholders (`<PERSON_1>`), keep the mapping in your process, send the masked text and restore placeholders in the output. Validate that the model did not invent or alter placeholders before restoring.

## Logs, traces, evals (practitioner advice)
Scrub before data leaves the process (tracing hooks, application logs, error trackers). Eval datasets built from production traffic get the same redaction plus review. Set retention on provider and own logs per your agreements.

## Output and access controls
Scope retrieval by user or tenant with filters enforced in code (OWASP: least privilege); scan output for patterns that should never appear (card numbers, other customers' emails); do not put secrets or other users' data in system prompts, and assume prompt contents can be extracted (OWASP lists concealing the system preamble).

## Verify
- [ ] Redaction recall/precision measured on a labelled sample, including custom id types.
- [ ] Trace/log samples contain no raw emails, phone numbers or card numbers (automated scan).
- [ ] Cross-tenant retrieval test returns nothing from other tenants.

## Checked
Method: docs-checked 2026-11-09 against the OWASP LLM02:2025 page (read in full) and the Presidio sample notebook on GitHub (the microsoft.github.io docs pages render only as empty stubs). Dropped: the Claude data-retention article (not read), the entity-name list (PERSON, IBAN_CODE and others, not shown in the notebook), and LangSmith `hide_inputs`. Sections marked practitioner advice are unsourced.
