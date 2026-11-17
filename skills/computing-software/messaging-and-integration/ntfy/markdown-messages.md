---
id: computing-software.messaging-and-integration.ntfy.markdown-messages
name: markdown-messages
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, markdown, x-markdown, formatting]
level: intro
status: docs-checked
description: "Send Markdown-formatted ntfy messages with the X-Markdown header or a text/markdown content type."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Markdown formatting

Messages are plain text by default. Enable Markdown with either:

- Header `X-Markdown` (aliases `Markdown`, `md`) set to `true`, `1` or `yes`
- `Content-Type: text/markdown`

```
curl -d "Look ma, **bold** and a [link](https://example.com)" -H "Markdown: yes" ntfy.sh/mytopic
curl -H "Content-Type: text/markdown" -d "# Heading" ntfy.sh/mytopic
```

## Supported elements

Emphasis, links, images, code blocks, inline code, headings, lists, blockquotes, horizontal rules.

## Gotchas

- The publish page marks Markdown as supported on Android and Firefox (the web app).
- In JSON publishing use the boolean field `markdown`.
- The Android publish dialog can send Markdown (listed in the phone page).

## Checked

2026-11-04. Confirmed against the ntfy publish page (Markdown formatting, JSON table) and phone page (publish dialog): header, aliases and accepted values, content type, supported element list, platform marker. Removed: a claim that other clients show raw text, and the Verify step.
Method: documentation only; no commands were run.
