---
id: computing-software.it-support-helpdesk.user-support-communication.prompting-ai-for-troubleshooting
name: prompting-ai-for-troubleshooting
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, prompt-engineering-support, ai-in-support, generative-ai, troubleshooting, comptia-a-plus]
level: practitioner
status: draft
description: "Prompt AI assistants for troubleshooting help: give context, errors and what was tried, ask for ranked hypotheses and checks, redact sensitive data, and verify every answer."
sources:
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
  - https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy
  - https://www.comptia.org/certifications/a
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prompting AI for troubleshooting

AI assistants (Copilot, ChatGPT, Claude, ServiceNow Now Assist) speed up diagnosis when given good input. Treat their output as hypotheses to test, and use only tools your organisation has approved for ticket data.

## Before you paste anything
Redact usernames, emails, hostnames, IPs, keys, tokens, customer data. Use the approved enterprise AI tool, which keeps data in your tenant. Never paste passwords or full logs containing secrets.

## A good prompt has
1. **Role and goal**: "You are helping a desktop support technician diagnose..."
2. **Environment**: OS and build (`winver`), device model, app version, managed by Intune/domain, network type.
3. **Symptom precisely**: exact error text or code (`0x80070005`), when it started, who is affected (one user, all users, one site).
4. **What changed**: updates, new software, password change, moved office.
5. **What you already tried** and the results.
6. **Output format**: "Give the 3 most likely causes ranked, with a quick check for each, and commands that are read-only first."
7. **Constraints**: "No registry edits without explaining the risk; I don't have admin on the server."

### Example
```
Windows 11 23H2, Intune-managed laptop, Outlook (Microsoft 365 Apps, current channel).
Since this morning one user gets "Something went wrong [1001]" signing into Outlook; Teams works.
Tried: restart, Outlook safe mode (same), new Outlook profile (same).
List the 3 most likely causes ranked, with a read-only check for each, before any fix.
```

## Iterate
Feed back the results of each check ("dsregcmd /status shows AzureAdPrt: NO"), ask follow-ups, ask it to explain what a command does before running it.

## Verify
Check suggested commands, registry keys and settings against vendor documentation (AI can invent cmdlets or keys). Test in a lab or on one device first, and record the verified fix and source in the ticket, not the AI transcript.
