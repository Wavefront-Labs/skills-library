---
id: computing-software.it-support-helpdesk.user-support-communication.supporting-microsoft-365-copilot-users
name: supporting-microsoft-365-copilot-users
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, ai-in-support, copilot-support, microsoft-365-copilot, copilot-chat, copilot-licence, oversharing, sharepoint-permissions, update-channel, copilot-oversharing]
level: practitioner
status: draft
description: "Field Microsoft 365 Copilot tickets: licence and app prerequisites, Copilot missing in Office apps, oversharing reports, and coaching users to verify output."
sources:
  - "https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-requirements"
  - "https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy"
  - "https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-enable-users"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# supporting-microsoft-365-copilot-users

Goal: resolve "Copilot isn't there / doesn't work / showed me something it
shouldn't" quickly, and set user expectations.

## "I don't have Copilot"
1. Licence: user has a **Microsoft 365 Copilot** add-on licence (Copilot
   Chat without licence is web-grounded and available more broadly) —
   M365 admin centre → user → Licenses.
2. Prerequisite base licence (M365 E3/E5, Business Standard/Premium, etc.).
3. Apps: Microsoft 365 Apps on **Current Channel or Monthly Enterprise**
   (Semi-Annual gets features later); new Outlook/classic Outlook build;
   Teams desktop updated.
4. Signed in with the work account (File → Account); sign out/in after
   licence assignment — allow up to 24–72 hours for provisioning.
5. Tenant settings: admins can pin/unpin, and some features are
   controlled by policy (e.g. Copilot in Teams meetings requires
   transcription).

## "Copilot showed me a file I shouldn't see"
Copilot only surfaces content the user already has permission to access —
the report usually reveals **oversharing** (site shared with "Everyone
except external users", broad links). Treat as a data-governance issue:
record the item, escalate to the SharePoint/data owner, don't dismiss it.
Admin tools: SharePoint Advanced Management reports, restricted content
discovery, sensitivity labels.

## "It gave a wrong answer"
Expected limitation — coach the user: give context and source files in the
prompt, ask for citations, check the referenced documents, never send
AI-generated content without reviewing it. Feedback via thumbs down helps
Microsoft, not the help desk queue.

## Common fixes
| Symptom | Fix |
|---|---|
| Copilot icon greyed in Word/Excel | file not saved to OneDrive/SharePoint (some features need cloud files and AutoSave) |
| Excel Copilot refuses | data not formatted as a table |
| Outlook Copilot missing | wrong Outlook version / shared mailbox context |
| Meeting recap missing | transcription off or meeting policy |

## Verify
User sees Copilot in the target app, completes one task with citations
visible, and any oversharing report has a linked governance ticket.
