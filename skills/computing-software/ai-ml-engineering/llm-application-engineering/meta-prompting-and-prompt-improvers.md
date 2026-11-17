---
id: computing-software.ai-ml-engineering.llm-application-engineering.meta-prompting-and-prompt-improvers
name: meta-prompting-and-prompt-improvers
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, prompt-improver, meta-prompting, prompt-generator, dspy, prompt-optimization]
level: practitioner
status: draft
description: "Use prompt generators, prompt improvers and meta-prompts (Claude Console, DSPy optimizers, an LLM rewriting a prompt) to draft and refine prompts, always gated by evals."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/prompt-generator
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/prompt-improver
  - https://dspy.ai/learn/optimization/optimizers/
  - https://platform.openai.com/docs/guides/prompt-generation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Prompt generators, improvers and meta-prompting

**Goal:** get a strong first draft prompt fast and improve it systematically, without trusting rewrites that were never measured.

## Tools
- **Prompt generator** (Claude Console, OpenAI playground "Generate"): describe the task, get a structured template with variables, role, instructions and examples. Good for blank-page starts.
- **Prompt improver** (Claude Console): takes an existing prompt plus feedback/examples and rewrites it with clearer structure, XML sections and step-by-step reasoning guidance. Rewrites tend to be longer and more thorough - better for accuracy-critical tasks, sometimes worse for latency and cost.
- **Programmatic optimizers** (DSPy `MIPROv2`, `BootstrapFewShot`; LangMem prompt optimizers): search over instructions and few-shot demos to maximise a metric on a training set.

## A meta-prompt you control
```
You are improving a prompt for {task}. Here is the current prompt:
<prompt>{prompt}</prompt>
Here are failing cases with the model's output and why it is wrong:
<failures>{failures}</failures>
Rewrite the prompt to fix these failures without breaking these passing behaviours:
<must_keep>{rules}</must_keep>
Return only the new prompt inside <new_prompt> tags, then a bullet list of changes and the failure each addresses.
```
Run it with a strong model (e.g. `claude-opus-5-5`) even if production uses a smaller one; then evaluate the new prompt on the production model.

## Process
1. Build the eval set first (including edge cases and the current failures).
2. Generate or improve candidates (several).
3. Score all candidates and the baseline on the same set; check per-case regressions, not only the average.
4. Keep a held-out split the optimizer never saw; promote only if held-out improves.
5. Read the winning prompt yourself - remove contradictions, leaked test examples and odd overfitting rules.

## Pitfalls
- Overfitting: an optimizer that sees the test set will memorise it (examples copied into the prompt).
- Prompt bloat increases cost and latency on every request; measure tokens alongside quality.
- Generated prompts written for older models may include heavy-handed emphasis that current models over-apply.
- Model-specific: a prompt optimised for one model family can regress on another; re-run when switching.

## Verify
- [ ] Improved prompt beats baseline on a held-out set with no critical per-case regressions.
- [ ] Token cost change recorded.
