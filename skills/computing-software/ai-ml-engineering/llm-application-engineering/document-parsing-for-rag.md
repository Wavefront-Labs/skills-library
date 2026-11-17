---
id: computing-software.ai-ml-engineering.llm-application-engineering.document-parsing-for-rag
name: document-parsing-for-rag
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, document-parsing, rag, pdf-parsing, table-extraction, ocr, chunking]
level: practitioner
status: draft
description: "Parse PDFs, tables and scanned docs for RAG: choosing parsers (pypdf, PyMuPDF, Docling, Unstructured, OCR, VLMs), layout and table handling, metadata and parse-quality checks."
sources:
  - https://docling-project.github.io/docling/
  - https://docs.unstructured.io/open-source/introduction/overview
  - https://docs.claude.com/en/docs/build-with-claude/pdf-support
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Document parsing for RAG

**Garbage in, garbage retrieved.** Broken reading order, merged columns, lost tables and OCR noise cap RAG quality no matter how good the embeddings are.

## Choosing a parser
| Document type | Approach |
|---|---|
| Born-digital PDFs, simple layout | PyMuPDF (`fitz`) or pypdf text extraction: fast, cheap |
| Multi-column, headers/footers, tables | layout-aware parsers: Docling, Unstructured (`hi_res`), Marker, Azure Document Intelligence / AWS Textract |
| Scanned / image PDFs | OCR (Tesseract, PaddleOCR, cloud OCR) or layout models with OCR |
| Charts, complex visuals, forms | vision-language model per page (e.g. send PDF pages to Claude with PDF support) to transcribe into Markdown |
| HTML/DOCX/PPTX | native structure parsers (keep headings, lists, tables) |

## Docling example
```python
from docling.document_converter import DocumentConverter
doc = DocumentConverter().convert("report.pdf").document
markdown = doc.export_to_markdown()        # headings, lists, tables as Markdown
```

## Practices
- Convert to Markdown that preserves headings; chunk by section, prefixing each chunk with its heading path ("Policy > Refunds > Exceptions").
- Tables: keep whole tables in one chunk (or row groups with repeated headers); also store a natural-language summary for retrieval.
- Strip repeated headers/footers and page numbers; keep page numbers as metadata for citations.
- Store metadata: source URI, title, page, section, version/date, access-control groups.
- Cache parse results keyed by file hash; parsing with VLMs/OCR is the expensive step.

## Quality checks
- Sample 20-50 pages and diff parser output against the visual page; count reading-order errors and lost tables.
- Track empty or near-empty pages (OCR needed) and garbled character ratios.
- Re-run retrieval evals when switching parsers.

## Verify
- [ ] Retrieval recall on table- and layout-heavy questions measured per parser option.
