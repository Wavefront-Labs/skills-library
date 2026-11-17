---
id: computing-software.general-digital-literacy.office-suites.ai-features-in-office-apps
name: ai-features-in-office-apps
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, generative-ai, copilot, gemini, microsoft-365-copilot, gemini-in-workspace, ai-writing, ai-summarisation]
level: intro
status: docs-checked
description: "Use Copilot in Microsoft 365 and Gemini in Google Workspace to draft, summarise and analyse in Word, Excel, Outlook and Docs while checking output and protecting data."
sources:
  - https://learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-overview
  - https://support.microsoft.com/en-us/microsoft-365-copilot/frequently-asked-questions-about-copilot-in-microsoft-365-subscriptions
  - https://knowledge.workspace.google.com/admin/gemini/google-workspace-with-gemini
  - https://workspace.google.com/solutions/ai/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# AI features in office apps

**Goal:** save time drafting and summarising without sending out wrong facts or leaking data. Product names, plans and features change often; confirm on the vendor pages in `sources`.

## What each suite offers (per vendor documentation, October 2026)
| App | Microsoft 365 Copilot | Google Gemini |
|---|---|---|
| Word / Docs | Draft, rewrite and summarise documents; ask questions about a document | *Help me write* drafts and refines text in Docs |
| Excel | Suggest formulas, chart types and insights; needs AutoSave on, so the file must be in OneDrive | (not covered here) |
| PowerPoint | Build a deck from a prompt or an existing file; summarise or edit a presentation | (not covered here) |
| Outlook / Gmail | Draft email, summarise threads, adjust tone and length | Summaries of long email threads; help drafting and suggested replies |
| Meetings | (see Teams documentation) | *Take notes for me* in Meet captures notes and highlights into a document |

Availability depends on licence, Workspace edition and admin settings; without a Copilot add-on licence Microsoft gives only limited access.

## Working well
- Give context: audience, length, tone and source.
- Treat drafts as first drafts: check every number, name, date and quote against the source. Word adds a notice that AI content may contain errors.
- Ask where a statement came from and open the source.

## Data and policy
- Copilot reaches data with your identity and permissions, so anything over-shared in SharePoint or OneDrive can surface through it; tidy permissions first.
- Read your organisation's AI policy and the vendor's data-handling terms for your account type before pasting personal data, passwords or confidential client material.
- Disclose AI assistance where your school or employer requires it.

## Gotchas
- Summaries skip nuance and can invent actions nobody agreed; review meeting notes before sharing.
- Suggested formulas can reference the wrong range; test on a few rows.

## Verify
- [ ] Every fact in the AI draft traced to a source.
- [ ] Account type and data-protection terms checked before use.

## Checked

2026-10-27. Microsoft Copilot overview and FAQ search results (Word, Excel, PowerPoint, Outlook features, AutoSave requirement, identity/permissions access, add-on licensing) and Google Workspace with Gemini help (Help me write, Gmail summaries, Meet notes, edition-dependent availability), as of 2026-10-27. Removed unconfirmed button names, the Excel Table requirement, the Teams recap line, the Sheets/Slides entries and enterprise-data-protection training claims.

Method: documentation only; no commands were run.
