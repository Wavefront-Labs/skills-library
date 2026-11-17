---
id: computing-software.cybersecurity-defensive.pomerium.ssh-policy-criteria
name: ssh-policy-criteria
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [ssh-publickey, ssh-ca, ssh-username, ssh-policy, username-matches-claim]
level: advanced
status: docs-checked
description: "Apply SSH-specific Pomerium policy criteria such as ssh_publickey, ssh_ca and ssh_username, and know which general criteria work on SSH routes."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/native-ssh-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SSH-specific criteria:
- `ssh_publickey`: matches the client public key (authorized_keys format); string or list.
- `ssh_ca`: requires the client key to be a certificate signed by the listed CA key(s).
- `ssh_username`: matches the requested username (a string or list).
- `ssh_username_matches_claim`: requested username must appear in the list held by the named OAuth claim (e.g. `allowed_usernames`).
- `ssh_username_matches_email`: when `true`, the username must equal the email local part (`bobby` for `bobby@gmail.com`).

General criteria that work: `email`, `domain`, `user`, `claim`. Enterprise-only on SSH: `groups`, `record`, `date`, `day_of_week`, `time_of_day`.

Not applicable on SSH: `http_method`, `http_path`, `cors_preflight`, `client_certificate`, `invalid_client_certificate`, `pomerium_routes`, `device`.

Docs examples include: `prod-server` needing the `sre-team` group and a weekday; and a combined `ops-server` rule with an email domain ending in `@example.com`, group, weekday, `ssh_publickey` list and `ssh_username_matches_email: true`.

Optional rate limiting: `ssh_rls_enabled: true` and `ssh_rls_additional_entries` (key/value descriptors using Envoy formatting such as `%DOWNSTREAM_REMOTE_ADDRESS_WITHOUT_PORT%`).

## Checked

2026-11-04. Read the Native SSH Access page: the five SSH criteria, applicability lists, the two policy examples and the rate-limit settings all confirmed. Nothing removed.

Method: documentation only; no commands were run.
