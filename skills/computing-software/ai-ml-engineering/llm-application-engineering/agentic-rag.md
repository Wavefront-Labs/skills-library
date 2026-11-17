---
id: computing-software.ai-ml-engineering.llm-application-engineering.agentic-rag
name: agentic-rag
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, agentic-rag, rag, retrieval-tool, multi-hop-retrieval, tool-use]
level: practitioner
status: docs-checked
description: "Build agentic RAG: retrieval exposed as tools, iterative and multi-hop search, query planning, stopping rules, citation tracking and when plain single-shot RAG is better."
sources:
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Agentic RAG (retrieval as a tool)

**Difference from classic RAG:** instead of always retrieving once before generation, the model decides whether, what and how many times to search, reformulating queries based on what it found.

## When it pays off
- Multi-hop questions ("compare policy X in 2024 vs 2025 for EU customers").
- Several sources (docs search, SQL, tickets API) where routing matters.
- Questions often answerable without retrieval (chit-chat, follow-ups).
Single-shot RAG is cheaper, faster and easier to evaluate for simple FAQ lookup; start there.

## Tool design
```python
tools = [
  {"name": "search_docs", "description": "Semantic + keyword search over product documentation. "
     "Use specific queries; call again with different wording if results are irrelevant. Returns a few passages with ids.",
   "input_schema": {"type": "object", "properties": {"query": {"type": "string"},
       "product": {"type": "string", "enum": ["core", "mobile", "api"]}}, "required": ["query"]}},
  {"name": "get_passage", "description": "Fetch full text of a passage by id when a snippet is cut off.",
   "input_schema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}},
]
```
Return compact results with ids, titles and short snippets; let the model fetch more when needed (keeps context small).

## Loop controls
- System prompt: when to search, to cite passage ids for every claim, and to stop and say so when evidence is missing.
- Caps: max tool calls, token budget; parallel searches for independent sub-questions.
- Track retrieved passage ids per turn for citation verification afterwards.

## Evaluation
Measure answer correctness, citation precision, number of searches per question (cost), and failure modes (looping, giving up early). Compare against single-shot RAG on the same set.

## Verify
- [ ] Per-question trace shows queries issued; average tool calls and latency within budget.

## Checked
2026-11-01. Confirmed against Anthropic's tool use overview (tools defined with name, description and `input_schema`; Claude decides when to call based on the description; parallel tool use) and Building effective agents (agent loop, stopping conditions). Removed: the LangGraph tutorial source (page empty when fetched) and the example caps and result counts.
Method: documentation only; no commands were run.
