---
id: computing-software.collaboration-platform-administration.vikunja.hardening-disable-features
name: hardening-disable-features
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, attack-surface, enablelinksharing, enablecaldav, webhooks-enabled, user-search-scope]
level: advanced
status: docs-checked
description: "Reduce Vikunja's attack surface by disabling link sharing, public teams, CalDAV, webhooks, plugins, importers, user deletion and attachments you do not need."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/security-hardening.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turn off what you do not use (defaults in brackets):
- `service.enablelinksharing` [true]: stops public link shares.
- `service.enablepublicteams` [false]: keeps teams visible to members only.
- `service.enablecaldav` [true]: removes the CalDAV endpoint, which accepts HTTP basic auth.
- `webhooks.enabled` [true]: stops users making Vikunja request URLs they choose.
- `plugins.enabled` [false]: keeps third-party code out.
- `migration.todoist.enable`, `migration.trello.enable`, `migration.microsofttodo.enable` [false]: OAuth importers.
- `service.enableuserdeletion` [true]: stops self-deletion, for retention needs; the CLI is unaffected.
- `service.enabletaskattachments` [true]: no uploads.

To restrict user search, set `service.enableopenidteamusersearch: true`; users then only find people sharing a team with them.

The file importers (Vikunja export, TickTick, WeKan, CSV) cannot be disabled. Bound them with `migration.vikunjafile.*` and `migration.maxcsvrows`.

Outgoing requests: keep `outgoingrequests.allownonroutableips` false to block SSRF to private, loopback and link-local addresses, and keep `sentry.enabled` off if no data may leave your network.

## Checked

2026-11-04. Confirmed against the Vikunja Security hardening page (setup/security-hardening): the feature keys and their defaults, user search restriction, the non-disableable file importers and their limits, outgoingrequests.allownonroutableips and sentry.enabled. Nothing removed.

Method: documentation only; no commands were run.
