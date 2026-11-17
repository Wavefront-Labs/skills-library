---
id: computing-software.devops-ci-cd.verdaccio.webhook-notifications
name: webhook-notifications
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [notify, webhook, handlebars, notify-block, webhook-template, publish-events, slack]
level: practitioner
status: docs-checked
description: "Send publish and unpublish events to Slack, Google Chat or any HTTP endpoint with the notify block, Handlebars templates, publishType and packagePattern."
sources:
  - https://verdaccio.org/docs/notifications/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Notifications fire on publish (and, since 6.8.0, unpublish). Single endpoint:

```yaml
notify:
  method: POST
  headers: [{ 'Content-Type': 'application/json' }]
  endpoint: https://hooks.example.org/registry
  content: '{"type":"{{ publishType }}","package":"{{ publishedPackage }}","by":"{{ publisher.name }}"}'
```
Several endpoints: use named keys under `notify` (e.g. `'example-google-chat'`, each with its own method, headers, endpoint, content).

Properties: `method` (POST, PUT, GET), `packagePattern` (regex; only matching package names notify), `packagePatternFlags`, `headers` (required), `endpoint` (required), `content` (required, Handlebars).

Template variables: `name`, `versions` (iterate with `{{#each versions}} v{{version}}{{/each}}`), `publisher.name`, `publisher.groups`, `publishedPackage` (package@version), `publishType` (`publish`, `unpublish`, `stage`, `unstage`).

Gotchas:
- No extra Handlebars helpers exist, so you cannot compare `publishType` in the template; send everything and filter at the receiver.
- Publisher info is unavailable if package.json already has a publisher property.
- `stage`/`unstage` fire only with staged publishing; approving reports `publish`.

## Checked

Method: docs-checked 2026-11-09 against the Verdaccio notifications page (website source, read in full); documentation only, no commands were run.
