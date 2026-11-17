---
id: computing-software.ai-ml-engineering.llm-application-engineering.prompt-chaining-and-decomposition
name: prompt-chaining-and-decomposition
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, prompt-engineering, prompt-chaining, task-decomposition, multi-step-pipelines, self-correction]
level: practitioner
status: docs-checked
description: "Split complex LLM tasks into chained prompts: choosing step boundaries, passing outputs via tags or JSON, gates between steps, parallel sub-steps and self-review chains."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts
  - https://www.anthropic.com/engineering/building-effective-agents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prompt chaining and decomposition

**When:** one prompt asks for several distinct cognitive steps (extract, analyse, write, check) and quality, debuggability or cost suffers. Each link gets the model's full attention and can be tested and tuned alone.

## Designing the chain
1. List the subtasks with a single clear objective each (e.g., extract clauses -> assess risk per clause -> draft summary -> review summary against clauses).
2. Define the hand-off format: XML tags or JSON with a schema between steps.
3. Add programmatic **gates**: validate each output (schema, non-empty, counts) before the next step; stop or retry early instead of compounding errors.
4. Use the cheapest adequate model per step (routing easy work to smaller models is a pattern in Anthropic's building-effective-agents post).

```python
def run(contract: str):
    clauses = call(MODEL_FAST, f"<contract>{contract}</contract>\nList every liability clause as JSON ...",
                   schema=ClauseList)
    if not clauses.items:
        return {"status": "no_liability_clauses"}
    risks = parallel_map(lambda c: call(MODEL_SMART, f"<clause>{c.text}</clause>\nAssess risk ...", schema=Risk),
                         clauses.items)                     # independent -> run concurrently
    draft = call(MODEL_SMART, render("summary.txt", risks=risks))
    review = call(MODEL_SMART, f"<risks>{dump(risks)}</risks><summary>{draft}</summary>\n"
                               "List any claim in the summary not supported by the risks.", schema=Review)
    return draft if not review.unsupported else revise(draft, review)
```

## Patterns
- **Sequential pipeline:** each step consumes the previous output.
- **Parallel sectioning:** independent sub-items processed concurrently, then aggregated.
- **Self-correction:** generate -> critique against explicit criteria -> revise. Each step is a separate call, so you can log, evaluate or branch at any point.
- **Branching:** a classifier step routes to specialised prompts.

## Trade-offs
- More calls = more latency and some duplicated context tokens; cache shared prefixes and parallelise independent steps.
- Anthropic's guide says Claude handles most multistep reasoning internally with adaptive thinking and subagents; explicit chaining is still useful to inspect intermediate outputs or enforce a pipeline structure. Measure both on the eval set before committing to complexity.
- Errors propagate: log every intermediate output with a trace id so failures can be localised.

## Checked
2026-11-01. Confirmed against Anthropic's prompt-engineering guide (Chain complex prompts: self-correction draft, review, refine; XML tags) and the building-effective-agents post (prompt chaining with gates, routing, parallelization by sectioning). Removed: model ids and the iteration cap.
Method: documentation only; no commands were run.

## Verify
- [ ] Each step has its own small eval (input -> expected output) besides the end-to-end eval.
- [ ] Gate failures are counted and alerted, not silently passed downstream.
