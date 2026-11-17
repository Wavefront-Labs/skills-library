---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.edit-regenerate-and-validate-usechat-messages
name: edit-regenerate-and-validate-usechat-messages
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [chatbot, usechat, sendmessage, regenerate, shared-chat, datapartschemas, vercel-ai-sdk]
level: advanced
status: docs-checked
description: "Use useChat controls beyond send: edit a message by id, regenerate a specific message, clear errors, optimistic setMessages, shared Chat instances and schema validation."
sources:
  - https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-chat
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Edit, regenerate and validate messages with useChat

Goal: use the precise `useChat` reference semantics for editing and retrying turns, and understand React snapshot behaviour.

## Returns and what they do

- `sendMessage(message?, options?)`: `message` is `{ text, files?, metadata?, messageId? }` or a `CreateUIMessage`. Passing `messageId` replaces that message (editing). When replacing with a `CreateUIMessage`, supply its `id` to assign a new id. Calling with no message resubmits the current messages (useful after adding tool outputs). `options` (`ChatRequestOptions`): `headers`, `body`, `metadata`.
- `regenerate({ messageId?, headers?, body?, metadata? })`: regenerates the last assistant message, or a specific one.
- `stop()` aborts streaming; `clearError()` resets `error`; `resumeStream()` resumes an interrupted stream after a network error.
- `setMessages(array | updater)`: local update, no API call (optimistic updates). A functional updater receives the Chat's latest messages, which may be newer than the render's.
- `addToolOutput({ tool, toolCallId, output })` or `{ tool, toolCallId, state: 'output-error', errorText }`; `addToolResult` is deprecated. `addToolApprovalResponse({ id, approved, reason? })`.
- `status`: `submitted | streaming | ready | error`; `id`; `messages` (each with `id`, `role`, `parts`, `metadata`).

## Hook parameters worth knowing

`chat` (existing `Chat<UIMessage>` instance; other params then ignored), `transport` (default `DefaultChatTransport` at `/api/chat`), `id` (random if omitted), `messages` (initial), `messageMetadataSchema` and `dataPartSchemas` (validate metadata and data parts), `generateId`, `onToolCall`, `sendAutomaticallyWhen`, `onFinish` (with `finishReason`, `isAbort`, `isDisconnect`, `isError`), `onError`, `onData`, `throttle` (React and Vue only), `resume` (default false).

`DefaultChatTransport` extras: `fetch` (interceptor or test double), `resumeStreamIsReplay` (default true), `prepareSendMessagesRequest` receiving `id, messages, requestMetadata, body, credentials, headers, api, trigger, messageId`, and `prepareReconnectToStreamRequest` (default URL `/api/chat/{chatId}/stream`). The reference types `trigger` as `'submit-message' | 'regenerate-message'`.

## React notes

`messages`, `status`, `error` are snapshots per render; status/error updates carry the latest messages so final results render fully. Components sharing one `Chat` via `useChat({ chat })` subscribe independently, so different `throttle` values can show different snapshots.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Fixed the dataPartSchemas typo; removed the unconfirmed trigger-naming discrepancy sentence.

Method: documentation only; no commands were run.
