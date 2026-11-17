---
id: computing-software.ai-ml-engineering.langchain.agents-and-tool-calling
name: agents-and-tool-calling
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langgraph, agents, tool-calling, agentexecutor, react-agent, tool-binding, structured-tools, agent-loops, max-iterations, intermediate-steps, langsmith]
level: advanced
status: verified
description: "Build LangChain/LangGraph agents that call tools correctly: binding tools to a model, AgentExecutor vs LangGraph tradeoffs, iteration limits, and debugging intermediate steps."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://langchain-ai.github.io/langgraph/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LangChain/LangGraph agents and tool calling

**Goal:** wire an LLM to a set of tools using LangChain's abstractions without the version-churn confusion and silent-failure modes that are specific to this framework (see computing-software.ai-ml-engineering.llm-application-engineering.agentic-tool-use-and-orchestration for framework-agnostic agent-loop design).

## 1. Defining and binding tools
```python
from langchain_core.tools import tool

@tool
def lookup_order(order_id: str) -> str:
    """Look up an order by id and return its status and items."""
    ...

llm_with_tools = llm.bind_tools([lookup_order])
```
- The `@tool` decorator's **docstring becomes the tool description sent to the model** — treat it as production prompt content, not an internal comment. A vague docstring is the most common cause of wrong-tool-selection, same failure mode as raw API tool-use.
- Type hints on the function signature generate the JSON schema LangChain sends to the model — untyped or loosely typed (`def f(x)`) parameters produce a vague schema and the model guesses formats; use Pydantic models or typed args for anything beyond trivial strings.
- `bind_tools` returns a **new** runnable; the original `llm` object is unmodified. A common mistake is binding tools once, then calling the unbound `llm` elsewhere in the same codebase and wondering why tool calls never happen.

## 2. AgentExecutor vs LangGraph
- `AgentExecutor` (the older, higher-level abstraction; it is no longer in `langchain` 1.x, `from langchain.agents import AgentExecutor` raises ImportError, and lives in the `langchain-classic` package as `langchain_classic.agents.AgentExecutor`) hides the agent loop behind a single `.invoke()` call — fast to get started, but harder to customize mid-loop behavior (conditional branching, human-in-the-loop approval, custom retry logic) since the loop internals aren't yours to edit.
- **LangGraph** models the agent as an explicit state graph (nodes = steps, edges = transitions, including conditional edges) — more setup, but you own the loop: you can insert a human-approval node before a destructive tool call, persist/checkpoint state between turns (`checkpointer`), or run multiple agents as graph nodes. For anything beyond a simple single-agent loop in production, LangGraph's explicitness pays for itself; for a quick prototype, `AgentExecutor` or a plain `bind_tools` + manual loop is less ceremony.
- LangChain's agent APIs have **changed significantly across versions** (`initialize_agent` → `create_react_agent` → `langgraph.prebuilt.create_react_agent`, now documented as deprecated in favour of `langchain.agents.create_agent`) — pin the LangChain version in requirements and check the current docs against that pinned version; code copied from an older tutorial against a newer install (or vice versa) is a frequent source of import errors and silently different default behavior (e.g. different default max iterations).

## 3. Debugging and guardrails specific to this framework
- `AgentExecutor(..., return_intermediate_steps=True)` (default `False`) gives you every (action, observation) pair from the run — inspect this before assuming a wrong final answer is a reasoning failure; it's frequently a tool returning an unexpected format the model then misreads.
- `max_iterations` (default 15) and `max_execution_time` (default `None`, no time cap) on `AgentExecutor` (langchain-classic 1.0.8, read from the model fields) are the loop caps; set both explicitly for anything user-facing. For LangGraph/`create_agent` the cap is the `recursion_limit` config, whose default is 10007 in langgraph 1.2.16 (`LANGGRAPH_DEFAULT_RECURSION_LIMIT`), so set it explicitly, e.g. `agent.invoke(inp, {"recursion_limit": 25})`.
- Use **LangSmith** (or at minimum, structured logging of each tool call/result) in any non-trivial agent — reasoning through a multi-step agent failure from final output alone is far slower than reading the actual trace of what was called with what arguments and what came back.
- Parsing errors (the model emits a tool call LangChain's output parser can't match to a registered tool, usually from an older string-based ReAct-style agent rather than native tool-calling) show up as a generic `OutputParserException` — prefer models/wiring that use the provider's **native tool-calling** (`bind_tools` with a tool-calling-capable model) over older ReAct text-parsing agents, since native tool calls are schema-enforced and don't depend on the model emitting an exact string format.

## Verify
- [ ] Tool docstrings reviewed as prompt content; each is specific about what the tool does and does not do.
- [ ] Tool argument types are explicit (Pydantic/typed), not loose strings for structured data.
- [ ] `max_iterations`/`max_execution_time` (or the LangGraph equivalent) set explicitly, not left at framework defaults, for any user-facing agent.
- [ ] Intermediate steps/trace are logged (LangSmith or equivalent) and were actually inspected when debugging a wrong agent output.
- [ ] Native tool-calling is used instead of string-based ReAct parsing where the model supports it.
- [ ] LangChain version is pinned and matches the API patterns actually used in the code.
