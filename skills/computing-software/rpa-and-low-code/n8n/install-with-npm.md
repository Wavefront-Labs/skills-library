---
id: computing-software.rpa-and-low-code.n8n.install-with-npm
name: install-with-npm
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, npm, npx, node-js, revert, db-revert]
level: intro
status: docs-checked
description: "Install n8n with npx or npm -g (deprecated from 3.0): Node.js 20.19 to 24.x, update commands and reverting an upgrade with n8n db:revert."
sources:
  - https://docs.n8n.io/deploy/host-n8n/install-options/install-with-npm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run n8n locally from npm. npm-based installs are deprecated from n8n 3.0, and n8n Assistant is not available with this method. Node.js must be between 20.19 and 24.x inclusive.

- Try without installing: `npx n8n`, then open `http://localhost:5678`.
- Install: `npm install n8n -g`; a specific version `npm install -g n8n@0.126.1`; the next channel `npm install -g n8n@next`.
- Start: `n8n` or `n8n start`.
- Update to latest: `npm update -g n8n`.

## Reverting an upgrade
Install the older version. If the upgrade ran a database migration, read the feature docs and release notes for manual steps, then run `n8n db:revert` on the current (newer) version to roll back the database. Repeat for each migration you need to undo.

## Tunnel for webhooks
With npm, use the services-only approach (needs Docker for cloudflared): `pnpm --filter n8n-containers services --services cloudflared` in one terminal and `pnpm dev` in another. The services command writes `packages/cli/bin/.env` with `WEBHOOK_URL` and `N8N_PROXY_HOPS=1`. Clean up with `pnpm --filter n8n-containers services:clean`.

On Windows, verify your Node.js environment setup if n8n will not start.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/install-options/install-with-npm

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
