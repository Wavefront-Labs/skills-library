---
id: computing-software.cybersecurity-defensive.zitadel.user-types-human-service-federated
name: user-types-human-service-federated
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, users, service-accounts, federated-users, external-users]
level: intro
status: docs-checked
description: "Distinguish ZITADEL human users, service accounts, federated users and external users, and how each authenticates."
sources:
  - https://zitadel.com/docs/guides/manage/console/users-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL separates interactive users from machines.

Human users are people who log in through an interface. They have an email address, a password and optional profile data such as phone, nickname, gender and language. They can authenticate with a password, with multiple factors or with passkeys. The application redirects the user to ZITADEL, which handles credentials and issues a token.

Service accounts represent machines, backend services or IoT devices. Their profile is only a name, description and username. They authenticate with the JWT profile or a personal access token, and both support expiration. They mainly gain access to the Management API or secure backend-to-backend calls.

Federated users are identities managed by a third-party identity provider such as Google, Azure AD or GitHub. Users log in through the external provider, and the federated identity is linked to an internal ZITADEL user so role assignments and audit trails still work.

External users are users from another organization who were invited to your projects through external role assignments.

Any user or service account can also hold an administrator role, which allows managing the instance, an organization or a project.

## Checked
2026-11-08. Confirmed against the ZITADEL Users overview page: human users, service accounts (JWT profile or PAT, both with expiration), federated users, external users via external user grants, administrators.
Method: documentation only; no commands were run.
