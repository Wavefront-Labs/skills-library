---
id: computing-software.digital-privacy-hygiene.privacy-configuration.ai-connectors-and-agent-permissions
name: ai-connectors-and-agent-permissions
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, ai-connectors, ai-privacy, oauth-scopes, prompt-injection]
level: practitioner
status: draft
description: "Review and limit the email, drive and calendar access granted to AI assistant connectors and agents, revoke unused ones, and watch for prompt injection."
sources:
  - "https://help.openai.com/"
  - "https://support.anthropic.com/"
  - "https://myaccount.google.com/connections"
  - "https://owasp.org/www-project-top-10-for-large-language-model-applications/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Connected apps and agent permissions

**Goal:** an AI assistant connected to your mail, files and calendar gets only the access it needs, and can't be
tricked into leaking it.

## Inventory
- In each AI app: ChatGPT Settings > Apps/Connectors; Claude Settings > Connectors; Gemini Apps/Extensions; Microsoft
  Copilot connected accounts.
- On the data side: Google Account > Security > **Your connections to third-party apps**; Microsoft account > Privacy >
  Apps and services; Slack/GitHub/Notion "installed apps".
Note the scopes: read-only vs read-write, single folder vs whole drive, send email or only read.

## Limit
- Remove connectors you haven't used in a month.
- Prefer read-only and narrower scopes (one shared folder, a label) when offered.
- Keep "act on my behalf" features (sending email, booking, purchases) behind confirmation prompts; don't turn on
  auto-approval.
- Use a separate account for experiments.

## Prompt injection
Content the assistant reads (emails, web pages, shared documents) can contain hidden instructions telling it to
forward data or click links. OWASP lists prompt injection as the top LLM application risk. Defences for users:
- Don't connect high-value mailboxes to agents that also browse the web freely.
- Review actions before approving; be suspicious of unexpected requests to share, send or download.

## Data retention
Connector data used in a chat may be stored in chat history; check the app's training and history settings and delete
chats containing sensitive material.

## Verify
After revoking, the service's connections page should no longer list the AI app; test that the assistant can't reach
the data.
