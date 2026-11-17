---
id: computing-software.ai-ml-engineering.langchain.langgraph-time-travel-and-update-state
name: langgraph-time-travel-and-update-state
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langgraph, langgraph-time-travel, update-state, get-state-history, checkpointer, replay]
level: practitioner
status: verified
description: "Inspect and rewind LangGraph runs: get_state and get_state_history, replay from a checkpoint_id, fork with update_state (as_node), and editing state to fix agent mistakes."
sources:
  - https://langchain-ai.github.io/langgraph/concepts/time-travel/
  - https://docs.langchain.com/oss/python/langgraph/use-time-travel
  - https://langchain-ai.github.io/langgraph/concepts/persistence/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Time travel: replay and update_state

**Requires:** a checkpointer (state saved after every super-step) and a `thread_id` in config.

## Inspect
```python
config = {"configurable": {"thread_id": "t-42"}}
snap = graph.get_state(config)              # latest StateSnapshot: values, next, config, metadata, tasks
for s in graph.get_state_history(config):   # newest first
    print(s.config["configurable"]["checkpoint_id"], s.next, s.metadata.get("step"))
```

## Replay from a past checkpoint
```python
past = next(s for s in graph.get_state_history(config) if s.next == ("tools",))
for event in graph.stream(None, past.config, stream_mode="updates"):   # input None = resume
    print(event)
```
Steps before the checkpoint are not re-executed; steps after it run again (run: replaying from the `next == ("tools",)` checkpoint ran only `tools` then `c`, and `snap._fields` is `values, next, config, metadata, created_at, parent_config, tasks, interrupts`).

## Fork with edited state
```python
new_cfg = graph.update_state(past.config, {"messages": [corrected_ai_message]}, as_node="agent")
graph.invoke(None, new_cfg)
```
- `update_state` creates a new checkpoint branching from the given one; history is preserved (run: history grew from 8 to 11 checkpoints after one fork and continuation).
- Updates go through the channel reducers: for `add_messages`, passing a message with the **same id** replaces it, a new id appends.
- `as_node` tells the graph which node the update pretends to come from, which determines what runs next.

## Uses
- Debugging: find the step where the agent went wrong, fix state, continue.
- Human review: edit a proposed tool call's arguments before execution (combined with interrupts).
- Evaluation: rerun from the same checkpoint with a new prompt/model to compare.

## Gotchas
- Side effects (emails sent, DB writes) in replayed nodes happen again; make tools idempotent or guard them.
- Checkpoint storage grows with history; prune old threads in production checkpointers.

## Verify
- [ ] Forked thread shows the edited message and a different continuation; original branch remains in history.
