---
id: computing-software.collaboration-platform-administration.zulip.securing-your-zulip-server
name: securing-your-zulip-server
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [server-security, hardening, shell-access, access-management]
level: practitioner
status: docs-checked
description: "Apply Zulip's server hardening checklist: limit shell access, prefer SSO, API key hygiene, access model, upload domain, Camo, outgoing request paths and rate limits."
sources: ["https://zulip.readthedocs.io/en/latest/production/securing-your-zulip-server.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Securing a Zulip server

Six practices from the documentation:

1. **Limit shell access.** Root on an application or database server, or access to the `zulip` user, gives complete control of all data, including reading messages and rewriting history.
2. **Prefer single sign-on** (Google, LDAP or similar) over passwords.
3. **Teach users to reset compromised credentials.** Each user's API key can do almost anything a logged-in user can, so a lost phone means resetting both API key and password.
4. **Learn the access model**: channel types and permissions, user roles, user groups, message edit and deletion restrictions, and bots.
5. **Understand uploads and outbound requests.** Host uploads from a separate domain, for example `zulip-user-content.example.com`, to avoid same-domain attacks. Backends are `LOCAL_UPLOADS_DIR` or S3. File URLs are long random strings, and every access also verifies the logged-in user received the file. The go-camo proxy fetches inline images so clients do not contact external servers; `INLINE_IMAGE_PREVIEW` controls image previews. Outgoing webhook bots, image and webpage previews, video-call API integrations and push notifications make server-side requests, and all go through Smokescreen, which denies non-public addresses including 127.0.0.1. Camo skips Smokescreen by default because it blocks private subnets itself.
6. **Understand rate limiting** (see the rate-limiting skill).

Report suspected vulnerabilities to the project's security team by email rather than publicly.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/securing-your-zulip-server.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.
