---
id: computing-software.general-digital-literacy.internet-navigation.privacy-when-using-ai-tools
name: privacy-when-using-ai-tools
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, generative-ai, ai-chatbots, ai-privacy, chat-history, training-opt-out, temporary-chat, workplace-ai-policy, confidential-data]
level: intro
status: docs-checked
description: "Protect personal and work data when using AI chatbots: what not to paste, chat history and training opt-outs, temporary chats, and workplace-approved tools."
sources:
  - https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt
  - https://support.google.com/gemini/answer/13594961
  - https://learn.microsoft.com/en-us/microsoft-365/copilot/enterprise-data-protection
  - https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Privacy when using AI tools

**Goal:** get help from AI without leaking sensitive information.

## Don't paste into consumer AI tools
Passwords, one-time codes, bank/card numbers, ID numbers, medical details of others, client or
employer confidential documents, unpublished financials, source code under NDA, other people's
personal data.

## Settings to check (names vary by product and change often)
- **ChatGPT:** Settings › Data controls › *Improve the model for everyone* (OpenAI says it is on by default for personal Free, Plus and Pro; off stops new chats being used for training but does not delete saved chats); **Temporary Chat** is not used to improve models and does not appear in history. Delete existing chats separately.
- **Google Gemini:** Gemini Apps Activity: review and delete activity, change the auto-delete period and control whether data is used to improve Google AI. Google's notice says human reviewers review some data, and chats are still used to respond to you and for protection even with Keep Activity off.
- **Microsoft Copilot:** with a work or school account, Microsoft says enterprise data protection means prompts and responses are not used to train foundation models; they may still be logged and retained for audit. Personal accounts are different.
- **Claude:** Settings › Privacy has the model-improvement toggle for consumer plans; Anthropic says incognito chats are not used for training. Turning the setting off does not remove data already used in completed or in-progress training runs.
- Memory/personalisation features remember facts about you; review and clear them.

## At work
Follow your organisation's AI policy and use the approved tool (often the enterprise version with
contractual data protection). If none exists, ask before using customer or internal data.

## Other cautions
- Uploading a document gives the provider a copy; redact names and numbers first.
- AI browser extensions and meeting note-takers can read pages and record calls; tell participants
  and check permissions.

## Verify
- [ ] Training/activity settings are set the way you want in each AI tool you use.

## Checked

Checked 2026-10-27 against OpenAI Help (data controls in ChatGPT), the Gemini Apps privacy notice, Microsoft Learn (enterprise data protection) and the Claude Privacy Center (model improvement settings). Confirmed: ChatGPT setting name, default and Temporary Chat behaviour; Gemini Apps Activity controls and human review; Copilot work or school data protection and retention; Claude toggle and incognito chats.

Method: documentation only; no commands were run.
