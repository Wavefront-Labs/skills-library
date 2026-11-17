---
id: computing-software.cybersecurity-defensive.zitadel.settings-and-policy-inheritance
name: settings-and-policy-inheritance
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, policies, default-settings, inheritance, console]
level: practitioner
status: docs-checked
description: "Configure ZITADEL default settings at instance level, know which policies organizations can override, and find the settings page in the console."
sources:
  - https://zitadel.com/docs/concepts/structure/policies
  - https://zitadel.com/docs/guides/manage/console/default-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Settings and policies control how every part of an instance or organization behaves. The API often calls settings "policies". Every setting has a default at instance level, and organizations can override most of them. Some policies exist only at instance level.

Open the instance defaults at `{instanceDomain}/ui/console/settings`, or use the default settings button at the top right of the console. The page covers:

- Organizations list and Features
- Notification settings (SMTP and SMS)
- Login behavior and security, including MFA and passkeys
- Identity providers available to all organizations
- Password complexity, password expiry and lockout
- Domain settings, branding, message texts and login interface texts
- External links, OIDC token lifetimes and the secret generator

The Features page offers Enabled, Disabled or Inherit per feature. Inherit follows the product default. Features can be experimental, so enable them deliberately.

If you run a single organization, the instance defaults are usually all you configure. With several organizations, set the instance default for the common case and override only the organizations that need different behavior. Branding and SMTP are worth setting first, so users see a familiar login page and mail sender from the start.

## Checked
2026-11-08. Confirmed against the ZITADEL Settings and Policies concept page and the Default Settings console guide: instance defaults, per-organization override, instance-only policies, settings URL, settings list, Features Enabled/Disabled/Inherit, branding and SMTP recommendation. Fixed the source URL list.
Method: documentation only; no commands were run.
