---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.read-sources-and-citations-from-results
name: read-sources-and-citations-from-results
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [generate-text, sources, citations, web-search, inline-references]
level: advanced
status: docs-checked
description: "Read result.sources and text-part citations from search-grounded models, and render inline references without mis-slicing UTF-16 offsets."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/generating-text
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: surface the references behind a grounded answer, and render citations correctly.

## Sources
Some providers (Perplexity, Google, OpenAI Responses and Anthropic web search, OpenAI file search) return sources. With search tools:
```ts
const result = await generateText({
  model: 'google/gemini-3.8-flash',
  tools: { google_search: google.tools.googleSearch({}) },
  prompt: 'List the top 5 San Francisco news from the past week.',
});
for (const source of result.sources) {
  if (source.sourceType === 'url') console.log(source.id, source.title, source.url, source.providerMetadata);
}
```
A url source has `id`, `url`, optional `title`, `providerMetadata`. With `streamText`, watch `part.type === 'source' && part.sourceType === 'url'` in `result.stream`; also the `result.sources` promise. For OpenAI Responses and Anthropic web search, sources are the retrieved references and can exceed what the answer cites. OpenAI file-search results appear as document sources.

## Citations (inline references)
OpenAI Responses and Anthropic attach an optional `citations` array to each `text` content part; other providers may omit it (an omitted field does not mean the source list is complete). A `Citation` (exported from `ai`) has `source` (URL or document source; its id does not necessarily match an id in `result.sources`), optional `startIndex` and `endIndex` (end exclusive), and optional `citedText` (supporting passage from the source, not a range in the answer).
```ts
for (const part of result.content)
  if (part.type === 'text') for (const c of part.citations ?? []) console.log(c.source, c.startIndex, c.endIndex);
```
Streaming: citations arrive on `text-end` events (`part.id`, `part.citations`), on text parts of completed `result.content`, and survive `toUIMessageStream` as `TextUIPart.citations`.

## Rules for rendering
- Offsets follow the provider's character-indexing convention; JavaScript `slice()` uses UTF-16 code units, so convert when text contains emoji or non-BMP characters.
- If offsets are absent or unreliable, list references beside the text block instead of guessing.
- Keep query parameters and fragments in source URLs; several citations may point to one source at different locations.
- Anthropic supplies passages and document locations rather than output offsets; OpenAI file-search `index` values stay in provider metadata and are not text ranges.
- Citation fallback source events can arrive at the end of the provider stream.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
