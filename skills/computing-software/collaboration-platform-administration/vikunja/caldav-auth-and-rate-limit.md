---
id: computing-software.collaboration-platform-administration.vikunja.caldav-auth-and-rate-limit
name: caldav-auth-and-rate-limit
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, caldav-token, caldav-api-token, caldav-429, caldav-2fa]
level: practitioner
status: docs-checked
description: "Choose the right CalDAV password for Vikunja (account password, dedicated CalDAV token or tk_ API token) and handle the failed-auth 429 rate limit."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/help/caldav.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CalDAV clients log in with the Vikunja username plus one of:

1. Account password: easiest, works for local and LDAP-provisioned accounts. Does not work for OIDC accounts (no password stored) or when two-factor authentication is on.
2. Dedicated CalDAV token: create it in Settings, CalDAV tab. Shown once. Use for OIDC or 2FA accounts.
3. API token (starts `tk_`) with the CalDAV permission group, from 2.3.0. One token can cover CalDAV and API access.

Rate limit (2.6.0 and later): failed CalDAV auth is limited per IP, default 10 failures per minute, even if the general rate limiter is off. Beyond that the IP gets `429 Too Many Requests` until the minute passes. Requests without credentials only get the normal auth challenge, and successful requests are refunded, so normal sync is unaffected. The failure budget is shared with authenticated notification feeds from that IP.

Troubleshooting: a client that suddenly breaks after several credential errors needs its saved credentials fixed and a one-minute wait.

## Checked

2026-11-04: authentication options, version gates (2.3.0, 2.6.0) and rate-limit behaviour checked against the CalDAV help page, and the limit's default (`ratelimit.basicauthlimit` 10) against config-raw.json. Removed the reverse-proxy shared-budget remark, which the page does not state.

Method: documentation only; no commands were run.
