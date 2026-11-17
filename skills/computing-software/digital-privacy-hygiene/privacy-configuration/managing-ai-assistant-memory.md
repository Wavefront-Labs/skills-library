---
id: computing-software.digital-privacy-hygiene.privacy-configuration.managing-ai-assistant-memory
name: managing-ai-assistant-memory
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, ai-memory, ai-privacy, ai-chat-history]
level: practitioner
status: draft
description: "Review and control what AI assistants remember about you across chats: view and delete saved memories, turn off chat-history reference, use temporary chats."
sources:
  - "https://help.openai.com/en/articles/8590148-memory-faq"
  - "https://support.anthropic.com/"
  - "https://support.google.com/gemini/answer/15637730"
  - "https://ssd.eff.org/module/privacy-considerations-ai-tools"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Managing AI assistant memory

**Goal:** the assistant only remembers what you want it to carry between conversations.

## What "memory" means
Assistants can store facts about you (name, job, family, preferences, health details you mentioned) and reuse them
in later chats; some also reference your past chat history.

## Where to control it (names vary by product and change often)
| Product | Controls |
|---|---|
| ChatGPT | Settings > Personalization > Memory: reference saved memories, reference chat history; Manage memories to delete items; Temporary Chat for no-memory sessions |
| Claude | Settings > memory / chat search options where available; incognito-style chats |
| Gemini | Saved info and personal context settings; Gemini Apps Activity |
| Copilot | Settings > Privacy / Personalization and memory |

## Routine
1. Open the memory list; delete anything sensitive (health, finances, other people's details, location).
2. Decide whether chat-history reference should be on.
3. Use temporary/incognito chats for one-off sensitive questions.
4. Tell the assistant "forget X"; then check the memory list actually changed.

## On shared or work accounts
Workspace admins may control memory and retention; personal facts in a work account belong to the employer's data.

## Gotchas
- Deleting a memory doesn't necessarily delete the chat where you said it; delete that chat too.
- Memory is separate from training opt-out; set both.
