---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.send-images-and-files-in-messages
name: send-images-and-files-in-messages
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [prompts, multimodal, image-parts, file-parts, experimental-download]
level: practitioner
status: docs-checked
description: "Attach images, PDFs and audio to a user message with file parts, choose the data format, set mediaType, and customise downloads."
sources:
  - https://ai-sdk.dev/docs/foundations/prompts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: send an image, PDF or audio file to a model as a part of a user message.

## Image parts
Put a part with `type: 'file'` and `mediaType: 'image'` in the user message content array next to a text part. `data` can be any of:
- base64 string or data URL string (`data:image/png;base64,...`)
- `ArrayBuffer`, `Uint8Array` or `Buffer`
- http(s) URL string or a `URL` object

```ts
const result = await generateText({
  model,
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'Describe the image in detail.' },
      { type: 'file', mediaType: 'image', data: fs.readFileSync('./data/comic-cat.png') },
    ],
  }],
});
```

## Other files (PDF, audio)
File parts accept the same data kinds, but you must give the MIME type:
```ts
{ type: 'file', mediaType: 'application/pdf', data: fs.readFileSync('./data/example.pdf'), filename: 'example.pdf' } // filename optional, not used by all providers
{ type: 'file', mediaType: 'audio/mpeg', data: fs.readFileSync('./data/galileo.mp3') }
```
The docs warn only a few providers/models support file parts: Google Generative AI, Google Vertex, OpenAI (wav and mp3 audio with `gpt-4o-audio-preview`, and pdf) and Anthropic.

## Provider options on a part
Settings like OpenAI image detail go on the part: `providerOptions: { openai: { imageDetail: 'low' } }` on the text or file part.

## Custom download function (experimental)
The default download implementation downloads files in parallel when they are not supported by the model. For throttling, retries, authentication or caching pass `experimental_download`, which receives `Array<{ url: URL; isUrlSupportedByModel: boolean }>` and returns an array in the same order of `{ data: Uint8Array; mediaType: string | undefined } | null`. It is experimental and may change.

## Gotchas
- Assistant messages can also carry file parts, but those are for model-generated files, which only a few models support.
- You need to specify the MIME type of the file you are sending: set `mediaType` on every file part.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Reworded the download-default line to the docs wording and replaced the invented "usual cause of rejected requests" gotcha with the docs statement about specifying the MIME type.

Method: documentation only; no commands were run.
