---
id: computing-software.systems-network-administration.audiobookshelf.oidc-lockout-recovery
name: oidc-lockout-recovery
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [oidc, sso, lockout, local-login, sqlite, authactiveauthmethods]
level: sme
status: docs-checked
description: "Recover from an OIDC misconfiguration with the autoLaunch=0 bypass, or re-enable local login by editing the settings row."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/oidc-authentication.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/faq/server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Test OIDC before turning off local authentication. If you are logged out with local login disabled, the only way back in is editing the database directly.

Step 1, bypass the SSO redirect (works only while local login is still enabled):

```text
https://example.com/login/?autoLaunch=0
```

This brings you to the local login page.

Step 2, if local login is disabled and OIDC also fails, edit the database (back it up first, and stop the server while editing):

- Table: `settings`
- Row: `server-settings`
- Key: `"authActiveAuthMethods"`
- Value to add: `"local"`

A tool such as DBeaver is suggested elsewhere in the docs for SQLite editing. Close the database before starting the server again.

For the root user's forgotten password specifically, a different edit applies: in the `users` table set the `pash` column of the root row to NULL (see the root password skill).

## Checked

Method: docs-checked 2026-11-09 against the OIDC Authentication page and the FAQ server page (SQLite editing precautions) of the Audiobookshelf docs repo, both read in full from raw markdown.
