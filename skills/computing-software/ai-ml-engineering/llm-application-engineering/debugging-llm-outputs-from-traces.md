---
id: computing-software.ai-ml-engineering.llm-application-engineering.debugging-llm-outputs-from-traces
name: debugging-llm-outputs-from-traces
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, trace-debugging, observability, root-cause-analysis, prompt-playground, rag-debugging]
level: practitioner
status: docs-checked
description: "Debug a bad LLM answer from its trace: rendered prompt, retrieval, tool calls and outputs, classify the failure, replay with changes, and turn it into a regression case."
sources:
  - https://docs.langchain.com/langsmith/observability
  - https://langfuse.com/docs/tracing
  - https://arize.com/docs/phoenix/tracing/llm-traces
  - https://docs.claude.com/en/docs/test-and-evaluate/develop-tests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debugging bad outputs from traces

**Goal:** go from "the bot gave a wrong answer" to a confirmed root cause, a fix, and a test that keeps it fixed.

## Start from evidence
Find the trace via the conversation id, user feedback or error alert. Never debug from a user's paraphrase; get the exact inputs and outputs.

## Walk the trace in order
1. **Input:** what exactly did the user send (including attachments and prior turns)?
2. **Rendered prompt:** the final system prompt and messages sent to the model - template variables filled, history trimmed, tools listed. Many bugs are here: missing variable, wrong tenant config, stale prompt version, history truncated mid-thought.
3. **Retrieval:** queries issued, documents returned with scores. Was the right answer in the retrieved context?
4. **Tool calls:** arguments the model chose, results returned, errors, latency. Did a tool fail silently or return truncated data?
5. **Model output:** full content including thinking summaries if available, `stop_reason`, token counts.
6. **Post-processing:** parsing, guardrails, formatting - did code alter or drop content?

## Classify the failure
| Symptom in trace | Root cause class | Typical fix |
|---|---|---|
| Answer not in retrieved docs | retrieval miss | query rewriting, hybrid search, chunking, index freshness |
| Answer in context but ignored or contradicted | generation/grounding | quote-first prompting, fewer distractor chunks, stronger model |
| Instructions conflict or are ambiguous | prompt design | rewrite rules, add examples |
| Tool error or wrong arguments | tool design | clearer schemas/descriptions, validation, better errors |
| Output cut off at the token limit | truncation | raise limit, shorter format |
| Wrong data in prompt | application bug | fix code, add tests |
| Correct trace, still wrong | model capability | different model, decomposition, human review |

## Reproduce and fix
Open the exact model call in a playground (a Langfuse or Phoenix playground, or replay the logged request body), confirm the failure reproduces (run several times - it may be intermittent), change one thing, and compare. Run the change against the full regression set before shipping.

## Lock it in
Add the case (input, context, expected behaviour) to the eval dataset with the root-cause label. Track root-cause counts over time - they tell you where to invest.

## Verify
- [ ] Root cause stated with trace evidence, not a guess.
- [ ] Fix validated on the failing case and the regression set.
- [ ] Case added to the eval dataset.

## Checked
2026-11-01. Confirmed that LangSmith, Langfuse and Arize Phoenix pages describe traces capturing LLM calls with inputs, outputs and spans, and that Langfuse and Phoenix list a playground. Removed the literal stop_reason value and the LangSmith playground claim (not on the fetched pages). The failure classification table is process guidance.
Method: documentation only; no commands were run.
