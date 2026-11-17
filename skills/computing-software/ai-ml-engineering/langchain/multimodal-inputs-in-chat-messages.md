---
id: computing-software.ai-ml-engineering.langchain.multimodal-inputs-in-chat-messages
name: multimodal-inputs-in-chat-messages
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, multimodal-messages, content-blocks, image-input, pdf-input, chat-models, vision]
level: practitioner
status: docs-checked
description: "Send images, PDFs and audio to chat models through LangChain content blocks: base64 vs URL sources, provider-specific fields such as filename and citations."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/multimodal_inputs.ipynb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multimodal inputs in chat messages

LangChain accepts multimodal input either in provider-specific formats or in a cross-provider standard block format (shown here, from the v0.3 how-to). Most chat models that take image input also accept OpenAI's Chat Completions form `{"type": "image_url", "image_url": {"url": image_url}}`. See each chat model integration page for native formats.

## Images
```python
import base64, httpx
from langchain.chat_models import init_chat_model

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")   # model id from the docs example; use a current one
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
message = {"role": "user", "content": [
    {"type": "text", "text": "Describe the weather in this image:"},
    {"type": "image", "source_type": "base64", "data": image_data, "mime_type": "image/jpeg"},
]}
response = llm.invoke([message])
print(response.text())
```
- Base64 block: `type: image`, `source_type: base64`, `mime_type` (image/jpeg, image/png...), `data`.
- URL block: `{"type": "image", "source_type": "url", "url": "https://..."}`. Docs name OpenAI, Anthropic and Google Gemini as accepting image URLs; many providers only take base64.
- Several images can go in one message as separate blocks.

## Documents (PDF)
- Base64: `{"type": "file", "source_type": "base64", "mime_type": "application/pdf", "data": ...}`. The docs name OpenAI, Anthropic and Google Gemini as accepting PDFs.
- URL: `{"type": "file", "source_type": "url", "url": ...}`; the docs say specifically Anthropic accepts document URLs.
- OpenAI requires a file name: add `"filename": "my-file"` to the block.

## Audio
`{"type": "audio", "source_type": "base64", "mime_type": "audio/wav", "data": ...}`. The docs name OpenAI and Google Gemini as accepting audio.

## Provider-specific fields
Put extra fields directly on the content block, or use the provider's native format.
- Anthropic prompt caching: add `"cache_control": {"type": "ephemeral"}` to a block. In the docs example the first call showed `cache_creation` and the follow-up call `cache_read` in `usage_metadata["input_token_details"]`.
- Anthropic citations on a PDF block: `"citations": {"enabled": True}`; the response content then holds blocks with `citations`.

## Tool calls
Bind tools as usual (`llm.bind_tools([...])`) and invoke with a message containing image or other blocks; the model can return `tool_calls`.

## Verify
- [ ] The chosen model and provider actually support the block type (image URL, PDF, audio); check its integration page.
- [ ] `response.usage_metadata` token counts for an image request are within budget.
- [ ] Extraction accuracy evaluated on a labeled sample of real documents.

## Checked
Date: 2026-11-09.
- Confirmed in the v0.3 multimodal_inputs how-to notebook: block shapes for image, file and audio (base64 and URL), the OpenAI image_url compatibility note, provider support lists, OpenAI filename requirement, cache_control and citations examples, tool-call example.
- Removed as unconfirmed: the claude-sonnet-5-5 id, the ChatPromptTemplate-with-image example, provider image size/count caps and token-proportional-to-pixels claims, the "image before question" advice, "errors appear only at request time", and the claim that newer versions accept a flat base64 block form. The docs.claude.com vision source was dropped (not read this batch).
Method: documentation only; no commands were run.
