---
id: computing-software.ai-ml-engineering.langchain.episodic-memory-few-shot-from-past-interactions
name: episodic-memory-few-shot-from-past-interactions
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, episodic-memory, few-shot, langgraph-store, long-term-memory, dynamic-few-shot]
level: practitioner
status: docs-checked
description: "Give agents episodic memory: store past interactions in a LangGraph store, retrieve similar ones by semantic search, and inject them as few-shot examples."
sources:
  - https://docs.langchain.com/oss/python/concepts/memory.md
  - https://docs.langchain.com/oss/python/langgraph/stores.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Episodic memory as few-shot examples

**Idea:** semantic memory stores facts; episodic memory stores experiences, often to help an agent remember how to accomplish a task. LangChain's memory concepts page notes that this is frequently implemented as few-shot examples retrieved from the store.

## Store episodes
Configure the store with an embedding index, then put episodes with the fields to embed.
```python
from langchain.embeddings import init_embeddings
from langgraph.store.memory import InMemoryStore

store = InMemoryStore(index={
    "embed": init_embeddings("openai:text-embedding-3-small"),
    "dims": 1536,
    "fields": ["input"],           # fields to embed
})
store.put(("episodes", user_id), str(uuid7()),
          {"input": task_input, "output": final_output, "score": score},
          index=["input"])          # embed only this field; index=False stores without embedding
```
`InMemoryStore` is for development; the stores page shows `PostgresStore.from_conn_string(DB_URI)` for persistence.

## Retrieve and inject
```python
async def call_model(state: MessagesState, runtime: Runtime[Context]):
    namespace = (runtime.context.user_id, "episodes")
    eps = await runtime.store.asearch(namespace, query=state["messages"][-1].content, limit=3)
    examples = "\n\n".join(f"Input: {e.value['input']}\nOutput: {e.value['output']}" for e in eps)
    # ... put examples in the system prompt and call the model
```
Compile the graph with `store=store` so nodes can reach it through `Runtime`. Use the same namespace tuple on put and search; the stores page keys memories by namespace such as `(user_id, "memories")`.

## Alternative
For more developer involvement or tighter ties to an evaluation harness, store the examples in a LangSmith Dataset and write your own retrieval logic to select the most relevant ones.

## Verify
- [ ] Search with a sample query and inspect the top 3 results for relevance.

## Checked
Method: docs-checked 2026-11-09 against the LangChain memory concepts page (episodic memory section) and the LangGraph stores page (semantic search, index fields, Runtime store usage). Dropped the feedback-score gating, curation, deduplication and PII advice, the SemanticSimilarityExampleSelector alternative and the dead langgraph and python.langchain.com sources, none of which were confirmed.
