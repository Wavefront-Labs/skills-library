---
id: computing-software.ai-ml-engineering.langchain.runnablewithmessagehistory-legacy-chat-history
name: runnablewithmessagehistory-legacy-chat-history
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, runnablewithmessagehistory, chat-history, session-history, lcel, legacy-migration]
level: practitioner
status: docs-checked
description: "Wrap an LCEL chain with RunnableWithMessageHistory: session factories, message keys, multi-key configs, and when to move to LangGraph persistence."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/libs/core/langchain_core/runnables/history.py
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/message_history.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/versions/migrating_memory/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RunnableWithMessageHistory (legacy chat history)

**Goal:** an existing LCEL chain remembers a conversation per session, and you know when this wrapper should give way to LangGraph persistence.

## Status
Since v0.3 LangChain recommends LangGraph persistence for new applications. Code already using `RunnableWithMessageHistory` or `BaseChatMessageHistory` needs no change: the migration guide says there is no plan to deprecate them in the near future and they are "sufficient for simple chat applications". The guide still encourages LangGraph for more complex use cases.

## Wiring
```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a support assistant."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
chain = prompt | llm

store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chat = RunnableWithMessageHistory(
    chain, get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)
chat.invoke({"question": "Reset my password"}, config={"configurable": {"session_id": "u42"}})
```
- The factory takes a `session_id` string by default, supplied through `config={"configurable": {"session_id": ...}}`.
- `input_messages_key`: required when the wrapped runnable takes a dict. `history_messages_key`: the dict key that receives history when the prompt has a separate placeholder. `output_messages_key`: required when the wrapped runnable returns a dict.

## Multi-key sessions
Pass `history_factory_config=[ConfigurableFieldSpec(id="user_id", annotation=str, name="User ID", default="", is_shared=True), ConfigurableFieldSpec(id="conversation_id", ...)]` (import `ConfigurableFieldSpec` from `langchain_core.runnables`), and make the factory take those arguments. Take `user_id` from the authenticated request, not from client-supplied JSON (this is a design rule, not from the docs).

## Migrating to LangGraph
The how-to shows wrapping a runnable in a minimal graph: `StateGraph(state_schema=MessagesState)` with one model node, compiled with a checkpointer (`MemorySaver` in the example; the docs say LangGraph persistence supports memory or backends such as SQLite, Postgres or Redis), invoked with `{"configurable": {"thread_id": ...}}`. State is read with `app.get_state(config).values` and edited with `app.update_state`. Use `Annotated[Sequence[BaseMessage], add_messages]` for a custom state that appends messages. Advantages listed by the docs: built-in multi-user and multi-conversation support, save and resume (error recovery, human intervention, time travel), compatibility with tool-calling chat models, custom state.

## Verify
- [ ] Two sessions with different ids do not see each other's messages.
- [ ] History survives a process restart (needs a durable history store or checkpointer).
- [ ] Long sessions are trimmed (see trim_messages) before the model call.

## Checked
Date: 2026-11-09.
- Confirmed in langchain_core runnables/history.py (v0.3): session_id default, key parameters and when each is required, ConfigurableFieldSpec history_factory_config. Confirmed in the v0.3 message_history how-to and migrating_memory page: recommendation, no-deprecation statement, MessagesState/MemorySaver/thread_id example, get_state/update_state, benefits list.
- Removed as unconfirmed: claude-sonnet-5-5 id, missing session_id "raises" claim, named Redis/Postgres/SQL chat-history classes and TTL/create_tables advice, the failure-modes section (unbounded growth, concurrent writes, streaming and aborted streams), InMemorySaver/PostgresSaver names, and copying old history into the first checkpoint.
Method: documentation only; no commands were run.
