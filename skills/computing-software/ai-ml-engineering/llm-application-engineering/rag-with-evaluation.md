---
id: computing-software.ai-ml-engineering.llm-application-engineering.rag-with-evaluation
name: rag-with-evaluation
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [rag, retrieval-augmented-generation, chunking, embeddings, vector-search, hybrid-search, bm25, reciprocal-rank-fusion, reranking, cross-encoder, grounded-generation, citations, eval-set, recall-at-k, mrr, faithfulness, groundedness, llm-as-judge, ragas, guardrails, prompt-injection, llm-application]
level: advanced
status: draft
description: "Build a RAG system that is measured, not guessed: chunking, hybrid BM25+vector retrieval, reranking, grounded prompts, an eval set with recall@k and faithfulness, guardrails and injection defence."
sources:
  - https://docs.ragas.io/
  - https://owasp.org/www-project-top-10-for-large-language-model-applications/
  - https://www.sbert.net/
  - https://docs.anthropic.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RAG with Evaluation — retrieval you can measure and answers you can trust

**Goal:** answer questions from your own documents with citations, and have numbers that tell you whether retrieval or generation is the weak link before every change ships.

## 1. Build the eval set first
Collect 50–200 realistic questions (from search logs, support tickets, domain experts), each with: the expected answer, the **ids of the chunks/documents that contain it**, and some questions whose answer is *not* in the corpus. Synthetic LLM-generated questions help coverage but skew easy; keep at least a core of real ones. Version this set; every pipeline change is judged against it.

## 2. Chunking
- Start around 300–800 tokens with 10–20% overlap; split on structure (headings, paragraphs, list items) before falling back to character counts.
- Prepend context the chunk loses when isolated: document title, section path, date. "It expires after 30 days" is useless without knowing *what* expires.
- Keep tables whole and keep code blocks intact.
- Store metadata (source, section, updated date, access-control group) for citations and filtering.
Changing the chunker or embedding model requires re-indexing and re-running the eval.

## 3. Hybrid retrieval and reranking
Dense embeddings miss exact identifiers (error codes, SKUs, names); BM25 misses paraphrases. Run both and fuse with **Reciprocal Rank Fusion**: `score = Σ 1 / (k + rank)`, with k = 60 conventionally. Retrieve ~20–50 candidates, then rerank with a cross-encoder (e.g. a sentence-transformers `CrossEncoder` or a hosted reranker) and keep the top 3–8 for the prompt. Apply metadata filters (tenant, permissions, date) **in the retrieval query**, never by asking the model to ignore documents — leaking another tenant's text is a security incident. Framework wiring: computing-software.ai-ml-engineering.langchain.retrieval-chains.

## 4. Grounded prompting
- Instruct: answer only from the provided context; cite chunk ids for every claim; say "I don't know" when the context is insufficient.
- Put retrieved text in clearly delimited blocks (e.g. XML-style tags with ids) and the instructions outside them.
- Order matters: models attend less to the middle of long contexts; fewer, better chunks beat stuffing 20.
- Post-check citations: every cited id must exist in the retrieved set; drop or flag answers citing nothing.

## 5. Measure retrieval and generation separately
**Retrieval** (no LLM needed): recall@k = share of questions where a gold chunk appears in the top k; MRR for rank quality. If recall@5 is 60%, no prompt can exceed that on answerable questions — fix retrieval first.
**Generation**:
- *Faithfulness/groundedness*: are all claims supported by the retrieved context?
- *Answer correctness* versus the expected answer.
- *Abstention*: rate of "don't know" on unanswerable questions (and false abstentions on answerable ones).
LLM-as-judge scoring (custom rubric, or libraries such as Ragas) scales this, but judges have biases: calibrate against 50+ human-labelled examples, use a strong judge model, keep its prompt fixed, and report agreement. Track latency and cost per query alongside quality. Wire the eval into CI so a regression in recall@k or faithfulness blocks the merge.

## 6. Guardrails and prompt injection
Retrieved documents and user input are **untrusted data**. A web page or uploaded PDF can contain "ignore previous instructions and ...". Defences, layered:
- Never give the model tools or permissions beyond what the user themselves could do; require confirmation for side-effecting actions.
- Mark retrieved content as data in the prompt and instruct the model not to follow instructions inside it — helpful, not sufficient alone.
- Validate outputs: schemas for structured output, allow-lists for URLs/actions, PII and secret scanning before display.
- Do not render model-produced markdown images/links to arbitrary domains (a data-exfiltration channel).
- Log prompts, retrieved ids and outputs for audit; red-team with injection examples in the eval set.
The OWASP Top 10 for LLM Applications is a good checklist.

## 7. In production
Log query, retrieved ids, scores and feedback. Monitor the share of "don't know" answers, low reranker scores and thumbs-down rates; sample failures weekly into the eval set. Re-index on document updates and remove deleted documents promptly.

## Verify
- [ ] A versioned eval set exists with gold chunk ids and unanswerable questions.
- [ ] recall@k is reported for the retriever alone, with and without hybrid search and reranking.
- [ ] Faithfulness and abstention are measured, and the LLM judge was checked against human labels.
- [ ] Permission filters are applied in the retrieval query and tested with a cross-tenant question.
- [ ] An injected instruction inside a test document does not change the system's actions.
- [ ] CI fails when recall@k or faithfulness drops below the agreed threshold.
