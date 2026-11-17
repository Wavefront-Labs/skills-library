---
id: computing-software.ai-ml-engineering.langchain.langgraph-interrupt-human-in-the-loop
name: langgraph-interrupt-human-in-the-loop
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langgraph, human-in-the-loop, interrupt, command-resume, approval-gates, checkpointer]
level: practitioner
status: verified
description: "Pause a LangGraph run for human approval or edits with interrupt() and resume it with Command(resume=...), including checkpointer requirements and node re-execution pitfalls."
sources:
  - https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/
  - https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Human-in-the-loop with interrupt and Command

## Pattern
```python
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

def approve_refund(state):
    decision = interrupt({"action": "refund", "amount": state["amount"], "order": state["order_id"]})
    if decision["approved"]:
        return {"status": "approved", "amount": decision.get("amount", state["amount"])}
    return Command(goto="notify_rejected")

app = builder.compile(checkpointer=InMemorySaver())        # persistent saver in production
cfg = {"configurable": {"thread_id": "ticket-4812"}}
out = app.invoke({"order_id": "A1", "amount": 120}, cfg)
out["__interrupt__"]                                       # payload shown to the reviewer
app.invoke(Command(resume={"approved": True, "amount": 100}), cfg)
```
- A checkpointer and a stable `thread_id` are mandatory; the run's state is saved at the interrupt and loaded on resume, possibly in another process hours later.
- The interrupt payload must be JSON-serialisable; it is what your UI renders.

## The re-execution rule
On resume the **whole node runs again from the top**; `interrupt()` then returns the resume value instead of pausing. Consequences:
- Side effects before `interrupt()` (API calls, emails, DB writes) run twice (run: a list append before `interrupt()` ran on both the first call and the resume). Put interrupts first in the node, or move side effects into a following node.
- Several `interrupt()` calls in one node are matched to resume values by order; do not make their number or order conditional on non-deterministic data.
- Do not catch the exception `interrupt()` raises with a bare `except Exception` - it swallows the pause (run: `GraphInterrupt` subclasses `Exception`, and the node returned the fallback value instead of pausing).

## Common gates
- Approve/reject a tool call before execution (wrap the tool or put an approval node before `tools`).
- Edit state: return the reviewer's edited values as the update.
- Collect missing input from the user mid-run.
LangChain v1 `create_agent` offers `HumanInTheLoopMiddleware(interrupt_on={"send_email": True})` for tool-level approval without hand-wiring.

Static breakpoints (`compile(interrupt_before=["tools"])`) are for debugging; use `interrupt()` for product flows.

## Verify
- [ ] Test: invoke -> assert `__interrupt__` -> resume in a fresh app instance with the same checkpointer -> expected final state.
- [ ] Side effects counted once across interrupt + resume.
- [ ] Abandoned threads expire or are cleaned up (checkpoint retention policy).
