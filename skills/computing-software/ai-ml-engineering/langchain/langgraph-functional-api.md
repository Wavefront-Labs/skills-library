---
id: computing-software.ai-ml-engineering.langchain.langgraph-functional-api
name: langgraph-functional-api
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langgraph, langgraph-functional-api, entrypoint, task, durable-execution, checkpointer]
level: practitioner
status: verified
description: "Write LangGraph workflows with the Functional API: @entrypoint and @task, futures for parallelism, checkpointed resume, interrupts and when to prefer StateGraph."
sources:
  - https://langchain-ai.github.io/langgraph/concepts/functional_api/
  - https://docs.langchain.com/oss/python/langgraph/functional-api
  - https://langchain-ai.github.io/langgraph/concepts/durable_execution/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LangGraph Functional API (@entrypoint / @task)

**Use when:** your workflow reads naturally as ordinary Python (loops, ifs) but you want LangGraph persistence, streaming, human-in-the-loop and durable resume without drawing a graph.

## Example
```python
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt

@task
def draft(topic: str) -> str:
    return llm.invoke(f"Write a short post about {topic}").content

@task
def critique(text: str) -> str:
    return llm.invoke(f"Critique this post:\n{text}").content

@entrypoint(checkpointer=InMemorySaver())
def write_post(topic: str) -> dict:
    futures = [draft(topic) for _ in range(3)]          # tasks run in parallel, return futures
    drafts = [f.result() for f in futures]
    best = drafts[0]
    review = critique(best).result()
    approved = interrupt({"draft": best, "review": review})   # pause for a human
    return {"post": best, "approved": approved}

cfg = {"configurable": {"thread_id": "p1"}}
write_post.invoke("vector databases", cfg)               # runs until interrupt
from langgraph.types import Command
write_post.invoke(Command(resume=True), cfg)              # resumes; finished tasks are NOT re-run
```

## Semantics
- `@task` results are checkpointed; on resume, completed tasks return saved results, so non-deterministic work is not repeated. Put side effects and LLM calls in tasks.
- Code in the entrypoint outside tasks re-runs on resume (run: the `parallel elapsed` print ran again in about 0 s because the 3 tasks were served from the checkpoint; the 3 parallel 0.2 s tasks took 0.2 s total), so keep it deterministic.
- `entrypoint.final(value=..., save=...)` returns one value and saves a different one; `previous` parameter gives the last saved value for the thread (memory across invocations).
- Inputs/outputs must be serializable by the checkpointer.

## StateGraph vs Functional
Graph API: explicit nodes/edges, visualization, fine-grained streaming of state channels, complex multi-agent topologies. Functional API: less boilerplate for linear or loop-heavy logic. They interoperate (call a graph from a task, or vice versa).

## Verify
- [ ] Kill the process after the interrupt, restart with a persistent checkpointer and resume: completed tasks are not re-executed (log calls).
