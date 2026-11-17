---
id: computing-software.web-development.ghost.ghost-cloudflare-rocketloader-fix
name: ghost-cloudflare-rocketloader-fix
category: computing-software
field: web-development
product: ghost
tags: [ghost, cloudflare, rocket-loader, minify, admin-panel, troubleshooting]
level: intro
status: docs-checked
description: "Stop Cloudflare features from breaking the Ghost admin panel by excluding the /ghost path from Rocket Loader, Mirage and auto-minify."
sources:
  - https://github.com/TryGhost/docs/blob/main/faq/using-cloudflare-with-ghost.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: fix a broken Ghost Admin behind Cloudflare.

Symptom: the browser console shows JavaScript errors such as `TypeError: n.item is not a function` or `Uncaught SyntaxError: Unexpected string` and Ghost Admin does not load after updates.

Cause: the docs recommend keeping Cloudflare performance features (Rocket Loader, Mirage and auto-minify) away from the admin panel; the page does not explain the mechanism further.

Fix: add a Cloudflare page rule for the path `/ghost*` that turns off Rocket Loader, Mirage and auto-minify for it, so these features do not touch the admin panel. Other paths can keep the optimisations.

Scope: this applies to developers maintaining self-hosted Ghost. On Ghost(Pro) both nginx and Cloudflare are already configured and no action is needed.

Verify: reload Ghost Admin with the developer console open and confirm the errors are gone.

## Checked

2026-11-04. Confirmed: both console errors, the /ghost* page rule, scope for self-hosted versus Ghost(Pro) (using Cloudflare with Ghost page). Removed: the rewrite-mechanism explanation and the related-setup bullets (nginx proxy headers, caching rules), which the page does not state.

Method: documentation only; no commands were run.
