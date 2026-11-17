---
id: computing-software.ai-ml-engineering.langchain.langmem-procedural-memory-prompt-optimization
name: langmem-procedural-memory-prompt-optimization
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, procedural-memory, langmem, prompt-optimization, langgraph-store, agent-memory]
level: practitioner
status: docs-checked
description: "Update an agent's system prompt from conversation trajectories and feedback with LangMem's create_prompt_optimizer: gradient, metaprompt and prompt_memory kinds."
sources:
  - https://langchain-ai.github.io/langmem/guides/optimize_memory_prompt/
  - https://langchain-ai.github.io/langmem/reference/prompt_optimization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prompt optimisation from trajectories (LangMem)

**Goal:** improve a system prompt from real conversations and feedback. LangMem's guide describes it as feeding past conversations and feedback into an optimizer to fix issues like missed requirements or poor response structure.

## Use the optimizer
```python
from langmem import create_prompt_optimizer

optimizer = create_prompt_optimizer(
    "anthropic:claude-sonnet-5",             # model string
    kind="metaprompt",
    config={"max_reflection_steps": 1, "min_reflection_steps": 0},
)
trajectories = [
    (conversation_messages, {"score": 0.9, "comment": "Should include more details and recommended follow-up questions"}),
]
new_prompt = optimizer.invoke({"trajectories": trajectories, "prompt": "You are a planetary science expert"})
```
Each trajectory pairs a conversation with feedback. Feedback can be a dict such as `{"score": ..., "comment": ...}` (guide example) or a free-form dict such as `{"clarity": "needs more structure"}` (reference example).

## The three kinds
- `kind="gradient"`: two LLM calls per cycle, one to propose improvements and one to apply them (the guide marks it as 2-10 LLM calls). Reflection cycles are bounded by `max_reflection_steps` (default 3) and `min_reflection_steps` (default 1); custom `gradient_prompt` and `metaprompt` can be supplied in the config.
- `kind="metaprompt"`: meta-learning that analyzes examples and proposes a direct update in a single step; config takes `metaprompt`, `max_reflection_steps` (default 3) and `min_reflection_steps` (default 1).
- `kind="prompt_memory"`: one LLM call using a simple metaprompt to infer updates from conversation history; no extra configuration (the guide marks it as 1 LLM call).

The reference also lists `create_multi_prompt_optimizer` for optimizing several prompts together.

## Checked
Method: docs-checked 2026-11-09 against the LangMem guide (How to Optimize a Prompt, full) and the prompt_optimization reference (create_prompt_optimizer section read, lines 1730-1935 and grepped). Dropped the store-backed instruction pattern, gating workflow, failure-mode advice and the LangGraph memory concepts source (none of which were read or confirmed), plus the multi-agent attribution claim.
