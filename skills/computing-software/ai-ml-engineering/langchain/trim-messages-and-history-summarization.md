---
id: computing-software.ai-ml-engineering.langchain.trim-messages-and-history-summarization
name: trim-messages-and-history-summarization
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langgraph, memory, conversation-history, trim-messages, summarization, removemessage, context-window]
level: practitioner
status: verified
description: "Keep chat history inside a token budget with trim_messages (strategy, token counter, valid boundaries) and running summaries that replace old turns via RemoveMessage."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# trim_messages and history summarization

## Trim to a token budget
```python
from langchain_core.messages import trim_messages
from langchain_core.messages.utils import count_tokens_approximately
trimmed = trim_messages(
    state["messages"],
    strategy="last",                 # keep the most recent
    token_counter=count_tokens_approximately,   # or the chat model (exact but may call an API)
    max_tokens=8000,
    start_on="human",                # first kept non-system message is a human turn
    end_on=("human", "tool"),
    include_system=True,             # always keep the system message
    allow_partial=False,
)
response = llm.invoke(trimmed)
```
- `start_on="human"` avoids beginning with an orphaned AI or tool message (run: a 67-message history with tool calls trimmed to 19 messages, 280 approximate tokens, `system, human, ai, ...` and ending on a human turn); providers reject a `tool` result without its preceding `tool_use`.
- Passing a chat model as `token_counter` uses that model's own counting, which can be a network call for some providers (not run here, no API key); use `count_tokens_approximately` for hot paths and leave headroom.
- Trimming at call time (in the node, or a `pre_model_hook` / middleware) does not alter stored state; full history stays in the checkpointer.

## Summarize instead of dropping
```python
from langchain_core.messages import RemoveMessage, SystemMessage
def summarize(state):
    msgs = state["messages"]
    if count_tokens_approximately(msgs) < 12000:
        return {}
    old, recent = msgs[:-6], msgs[-6:]
    summary = llm.invoke([SystemMessage("Summarize the conversation so far: decisions, facts about the user, open tasks."),
                          *old]).text
    return {"summary": summary, "messages": [RemoveMessage(id=m.id) for m in old]}
```
Then prepend `SystemMessage(f"Conversation summary: {state['summary']}")` when calling the model. Make sure the cut point does not split a tool-call/tool-result pair. Ready-made: LangChain v1 `SummarizationMiddleware` for `create_agent`, `langmem.short_term.SummarizationNode` for LangGraph (import confirmed in langmem; also exports `RunningSummary`, `SummarizationResult`).

## Choosing
- Short support chats: trim.
- Long tasks where early decisions matter: summarize (and keep IDs, numbers, commitments verbatim in the summary prompt).
- Claude API apps not on LangChain can use server-side compaction instead.
- Rewriting history invalidates prompt-cache prefixes: summarize in large steps (at thresholds), not every turn.

## Verify
- [ ] Unit test with a 200-message history: output under budget, starts with system + human, no orphan tool messages.
- [ ] Eval questions referring to facts from early turns still pass after summarization.
