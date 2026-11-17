---
id: computing-software.web-development.appwrite.appwrite-email-policies
name: appwrite-email-policies
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, email-policies, abuse-protection, project-api]
level: practitioner
status: docs-checked
description: "Block free, aliased or disposable email addresses at sign-up and on email changes using Console toggles or the Project service."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/email-policies/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: raise sign-up quality and cut throwaway accounts.

Three independent policies:
- Deny free emails: blocks providers such as Gmail or Yahoo.
- Deny aliased emails: blocks tags and subaddresses like `user+folder1@gmail.com`.
- Deny disposable emails: blocks temporary providers such as mailinator.

They run at sign-up and when an existing user changes their email. They do not affect session creation, so existing users whose address would now fail can still sign in.

Console: project > Auth > Security tab > Email policies card, toggle, then Update.

Server SDK (Project service, each method takes an `enabled` boolean; for example `appwrite project update-deny-free-email-policy --enabled true` in the CLI): `project.updateDenyFreeEmailPolicy`, `project.updateDenyAliasedEmailPolicy`, `project.updateDenyDisposableEmailPolicy`. The API key needs the `policies.write` scope.

Benefits per docs: higher quality user data, lower spam and abuse (including duplicate accounts through subaddresses of one inbox), work-email-only rules, and fewer bounced emails.

Gotcha: the aliased policy rejects any address with aliases, tags, subaddresses or provider-specific variations, such as `user+folder1@gmail.com`, so tell people on your sign-up form.

The CLI command for the aliased policy is named `update-deny-canonical-email-policy` on the docs page.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Email policies (auth/email-policies): the three policies and examples, when they run (sign-up and email change, not session creation), Console path, the three Project service methods (`updateDenyFreeEmailPolicy`, `updateDenyAliasedEmailPolicy`, `updateDenyDisposableEmailPolicy`), the `enabled` body, the `policies.write` scope and the benefits. Removed: the Verify step.
Method: documentation only; no commands were run.
