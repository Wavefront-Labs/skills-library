---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.render-reasoning-sources-files-in-usechat
name: render-reasoning-sources-files-in-usechat
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [chatbot, usechat, reasoning, sources, attachments, file-parts, vercel-ai-sdk]
level: practitioner
status: docs-checked
description: "Forward reasoning and sources from the server, render reasoning, source and image parts, and send file attachments from useChat."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-ui/chatbot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Render reasoning, sources, generated images and attachments in useChat

Goal: show non-text message parts and let users attach files.

## Server flags on toUIMessageStream

```ts
toUIMessageStream({ stream: result.stream, sendReasoning: true })  // reasoning tokens
toUIMessageStream({ stream: result.stream, sendSources: true })    // provider sources
```

## Client part types

```tsx
message.parts.map((part, i) => {
  if (part.type === 'text') return <div key={i}>{part.text}</div>;
  if (part.type === 'reasoning') return <pre key={i}>{part.text}</pre>;
  if (part.type === 'file' && part.mediaType.startsWith('image/'))
    return <img key={i} src={part.url} alt="Generated image" />;
});
```

- Sources arrive as two part types: `source-url` (fields `sourceId`, `url`, optional `title`) and `source-document` (`sourceId`, optional `title`). Filter `message.parts` on each type; fall back to `new URL(part.url).hostname` when `title` is missing.
- Images produced by image-capable models are `file` parts. Files generated during reasoning are `reasoning-file` parts (`ReasoningFileUIPart`) with `mediaType` and `url`.

## Sending attachments

`sendMessage({ text: input, files })` accepts either:

1. A `FileList` from `<input type="file" multiple>`: `useChat` converts files to data URLs. Only `image/*` and `text/*` types are turned into multi-modal parts automatically; handle other types yourself. Reset with `setFiles(undefined)` and clear `fileInputRef.current.value = ''` after sending.
2. An array of `FileUIPart` objects: `{ type: 'file', filename: 'earth.png', mediaType: 'image/png', url }` where `url` is an https URL or a `data:` URL (good for pre-uploaded files).

Render attachments in history with `part.type === 'file' && part.mediaType?.startsWith('image/')` and `alt={part.filename}`.

## Type safety for tool parts

`InferUITool<typeof tool>` gives `{input, output}` for one tool; `InferUITools<typeof tools>` does it for a `ToolSet` (declare the object with `satisfies ToolSet`). Build `type MyUIMessage = UIMessage<never, UIDataTypes, InferUITools<typeof tools>>` and pass it to `useChat<MyUIMessage>()` and `createUIMessageStream<MyUIMessage>(...)`.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
