---
id: computing-software.ai-ml-engineering.langchain.memory-and-conversation-state
name: memory-and-conversation-state
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langgraph, memory, conversation-history, chat-history, summarization, checkpointer, persistence, token-budget, context-window, session-state, buffer-memory]
level: practitioner
status: docs-checked
description: "Manage LangChain/LangGraph conversation memory: message passing, checkpointer persistence by thread_id, trimming and summary patterns, legacy memory classes."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/chatbots_memory.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/versions/migrating_memory/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conversation memory and state in LangChain / LangGraph

**Goal:** keep a multi-turn conversation coherent across turns without the history growing past the context window or distracting the model.

## 1. What replaced the old Memory classes
- As of v0.3 LangChain recommends LangGraph persistence for memory in new applications. Most LangChain 0.0.x memory classes (`ConversationBufferMemory`, `ConversationSummaryMemory`, etc.) were officially deprecated in 0.3.x. The migration page has per-class guides (buffer, buffer window and token buffer, summary and summary buffer); `VectorStoreRetrieverMemory` and the entity memories point to the long-term memory agent tutorial.
- Existing `RunnableWithMessageHistory` / `BaseChatMessageHistory` code needs no change; the docs do not plan to deprecate them soon.
- Why LangGraph: built-in multi-user and multi-conversation support, save and resume (error recovery, human intervention, time travel), custom state, compatibility with tool-calling chat models.

## 2. Techniques from the how-to
1. **Message passing**: put prior messages in a `MessagesPlaceholder` and pass them each call. Fine, but you manage the list yourself.
2. **Checkpointer**: `StateGraph(state_schema=MessagesState)` with a `model` node, compiled with `checkpointer=MemorySaver()`. Pass only the new message and `config={"configurable": {"thread_id": "1"}}`; the graph keeps history. A different `thread_id` starts separate state, so choose the id to match the conversation boundary (for example one per user conversation).
3. **Trimming**: `trim_messages(strategy="last", max_tokens=2, token_counter=len)` counts each message as one "token" and keeps the last two; the docs example shows the model then forgetting a name given earlier. Apply it inside the model node before calling the model.
4. **Summary memory**: in the model node, once the history reaches a size (4 messages in the example), call the model to "distill the above chat messages into a single summary message", delete old messages with `RemoveMessage(id=m.id)`, and re-add the latest human message. History then accumulates again until the threshold and another summary is made from the earlier summary plus new messages. Whether detail survives a summary is not guaranteed; test on long conversations.

## 3. Choosing
Full buffer is simplest but grows each turn; trimming bounds cost but forgets anything outside the window; summaries preserve older facts at the cost of an extra model call and possible detail loss. Pick based on measured conversation length and what must persist (design guidance).

## Verify
- [ ] Strategy chosen from measured typical and worst-case conversation length.
- [ ] `thread_id` granularity matches the real conversation boundary.
- [ ] Summary logic tested on a conversation long enough to cross the threshold at least twice.
- [ ] Persistence tested across a process restart with a durable checkpointer (`MemorySaver` is in-process).

## Checked
Date: 2026-11-09.
- Confirmed in the v0.3 chatbots_memory how-to and migrating_memory page: recommendation and deprecation statements, checkpointer/thread_id pattern, trim_messages example and outcome, summary-with-RemoveMessage example and accumulation note, migration table mapping.
- Removed as unconfirmed: Postgres/SQLite checkpointer names, retrieval-based memory advice and the cross-reference to another skill, the failure-modes section (linear cost growth, summary-of-summary drift, prompt/state version mismatch), and the claim that old classes are deprecated "in current versions" beyond 0.3.x.
Method: documentation only; no commands were run.
