---
id: computing-software.ai-ml-engineering.langchain.parent-document-and-multivector-retrievers
name: parent-document-and-multivector-retrievers
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, retriever, vector-store, parentdocumentretriever, multivectorretriever, small-to-big-retrieval]
level: practitioner
status: verified
description: "Retrieve small precise chunks but return larger parent context with ParentDocumentRetriever, or index summaries / hypothetical questions per document with MultiVectorRetriever."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ParentDocumentRetriever and MultiVectorRetriever

**Problem:** small chunks embed precisely but lack context; big chunks give context but embed vaguely. Search small, return big.

## ParentDocumentRetriever
```python
from langchain_classic.retrievers import ParentDocumentRetriever        # langchain<1.0: langchain.retrievers
from langchain_classic.storage import LocalFileStore, create_kv_docstore
retriever = ParentDocumentRetriever(
    vectorstore=vs,                                          # stores child chunks
    docstore=create_kv_docstore(LocalFileStore("./parents")), # stores parents by id
    child_splitter=RecursiveCharacterTextSplitter(chunk_size=400),
    parent_splitter=RecursiveCharacterTextSplitter(chunk_size=2000),   # omit to return whole documents
)
retriever.add_documents(docs)              # splits, embeds children, stores parents
retriever.invoke("how do refunds work?")   # returns parent chunks, de-duplicated (run: 2 parents, each under the 1200-char parent size)
```
- `InMemoryStore` is lost on restart - production needs a persistent docstore (Redis, SQL, file/object store) sharing ids with the vector store.
- Child metadata carries `doc_id` (`id_key`, default `"doc_id"`; run); deleting a document means deleting children by that id and the parent key.
- Returned parents count toward the context budget: k=4 children can mean 4 x 2000-char parents.

## MultiVectorRetriever - custom representations
Index summaries, hypothetical questions or table descriptions, return the original:
```python
from langchain_classic.retrievers.multi_vector import MultiVectorRetriever, SearchType
retriever = MultiVectorRetriever(vectorstore=vs, byte_store=store, id_key="doc_id", search_type=SearchType.mmr)
ids = [str(uuid4()) for _ in docs]
summaries = (summary_prompt | llm | StrOutputParser()).batch([d.page_content for d in docs], {"max_concurrency": 8})
vs.add_documents([Document(page_content=s, metadata={"doc_id": i}) for s, i in zip(summaries, ids)])
retriever.docstore.mset(list(zip(ids, docs)))
```
Good for tables/images (embed an LLM-written description, return the raw table or image reference) and for long documents where questions do not resemble the prose.

## Gotchas
- Summary generation is an LLM cost per document and must be re-run when the document changes - tie it into incremental indexing.
- Hypothetical-question indexing can over-match generic queries; evaluate recall@k vs plain chunking on your eval set before adopting.

## Verify
- [ ] Retriever returns parents whose text contains the matched child.
- [ ] Restarting the service keeps retrieval working (docstore persisted).
- [ ] recall@k / answer quality measured against baseline chunking.
