---
id: computing-software.ai-ml-engineering.langchain.document-loaders-and-metadata
name: document-loaders-and-metadata
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, retriever, document-loaders, text-splitter, metadata, ingestion, rag]
level: practitioner
status: docs-checked
description: "Load PDFs and directories into LangChain Documents with lazy loading, and split Markdown by headers or text by size while keeping metadata for citations."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/document_loader_pdf.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/document_loader_directory.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/recursive_text_splitter.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/markdown_header_metadata_splitter.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/tutorials/rag.ipynb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Document loaders and metadata

**Goal:** turn raw sources into `Document(page_content, metadata)` objects whose metadata is good enough to cite and filter.

## Loading
```python
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
pages = []
async for page in PyPDFLoader("handbook.pdf").alazy_load():
    pages.append(page)                       # one Document per page; metadata has source and page
loader = DirectoryLoader("docs/", glob="**/*.md", loader_cls=TextLoader, show_progress=True, use_multithreading=True)
docs = loader.load()
```
- Loaders implement `lazy_load` and async `alazy_load`, which return iterators of `Document` objects, so you can stream rather than hold everything.
- PDF loader metadata stores the source path and page number (the docs example shows `{'source': ..., 'page': 0}`).
- LangChain integrates many PDF parsers: some are simple and low-level, others support OCR and image processing or layout analysis. Choose by need. For PDFs with complex layouts, diagrams or scans the docs suggest it can be better to skip parsing and pass page images to a multimodal model.
- `DirectoryLoader`: `glob` selects files; `loader_cls` defaults to `UnstructuredLoader` and can be changed (for example `TextLoader`); progress bar needs `tqdm` and `show_progress=True`; `use_multithreading=True` uses several threads (default is one); the docs also show handling files with differing text encodings.

## Metadata
Documents carry a `metadata` dict; loaders fill in source (and page for PDFs). Add your own fields at load time, before splitting, so every chunk inherits them (for example tenant or updated date). Enforce access fields in code, not through a model (design guidance, not from the docs).

## Splitting while keeping provenance
```python
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
chunks = splitter.split_documents(docs)
```
- `add_start_index=True` tracks the index of each chunk in the original document (used in the v0.3 RAG tutorial). The size is in characters by default (`length_function`).
- `chunk_overlap` is the target overlap between chunks and mitigates losing information when context is divided.
- `MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "Header 1"), ("##", "Header 2")])` splits Markdown by headers and records the headers in each chunk's metadata, for example `{'Header 1': 'Foo', 'Header 2': 'Bar'}`.

## Verify
- [ ] Count of empty or very short Documents after loading is near zero (scanned pages).
- [ ] A random chunk shows source, page or header path, and start index sufficient to cite it.

## Checked
Date: 2026-11-09.
- Confirmed in the v0.3 PDF, directory, recursive splitter, Markdown header splitter and RAG tutorial docs: lazy/async loading, PDF metadata, parser range and multimodal alternative, DirectoryLoader options, splitter parameters and add_start_index, header metadata output.
- Removed as unconfirmed: "PyPDF returns empty strings for scanned PDFs", UnstructuredLoader strategy="hi_res" OCR advice, WebBaseLoader and JavaScript claims, TextLoader encoding kwargs, the source/source_id_key link to the indexing API, claim that vector stores reject nested metadata, the stable doc_id check, `from_tiktoken_encoder` details for this skill, and the dead python.langchain.com source URLs.
Method: documentation only; no commands were run.
