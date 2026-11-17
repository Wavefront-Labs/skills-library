---
id: computing-software.ai-ml-engineering.langchain.retrieval-chains
name: retrieval-chains
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, lcel, runnables, retrieval-chain, rag, retriever, vector-store, as-retriever, recursivecharactertextsplitter, chunking, langsmith, langgraph]
level: practitioner
status: docs-checked
description: "Build a retrieval chain in LangChain: split and index documents, make a retriever, compose LCEL runnables or a LangGraph sequence, and trace runs."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/tutorials/rag.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/concepts/lcel.mdx
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/vectorstore_retriever.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/recursive_text_splitter.ipynb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LangChain retrieval chains

**Goal:** a question-answering pipeline over your documents made of small, inspectable steps, with tracing.

## 1. Chunk and index
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
chunks = splitter.split_documents(docs)
vector_store.add_documents(chunks)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
```
- The v0.3 RAG tutorial uses `chunk_size=1000`, `chunk_overlap=200` and `add_start_index=True` (tracks the index in the original document). Chunk size is measured by `length_function`, which counts characters by default (`len`). The recursive splitter tries the separators `["\n\n", "\n", " ", ""]` in order until chunks are small enough.
- For token-based sizing, `RecursiveCharacterTextSplitter.from_tiktoken_encoder(...)` gives a hard size constraint by recursively re-splitting.
- `vectorstore.as_retriever()` builds a retriever. `search_type="mmr"` and `search_kwargs={"k": 1}` (the docs value) are supported options.
- RAG structure in the tutorial: indexing (load, split, store), then retrieval and generation at run time.

## 2. Compose
Two ways in the v0.3 docs:
- **LangGraph sequence** (tutorial): a `State` TypedDict with `question`, `context`, `answer`; a `retrieve` step calling `vector_store.similarity_search(state["question"])`; a `generate` step that fills a prompt with the joined document text; `StateGraph(State).add_sequence([retrieve, generate])` plus `add_edge(START, "retrieve")`. The tutorial's prompt pulled from the hub is `rlm/rag-prompt`; it tells the model to say it doesn't know when the context lacks the answer.
- **LCEL**: the `|` operator overloads to build a `RunnableSequence`; `RunnableParallel` runs several runnables concurrently on the same input and returns a dict with the same keys (a dict literal in a chain is shorthand for it). Runnables support invoke, batch and streaming, sync and async.
## 3. Tracing
Set `LANGSMITH_TRACING="true"` and `LANGSMITH_API_KEY` in the environment to trace runs in LangSmith; the tutorial recommends it for understanding the application as it grows. Check your data policy before sending production user data to a hosted tracer.

## Verify
- [ ] Chunks keep source metadata and the same embedding model is used at index and query time.
- [ ] `invoke` on a question with a known answer returns it.
- [ ] A question outside the corpus gets "I don't know" rather than an invented answer.
- [ ] A trace shows the retrieved chunks for each test query.

## Checked
Date: 2026-11-09.
- Confirmed in the v0.3 RAG tutorial, LCEL concepts, vectorstore retriever and recursive splitter docs: splitter parameters, separators, length function, tiktoken variant, as_retriever options, LangGraph sequence pattern, rag-prompt, LCEL composition primitives and the | operator, LangSmith environment variables.
- Removed as unconfirmed: the version-churn history (0.1 split, 0.2/0.3 deprecations, 1.x refocus), pin-everything advice, structured-output section and its reliability claims, the retriever | format_docs / RunnablePassthrough chain sketch and its missing-variable gotcha, RunnableParallel(...).assign and get_graph().print_ascii() tips, callbacks config keys, LlamaIndex and "when not to use LangChain" comparisons, OpenTelemetry options, the cross-reference to another skill, and the dead python.langchain.com, LangSmith and LlamaIndex source URLs.
Method: documentation only; no commands were run.
