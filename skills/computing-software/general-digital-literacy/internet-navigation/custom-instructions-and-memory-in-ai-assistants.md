---
id: computing-software.general-digital-literacy.internet-navigation.custom-instructions-and-memory-in-ai-assistants
name: custom-instructions-and-memory-in-ai-assistants
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, in-generative-ai, custom-instructions, ai-memory, chatbot-settings]
level: intro
status: docs-checked
description: "Set custom instructions and manage memory in ChatGPT, Claude, Gemini and Copilot so answers fit you, review or delete what the assistant remembers, and use temporary chats."
sources:
  - https://help.openai.com/en/articles/8590148-memory-in-chatgpt
  - https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context
  - https://support.claude.com/en/articles/12260368-use-incognito-chats
  - https://support.google.com/gemini/answer/16598469
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom instructions and memory

## Custom instructions (standing preferences)
- **ChatGPT**: Settings > **Personalization > Custom instructions**.
- **Claude**: Settings > Your Claude > **Instructions for Claude** apply to every conversation; each **Project** has its own instructions (tone, formatting, rules) and its own memory.
- **Gemini**: *Saved info* (the label varies by region) holds instructions Gemini uses to customise responses; it stays saved until you delete it.
- **Copilot** and others: look for personalization or memory in the app's settings.

## What to write
- Role and context: "I'm a primary school teacher in Scotland."
- Output preferences: "British spelling. Short answers with bullet points. Ask a clarifying question if my request is ambiguous."
- Avoid: passwords, health details or anything you wouldn't want stored.

## Memory
- ChatGPT: Settings > Personalization > Memory has controls such as Reference saved memories and Reference chat history. Saved memories are stored separately from chat history, so deleting a chat does not remove a related saved memory. Turning memory off leaves past chats intact.
- Claude: memory is on by default for Free, Pro and Max plans; turn it off in Settings > Your Claude, where a Reset memory option permanently deletes all memories, including project memories. You can also turn Memory off for a single chat from the + menu before sending the first message.
- Gemini: you can view, edit or delete what Gemini has learned (memory summary) and turn it on or off; memory is not available in features such as Gems or Live chats. To remove something learned from a chat, delete the chats containing it from Gemini Apps Activity.
- Wrong memory leads to odd answers; delete it.

## Temporary or incognito chats
- ChatGPT **Temporary Chat** and Claude **incognito chats** are not saved to history or memory. Claude can still use your profile preferences inside an incognito chat, and incognito is not available inside projects. Providers may retain data for a period for safety; check each one's policy.

## Work accounts
- On Claude Team and Enterprise plans, owners control whether memory is available; Gemini activity for work or school accounts is controlled by the Workspace administrator. Follow your organisation's policy.

## Verify
- [ ] Ask "What do you remember about me?" and the answer matches what you intend it to know.

## Checked

Checked 2026-10-27 against OpenAI Help (Memory in ChatGPT), Claude Help (chat search and memory; incognito chats; projects) and Gemini Apps Help (memory of past chats). Confirmed: ChatGPT Personalization path and memory controls, Claude memory defaults, Reset memory, per-chat off, incognito behaviour, Gemini saved info and memory summary, Gems limitation, workplace admin control.

Method: documentation only; no commands were run.
