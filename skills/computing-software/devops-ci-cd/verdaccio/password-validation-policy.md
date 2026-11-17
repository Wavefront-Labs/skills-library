---
id: computing-software.devops-ci-cd.verdaccio.password-validation-policy
name: password-validation-policy
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [password-policy, password-regex, validation, passwordvalidationregex, min-length, registration]
level: practitioner
status: docs-checked
description: "Enforce a minimum password strength with server.passwordValidationRegex for registration and password changes handled by Verdaccio itself."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/change-password/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The default minimum is three characters. Change it with a regular expression:

```yaml
server:
  # at least 10 characters
  passwordValidationRegex: /.{10}$/
```
The value arrives from YAML as a string and is compiled at runtime. An invalid pattern makes every password fail validation rather than being ignored, so test it after changing it.

Scope: it applies only where Verdaccio validates the password itself, i.e. user registration and password changes (htpasswd). An auth plugin that manages its own users (LDAP, identity provider) is not affected.

With the `changePassword` flag, a too-weak new password gets a `401` password-too-short error.

Also see the htpasswd skill for `max_users: -1` to close registration.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (Password policy), Changing a password and Authentication. Confirmed: the three-character default, the regex form, string compilation, invalid patterns failing every password, the registration and password-change scope, the 401 password-too-short answer and max_users: -1. Removed or corrected: the adduser verify command.

Method: documentation only; no commands were run.
