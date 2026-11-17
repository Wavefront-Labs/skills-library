---
id: computing-software.systems-network-administration.netbird.audit-events
name: audit-events
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, audit-events, activity-log, encryption-key, unknown-events]
level: intro
status: docs-checked
description: "Use the NetBird Audit Events log to review management changes (peers, users, policies, tokens), filter it, and fix events showing as unknown after key loss."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/activity/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Audit event logging is on by default for every NetBird network. Open the Audit Events tab in the web UI; search by activity name and filter by timeframe, event type or user.

Tracked (changes made on the Management server):
- Peers: add, remove, rename, enable or disable SSH, login expiration.
- Users and roles: join, invite, role change, block, unblock, delete.
- Groups, setup keys, routes: create, update, delete, membership.
- Policies and rules.
- Account settings: login expiration, peer approval.
- Personal access tokens, service users, integrations.
- Traffic logging and packet counting toggles.
- Posture checks, owner transfers, peer logins, dashboard logins.

Client connection events (one peer connecting to another) are not tracked in this log; the page says future versions will support them.

Troubleshooting "unknown" names and `unknown@unknown.com` emails: the event encryption key is corrupted or lost, mainly self-hosted. Find the key at:
- Combined setup: `server.store.encryptionKey` in `config.yaml`.
- Older `configure.sh` multi-container setups: `DataStoreEncryptionKey` in the `management.json` backup.

Audit events can be streamed in real time to a SIEM; see event-streaming.

## Checked

2026-11-04. Confirmed against the NetBird audit events docs page: on by default, Audit Events tab search and filters, tracked event list, unknown name cause, `server.store.encryptionKey` in `config.yaml`, `DataStoreEncryptionKey` in the `management.json` backup, SIEM streaming. Changed the client connection events line to match the page, which does not point to traffic events logging.
Method: documentation only; no commands were run.
