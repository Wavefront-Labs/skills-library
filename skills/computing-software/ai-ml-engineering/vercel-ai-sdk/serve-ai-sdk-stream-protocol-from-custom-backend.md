---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.serve-ai-sdk-stream-protocol-from-custom-backend
name: serve-ai-sdk-stream-protocol-from-custom-backend
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [stream-protocol, sse, text-stream, data-stream, custom-backend, vercel-ai-sdk]
level: advanced
status: docs-checked
description: "Choose the text or UI message (data) stream protocol and emit correct SSE chunks, header and DONE marker so useChat works with a non-AI-SDK backend."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serve the AI SDK stream protocol from a custom backend

Goal: make `useChat`/`useCompletion` work against a backend you control (for example Python), or pick the simpler text protocol.

## Text stream protocol

Plain text chunks appended into one response. Supported by `useChat` (via `TextStreamChatTransport({ api })`), `useCompletion` (`streamProtocol: 'text'`) and `useObject`. Server: `createTextStreamResponse({ stream: toTextStream({ stream: result.stream }) })`. Only basic text; no tool calls.

## Data (UI message) stream protocol

Server-Sent Events, each `data: {json}` followed by a blank line. A custom backend must send the header `x-vercel-ai-ui-message-stream: v1`. From the SDK: `createUIMessageStreamResponse({ stream: toUIMessageStream({ stream: result.stream }) })`.

Chunk types:

- `{"type":"start","messageId":"..."}`
- text: `text-start` / `text-delta` (`id`, `delta`) / `text-end`, using the same `id` for one block
- reasoning: `reasoning-start` / `reasoning-delta` / `reasoning-end`; `reasoning-file` (`url`, `mediaType`)
- `source-url` (`sourceId`, `url`), `source-document` (`sourceId`, `mediaType`, `title`), `file` (`url`, `mediaType`), `custom` (`kind` like `openai.compaction`), `data-<name>` (`data`)
- tools: `tool-input-start` (`toolCallId`, `toolName`, optional `inputEncoding` of `json` or `text`; use `text` for raw code/HTML), `tool-input-delta` (`inputTextDelta`), `tool-input-available` (`input`), `tool-output-available` (`output`), `tool-output-denied`
- approvals: `tool-approval-request` (`approvalId`, optional `approvalDescriptor`, `reason`; omitted `isAutomatic` means the client must respond), `tool-approval-response` (`approvalId`, `approved`, `reason`, optional `providerExecuted`)
- steps: `start-step`, `finish-step` (needed to stitch multi-step assistant calls), `reset-step` (drops parts since the last `start-step`, for retried steps)
- `{"type":"error","errorText":"..."}`, `{"type":"finish"}`, `{"type":"abort","reason":"..."}`
- terminator: `data: [DONE]`

`useCompletion` only understands text and data parts.

## Gotchas

- Custom backends must set the `x-vercel-ai-ui-message-stream: v1` header.
- `finish-step` is required to correctly process multiple stitched assistant calls (multi-step tools with steps in `useChat`).
- FastAPI example lives in the AI SDK repo (`examples/next-fastapi`).

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the UI_MESSAGE_STREAM_HEADERS remark (not on the page) and the "typical order" claim.

Method: documentation only; no commands were run.
