---
id: computing-software.ai-ml-engineering.llm-application-engineering.reducing-hallucinations
name: reducing-hallucinations
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, reduce-hallucinations, grounding, quote-extraction, abstention, prompt-engineering]
level: practitioner
status: docs-checked
description: "Cut LLM hallucinations with prompt and system design: permission to say I don't know, quote-first grounding, citations, verification passes, retrieval and measuring the effect."
sources:
  - https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
  - https://docs.claude.com/en/docs/build-with-claude/citations
  - https://platform.openai.com/docs/guides/optimizing-llm-accuracy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reducing hallucinations

## Prompt-level techniques (cheapest first)
1. **Allow abstention:** "If the documents do not contain the answer, say 'I don't know based on the provided documents.'" Models fabricate less when uncertainty is an acceptable output.
2. **Quote first, then answer:** for long documents, ask the model to extract verbatim quotes relevant to the question first (the guide suggests this for long documents), then base the analysis only on those quotes. Claims with no supporting quote are retracted.
3. **Restrict knowledge source:** "Answer only from the provided context; do not use outside knowledge" for closed-domain tasks.
4. **Ask for citations:** use the Claude API citations feature (`citations: {"enabled": true}` on document blocks) so every claim maps to a source span you can verify or display.
5. **Chain-of-thought verification:** review the summarized reasoning in thinking blocks when an answer looks wrong, to spot faulty logic or assumptions.

## System-level techniques
- **Retrieval quality first:** most RAG hallucinations are retrieval misses; measure context recall before tuning prompts.
- **Verification pass:** a second call (iterative refinement: feed the output back and ask it to verify) checks each claim against the sources and flags unsupported ones.
- **Best-of-N consistency:** run the same prompt several times; inconsistencies across outputs can indicate hallucinations.
- **Constrain outputs:** structured output with enumerated fields leaves less room for invention; for IDs/URLs, look them up with tools rather than generating them.
- **Tools for facts:** dates, prices, account data come from tool calls, never model memory.

## Checked
2026-11-01. Confirmed against Anthropic's Reduce hallucinations guide (allow uncertainty, direct quotes, citations and retraction, best-of-N, iterative refinement, knowledge restriction, thinking review) and the citations page (`"citations": {"enabled": true}`). Removed: model id, adaptive-thinking claim, the `<quotes>` tag requirement. The OpenAI accuracy page was not used for any claim.
Method: documentation only; no commands were run.

## Measure
- Faithfulness / groundedness scores (LLM-judge checking each claim against context), abstention rate on unanswerable questions, and accuracy on answerable ones. Include deliberately unanswerable items in the eval set; otherwise "I don't know" looks like a failure.

## Trade-off
Stronger abstention lowers hallucination and raises false refusals. Tune on an eval set with both kinds of items and pick the operating point the product needs.

## Verify
- [ ] Eval reports hallucination rate and abstention correctness before and after each change.
