---
id: computing-software.ai-ml-engineering.langchain.langgraph-multi-agent-supervisor-and-handoffs
name: langgraph-multi-agent-supervisor-and-handoffs
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langgraph, multi-agent-supervisor, agent-handoffs, multi-agent, subagents-as-tools, langgraph-supervisor]
level: practitioner
status: docs-checked
description: "Choose multi-agent patterns in LangChain/LangGraph: subagents as tools, handoffs, skills, router; langgraph-supervisor options (output_mode, handoff tools); cost trade-offs."
sources:
  - https://docs.langchain.com/oss/python/langchain/multi-agent
  - https://github.com/langchain-ai/langgraph-supervisor-py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-agent patterns, supervisor and handoffs

**First question:** does one agent with the right tools and prompt do the job? The LangChain docs say a single agent often achieves similar results. Multi-agent is mainly for context management, distributed development across teams, and parallelisation; it also helps when one agent has too many tools and picks poorly, or needs sequential constraints.

## The five patterns (LangChain docs)
| Pattern | How it works |
| - | - |
| Subagents | A main agent coordinates subagents as tools; all routing passes through it |
| Handoffs | Tool calls update a state variable that switches the active agent or its tools/prompt |
| Skills | One agent stays in control and loads specialised prompts/knowledge on demand |
| Router | A routing step classifies input and sends it to one or more agents; results are synthesised |
| Custom workflow | Bespoke LangGraph flow mixing deterministic and agentic steps |

The docs' comparison (their illustrative scenarios, not benchmarks of your app):
- One-shot request ("buy coffee"): handoffs, skills and router take 3 model calls, subagents 4 (results flow back through the main agent; the price of centralised control).
- Repeat request: handoffs and skills drop to 2 calls on turn 2 (state or loaded skill persists); router stays at 3; subagents stay at 4 because they are stateless.
- Multi-domain compare (three ~2000-token domains): subagents and router run in parallel, about 9K tokens; handoffs run sequentially, 7+ calls and about 14K+ tokens; skills take 3 calls but about 15K tokens because loaded context accumulates.
- Patterns can be mixed (e.g. a subagent using skills).
- Core design idea per the docs: context engineering, deciding what each agent sees.

## Subagents as tools (illustrative sketch)
```python
from langchain.agents import create_agent
from langchain_core.tools import tool

research = create_agent(model="<model-id>", tools=[web_search], system_prompt="Research only.")

@tool
def ask_research(task: str) -> str:
    """Delegate a research question. Pass all needed context; the researcher sees only this."""
    r = research.invoke({"messages": [{"role": "user", "content": task}]})
    return r["messages"][-1].content

supervisor = create_agent(model="<model-id>", tools=[ask_research], system_prompt="Route work to specialists.")
```
The pattern follows the docs' description (subagents are stateless, start fresh each call); the code itself is a sketch, not copied from the docs.

## langgraph-supervisor library
- The README now recommends building the supervisor pattern directly with tools for most uses, because it gives more control over context engineering; the library stays for existing code (being made compatible with LangChain 1.0).
- `create_supervisor([agent_a, agent_b], model=..., prompt=...)` returns a `StateGraph`; call `.compile(checkpointer=..., store=...)` to add memory. Needs Python >= 3.10.
- Give each agent a `name`; the supervisor gets generated handoff tools named from them (prefix via `handoff_tool_prefix`, e.g. `delegate_to`).
- `output_mode="full_history"` includes workers' whole message history; `"last_message"` only the final response.
- `create_handoff_tool` passes the full supervisor message history plus a success tool message by default; `add_handoff_messages=False` omits the handoff messages. Custom handoff tools can add LLM-populated args such as a task description.
- A custom handoff returns `Command(goto=agent_name, graph=Command.PARENT, update={"messages": messages + [tool_message]})` using `InjectedState` and `InjectedToolCallId`; the ToolMessage answers the tool call.
- `create_forward_message_tool("supervisor")` gives a `forward_message` tool (arg `from_agent`) that sends a worker's last message straight to the output, saving supervisor tokens and avoiding paraphrase.
- Multi-level hierarchies: compile a supervisor with a `name` and pass it as an agent to a higher supervisor.

## Practical advice (author guidance, not on the pages)
- Cap delegation hops (recursion limit) and watch for ping-pong; use a stronger model for routing and cheaper workers.
- Evaluate routing accuracy separately from answer quality and compare tokens with a single-agent baseline.

## Checked
Method: 2026-11-08 read the LangChain multi-agent overview page and the langgraph-supervisor README in full (raw markdown). Removed the draft's `langgraph-swarm` mention and the old LangGraph concepts URLs (redirect to generic pages, unreadable). The subagent code sketch and last section are not from the sources.
