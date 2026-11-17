---
id: computing-software.cloud-infrastructure-engineering.rancher.auth-local-users-fallback
name: auth-local-users-fallback
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [local-users, admin, authentication, fallback, principal]
level: intro
status: docs-checked
description: "Keep local Rancher users as a fallback: local auth is the default until an external provider is enabled, and a few local accounts survive an identity provider outage."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/authentication-config/create-local-users
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Local authentication is the default until you configure an external provider. Rancher stores usernames and passwords itself, and the first `admin` user is a local user.

Even when you use external authentication, create a few local users so you can keep using Rancher if the external service has problems.

To add one: **Users & Authentication**, then **Users** in the left menu, **Create**, complete the **Add User** form and save.

The page says local authentication is designed mainly for small-scale deployments and test environments, lacking advanced password policies and centralised identity management. It highly recommends an external provider as the primary method, and in production local authentication only as an emergency backup if the external provider goes down.

## Checked

2026-11-09. Read in full the Rancher Manager Local Authentication page (authentication-config/create-local-users). Removed the users-and-groups, bootstrap-password and SAML claims, which come from other pages not read here.

Method: documentation only; no commands were run.
