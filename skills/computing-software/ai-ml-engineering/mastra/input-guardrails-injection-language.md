---
id: computing-software.ai-ml-engineering.mastra.input-guardrails-injection-language
name: input-guardrails-injection-language
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, guardrail, moderation, pii, promptinjectiondetector, unicodenormalizer, languagedetector, processor]
level: practitioner
status: docs-checked
description: "Add Mastra input guardrail processors for Unicode normalization, prompt injection detection, and language detection or translation, and handle blocked requests."
sources:
  - https://mastra.ai/docs/agents/guardrails
  - https://mastra.ai/docs/agents/processors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: screen user messages before they reach the model using built-in input processors from `@mastra/core/processors`.

Input processors go in the agent's `inputProcessors` array and run in order.

## Normalize text
```typescript
new UnicodeNormalizer({ stripControlChars: true, collapseWhitespace: true })
```
Unifies Unicode, standardizes whitespace, removes problematic symbols.

## Prompt injection
`PromptInjectionDetector` uses an LLM to classify injection, jailbreak and system-override patterns; it can block or rewrite.
```typescript
new PromptInjectionDetector({
  model: 'openrouter/openai/gpt-oss-safeguard-20b',
  threshold: 0.8,
  strategy: 'rewrite',
  errorStrategy: 'strict',
  detectionTypes: ['injection', 'jailbreak', 'system-override'],
})
```
Model-backed guardrails (other than `ClassifierProcessor`) default to `errorStrategy: 'warn'`: internal model failures are logged and processing continues. Use `'strict'` when unchecked content must not proceed if the guardrail model is down or returns invalid output; strict stops with a tripwire.

## Language detection and translation
```typescript
new LanguageDetector({
  model: 'openrouter/openai/gpt-oss-safeguard-20b',
  targetLanguages: ['English', 'en'],
  strategy: 'translate',
  threshold: 0.8,
})
```

## Strategies
`strategy` values include `block`, `warn`, `detect`, `redact`, `rewrite`, `translate`. Most let the request continue; `block` calls `abort()`, stopping the request and later processors.

## Handle blocked requests
- `generate()`: check `result.tripwire` (`.reason`, `.processorId`).
- `stream()`: watch `fullStream` for `chunk.type === 'tripwire'` (`chunk.payload.reason`, `.processorId`).

## Speed
Guardrails add latency per request. Use a small fast model for classification. Block-only guardrails (no message mutation) are independent and can run in parallel via a workflow processor: `createWorkflow({ id, inputSchema: ProcessorStepSchema, outputSchema: ProcessorStepSchema }).parallel([createStep(new ...), ...]).map(...).commit()`; each branch result is keyed like `processor:pii-detector`, so `.map()` to the branch whose redacted messages should carry forward. Place the workflow in `inputProcessors`.

## Violation callback
Set `processor.onViolation = ({ processorId, message, detail }) => ...` for alerting; it fires when a violation aborts the run (e.g. `block`).

Related: computing-software.ai-ml-engineering.mastra.processor-execution-order-and-attachment

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
