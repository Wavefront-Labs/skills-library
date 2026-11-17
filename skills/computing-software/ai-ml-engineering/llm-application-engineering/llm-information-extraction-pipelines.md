---
id: computing-software.ai-ml-engineering.llm-application-engineering.llm-information-extraction-pipelines
name: llm-information-extraction-pipelines
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, structured-output, llm-extraction, document-extraction, field-level-evaluation, human-review, long-documents]
level: practitioner
status: docs-checked
description: "Build production extraction from documents with LLMs: schema design, chunking long inputs, source-grounded values, confidence and review routing, and field-level evaluation."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/structured-outputs
  - https://docs.claude.com/en/docs/build-with-claude/citations
  - https://platform.openai.com/docs/guides/structured-outputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LLM information extraction pipelines

**Goal:** turn contracts, invoices, emails or reports into validated records with measured accuracy per field.

## Pipeline
1. **Ingest:** convert to text with layout (PDF text extraction, OCR for scans, table extraction). Many models accept PDFs directly; text pipelines give more control. Keep page numbers.
2. **Extract** with a schema (structured outputs). One call per document when it fits the context window; otherwise chunk.
3. **Ground:** ask for a verbatim quote or page reference per field, then verify the quote exists in the source (string match after whitespace normalisation). Unverifiable values are suspect.
4. **Validate:** types, formats (dates, currency, IDs), cross-field rules (line items sum to total), lookups against master data.
5. **Route:** pass -> store; fail or low confidence -> human review queue with the source highlighted.
6. **Learn:** reviewed corrections become eval cases and few-shot examples.

## Schema tips
- Field descriptions are instructions: "effective_date: the date the contract takes effect, not the signature date; ISO 8601; null if not stated".
- Allow `null` and say so; otherwise the model invents values.
- Lists for repeating structures (line items, parties), with a stable key per item.
- Normalisation in code, not in the prompt (currency parsing, date formats) when possible.

## Long documents
- Locate-then-extract: first find the relevant section(s) (retrieval or a cheap classification pass), then extract from them.
- Per-chunk extraction + merge with conflict rules (prefer the chunk containing the definitions section; flag disagreements for review).
- Prompt caching of the document when asking several extraction questions over the same text.

## Evaluate per field
Gold set of documents with labelled fields, sized to your field volume and variance. Per field: exact-match/normalised-match accuracy, null precision (did it correctly say "not present"), and hallucination rate (value present but not in source). Aggregate document accuracy hides weak fields.

## Verify
- [ ] Field-level accuracy table on the gold set meets targets per field.
- [ ] Every extracted value has a verified source quote or is routed to review.
- [ ] Reviewer corrections feed back into the eval set.

## Checked
2026-11-01. Confirmed against Anthropic's structured outputs, citations and PDF support pages (schema-constrained output, citations for grounding, prompt caching, PDFs accepted directly) and OpenAI's structured outputs guide. Removed the gold-set size figure. The pipeline and evaluation steps are process guidance.
Method: documentation only; no commands were run.
