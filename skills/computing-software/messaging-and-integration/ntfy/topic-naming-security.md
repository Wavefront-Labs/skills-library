---
id: computing-software.messaging-and-integration.ntfy.topic-naming-security
name: topic-naming-security
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, topic, security, brute-force, acl]
level: practitioner
status: docs-checked
description: "Choose ntfy topic names that are valid and hard to guess, and know when to use access control instead of obscurity."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Topic names and security

## Rules

- Allowed characters: `[-_A-Za-z0-9]`.
- Maximum length: 64 characters.
- The web app's topic generator runs locally in the browser and adds a random suffix.

## Security model

Without ACLs there is no authentication: the topic name is the password. Anyone who knows or guesses it can read and publish.

- Pick a random name, not `alerts` or `backups`.
- The FAQ argues a random 10-character name from A-Z, a-z, 0-9, `_` and `-` (64^10 possibilities) is infeasible to brute-force under default rate limiting.
- ntfy.sh bans abusive IPs; the FAQ points to am-i-banned.ntfy.sh to check.
- The ntfy.sh logs contain topic names and IP addresses (used only for troubleshooting and rate limiting, per the FAQ); if you do not trust the operator or your messages are sensitive, the FAQ says to run your own server.

## When names are not enough

On a self-hosted server set `auth-default-access: "deny-all"` and grant per-user topic access with `ntfy access`; see the access-control skills.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Picking a topic: characters, 64 characters, local generator) and FAQ (topic is the password without ACLs, 64^10 brute-force argument, am-i-banned, logs, self-hosting). Removed: the Verify curl and its 401/403 claim.
Method: documentation only; no commands were run.
