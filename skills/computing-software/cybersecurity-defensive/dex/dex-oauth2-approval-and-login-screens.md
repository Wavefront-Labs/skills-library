---
id: computing-software.cybersecurity-defensive.dex.dex-oauth2-approval-and-login-screens
name: dex-oauth2-approval-and-login-screens
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [oauth2, approval-screen, login-screen, user-flow]
level: practitioner
status: docs-checked
description: "Tune the user flow with oauth2.skipApprovalScreen and alwaysShowLoginScreen, and know how approval_prompt=force overrides them."
sources:
  - https://dexidp.io/docs/configuration/oauth2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two settings under `oauth2` shape what users see when logging in.

```yaml
oauth2:
  skipApprovalScreen: true
  alwaysShowLoginScreen: false
```

- `skipApprovalScreen`: controls the need for user approval before data is shared with a connected app. The docs' wording for this setting is ambiguous, so test the behaviour. It is not applicable when the request carries `approval_prompt=force`, in which case the approval screen is always shown.
- `alwaysShowLoginScreen`: whether to always display the login screen. If only one authentication method is enabled, the default is to go directly to it. For connected identity providers that means the browser is redirected away from the application to the upstream provider, such as the Google login page.

Gotchas:

- With a single connector and `alwaysShowLoginScreen: false`, users never see the Dex connector chooser.
- A client can always force the approval screen with `approval_prompt=force`.

## Checked

2026-11-03: read against Dex docs, OAuth2 configuration (https://dexidp.io/docs/configuration/oauth2/).

Removed or corrected: The paraphrase of the skipApprovalScreen description (the page wording is self-contradictory) and the Check step.

Method: documentation only; no commands were run.
