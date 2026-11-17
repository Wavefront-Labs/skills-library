---
id: computing-software.cybersecurity-defensive.zitadel.instance-feature-restrictions
name: instance-feature-restrictions
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, restrictions, instance, registration, allowed-languages]
level: advanced
status: docs-checked
description: "Restrict public organization registration and languages on an instance, via self-hosting defaults or the Feature Restrictions admin API."
sources:
  - https://zitadel.com/docs/guides/manage/customize/restrictions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
New self-hosted and cloud instances are unrestricted by default. Self-hosters can change this default for new instances with the `DefaultInstance.Restrictions` settings section. Users holding IAM_OWNER can change an existing instance's restrictions through the Feature Restrictions admin API.

Two restrictions exist:

Disallow public organization registrations. When restricted, only IAM_OWNERs can create organizations. The endpoint `/ui/login/register/org` then returns HTTP 404 for GET requests and 409 for POST requests. Use this when you run ZITADEL as an internal platform and do not want anonymous sign-up of organizations.

AllowedLanguages. Only allowed languages appear in the discovery document at `/.well-known/openid-configuration`, the login UI texts and the notification message texts render only in allowed languages. Custom texts can still be created for a disallowed language as long as ZITADEL supports it, so you can customize texts before allowing a language.

Restrictions for an instance are meant to be configured by a user managed inside that instance. If you self-host and need to control the usage of your virtual instances from outside, use the system-user APIs for limits and quotas described in the usage control skill.

Check the result by requesting the discovery document and, for registration, visiting the organization registration path.

## Checked

2026-11-08. Read the feature restrictions page in full; added the custom texts rule.

Method: documentation only; no commands were run.
