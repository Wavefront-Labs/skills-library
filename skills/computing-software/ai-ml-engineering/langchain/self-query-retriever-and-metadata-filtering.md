---
id: computing-software.ai-ml-engineering.langchain.self-query-retriever-and-metadata-filtering
name: self-query-retriever-and-metadata-filtering
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, retriever, vector-store, self-query-retriever, metadata-filtering, structured-query]
level: practitioner
status: docs-checked
description: "Combine semantic search with metadata filters: SelfQueryRetriever where an LLM builds filters from the question, and why tenant scoping stays in your code."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/self_query.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/vectorstore_retriever.ipynb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-query and metadata filtering

## Explicit filters (do this for anything security-relevant)
`vectorstore.as_retriever(search_kwargs={...})` passes parameters to the underlying vector store search methods (the docs show `{"k": 1}` and `{"score_threshold": 0.5}`). Filter syntax is specific to each vector store, so check your store's integration page for how to pass a filter, and wrap filter construction in one tested function per store.

Design rule (not from the docs): tenant and ACL filters are applied by your code from the authenticated identity, never inferred by a model.

## SelfQueryRetriever - LLM extracts filters from the question
A query-constructing LLM chain writes a structured query (a text query plus a metadata filter) which is applied to the vector store, so the retriever filters on metadata as well as comparing semantics.
```python
from langchain.chains.query_constructor.schema import AttributeInfo      # v0.3 import paths
from langchain.retrievers.self_query.base import SelfQueryRetriever
fields = [AttributeInfo(name="genre", description="The genre of the movie. One of ['science fiction', 'comedy', 'drama']", type="string"),
          AttributeInfo(name="year", description="The year the movie was released", type="integer"),
          AttributeInfo(name="rating", description="A 1-10 rating for the movie", type="float")]
retriever = SelfQueryRetriever.from_llm(llm, vectorstore, "Brief summary of a movie", fields, enable_limit=True)
retriever.invoke("What's a highly rated (above 8.5) science fiction film?")
```
- Needs the `lark` package. The docs demo uses Chroma; the vector store needs a built-in structured-query translator (list on the integrations page for self-querying).
- Provide each attribute's `name`, `description` and `type`; put allowed values in the description (the docs list the genre values there).
- `enable_limit=True` lets the question set `k` ("What are two movies about dinosaurs").
- Under the hood: `get_query_constructor_prompt(...) | llm | StructuredQueryOutputParser.from_components()` gives a `StructuredQuery` with `query`, `filter` and `limit`. The prompt lists comparators `eq ne gt gte lt lte contain like in nin` and operators `and or not`, requires `YYYY-MM-DD` for dates and returns `NO_FILTER` when no filter applies.
- Translating to the store: pass `structured_query_translator=` (for example `ChromaTranslator()` from `langchain_community.query_constructors.chroma`) to build `SelfQueryRetriever(query_constructor=..., vectorstore=..., structured_query_translator=...)`.
- The docs say the query constructor is the key element: tune the prompt, its examples and attribute descriptions. Always inspect the generated `StructuredQuery` when results look wrong.

## Verify
- [ ] Eval set of filter-bearing questions checks extracted filters field by field.
- [ ] A question mentioning another tenant's name still only returns the caller's tenant documents (tenant filter applied by your code).

## Checked
Date: 2026-11-09.
- Confirmed in the v0.3 self_query and vectorstore_retriever how-tos: mechanism, lark requirement, AttributeInfo fields, enable_limit, query-constructor prompt contents, StructuredQuery shape, translator argument, search_kwargs.
- Removed as unconfirmed: store-by-store filter syntax claims (Mongo-like operators, Qdrant models.Filter, Pinecone DSL), the langchain_classic import path, the list of supported stores beyond Chroma, "wrong filters return zero results silently", the AND-a-tenant-constraint wrapper recipe and the with_structured_output alternative.
Method: documentation only; no commands were run.
