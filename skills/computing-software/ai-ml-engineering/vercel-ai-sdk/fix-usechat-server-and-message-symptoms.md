---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.fix-usechat-server-and-message-symptoms
name: fix-usechat-server-and-message-symptoms
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [troubleshooting, usechat, convert-to-model-messages, onerror, stale-body, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Fix five useChat symptoms: parse-stream errors, no reply after tools, An error occurred, duplicated assistant messages, and stale body values."
sources:
  - https://ai-sdk.dev/docs/troubleshooting/use-chat-failed-to-parse-stream
  - https://ai-sdk.dev/docs/troubleshooting/use-chat-tools-no-response
  - https://ai-sdk.dev/docs/troubleshooting/use-chat-an-error-occurred
  - https://ai-sdk.dev/docs/troubleshooting/repeated-assistant-messages
  - https://ai-sdk.dev/docs/troubleshooting/use-chat-stale-body-data
  - https://ai-sdk.dev/docs/troubleshooting/abort-breaks-resumable-streams
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fix common useChat symptoms

Goal: map a symptom to its documented cause and one-line fix.

## "Failed to parse stream string. Invalid code"

`useChat` and `useCompletion` expect the stream data protocol. The error appears with an older SDK in the backend, a custom provider returning a plain text stream, or a raw LangChain stream result. If the backend really sends plain text, set `useChat({ streamProtocol: 'text' })`.

## Server logs show tool call and tool result but the model says nothing

Fix: convert the incoming UI messages to `ModelMessage` format with `messages: await convertToModelMessages(messages)` in `streamText`.

## "An error occurred"

`toUIMessageStream` masks error details by default so sensitive information is not leaked to the client. Pass `onError` to forward or log them, for example a handler returning `error.message` for `Error`, the string itself for strings, `'unknown error'` for null and `JSON.stringify(error)` otherwise. With `createUIMessageStream`, pass `onError` to it instead.

## Assistant messages duplicated, especially with tool calls

The UI message stream generates new message ids for each message. Pass `originalMessages: messages` to `toUIMessageStream` so existing ids are reused (the docs example also passes `generateMessageId: generateId` and an `onEnd: ({ messages }) => saveChat(...)`).

## Body values always stale

The hook-level `body` of `DefaultChatTransport` is captured when the hook initialises. Pass dynamic values in the second argument of `sendMessage({ text }, { body: { temperature, userId } })`; request-level options are evaluated per call and take precedence. If you need hook-level config, use a function (`body: () => ({ temperature: temperatureRef.current })`) and read component state through a `useRef`. The server reads them from `await req.json()`.

## Stop button with resume enabled

With `resume: true`, `stop()` only aborts the client request, and disconnects must stay resumable. Add a dedicated stop endpoint (load chat, read active stream id, save latest partial assistant message, cancel the producer, clear the active stream reference only if it still points to the same stream) and call it before `chat.stop()`. Never call it from unload or unmount cleanup. Without resumption use `resume: false` and plain `stop()`.

## Checked

Date: 2026-11-07. Read the 6 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Restated a diagnosis as a fix.

Method: documentation only; no commands were run.
