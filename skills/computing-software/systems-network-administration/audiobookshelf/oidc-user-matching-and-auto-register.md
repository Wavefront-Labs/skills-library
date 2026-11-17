---
id: computing-software.systems-network-administration.audiobookshelf.oidc-user-matching-and-auto-register
name: oidc-user-matching-and-auto-register
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [oidc, sso, user-matching, auto-register, authentik]
level: advanced
status: docs-checked
description: "Link OIDC logins to existing Audiobookshelf users with Match existing users by, use Auto Register, and fix Authentik Unauthorized errors."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/oidc-authentication.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/faq/server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Existing users:** use the **Match existing users by** setting to link existing Audiobookshelf accounts to OIDC accounts.

**Auto Register:** when enabled, an OIDC login that matches no existing user (by the match criteria) automatically creates and links a new user in Audiobookshelf.

**Subject mode:** with a provider such as Authentik you do not need to change it. It is not about matching; it locks a user out if they change the selected subject (for example mail or username) in the provider. Leave the default, which for most providers is a unique identifier that never changes.

**Authentik Unauthorized:** if logins return "Unauthorized", check that the user's email is verified in Authentik. See the Authentik scope-mapping documentation and the linked web-client issue #150 step-by-step guide.

**Passwords:** if a user logs in with OIDC, reset the password in the OIDC provider rather than in Audiobookshelf.

## Checked

Method: docs-checked 2026-11-09 against the OIDC Authentication page and the FAQ server page (password reset) of the Audiobookshelf docs repo, both read in full from raw markdown. Dropped a loosely derived match-field warning.
