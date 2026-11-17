---
id: computing-software.devops-ci-cd.rundeck.password-complexity-settings
name: password-complexity-settings
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, password-strength, password-minlength, user-manager, zxcvbn]
level: practitioner
status: docs-checked
description: "Enforce minimum length and zxcvbn-scored complexity for Rundeck User Manager passwords with rundeck.password.minLength and rundeck.password.strength (Enterprise)."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/security/password-security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
This is a commercial feature of the User Manager (local logins), available from Rundeck 4.0.

Set these in Configuration Management or in `rundeck-config.properties`:

```properties
rundeck.password.minLength = <integer>
rundeck.password.strength = <strength setting>
```

`minLength` is the minimum number of characters.

`strength` is an integer 0-4 scored by the zxcvbn library on how hard the password is to guess:
- 0: easily guessable, risky (under 10^3 guesses)
- 1: very guessable, protects against throttled online attacks (under 10^6)
- 2: somewhat guessable, protects against un-throttled online attacks (under 10^8)
- 3: safely unguessable, moderate protection against offline slow-hash attacks (under 10^10)
- 4: very unguessable, strong protection (10^10 or more)

Gotcha: the page names the file `rundeck-config.properties` in one place and `rundeck-configuration.properties` in another; the config file is `rundeck-config.properties`.

Verify by trying to create a user in User Manager with a weak password and confirming it is rejected.

## Checked

2026-11-04. Confirmed against the Rundeck docs page User Manager Password Security (Commercial): Rundeck 4.0+, rundeck.password.minLength and rundeck.password.strength, strength 0-4 descriptions and guess thresholds, zxcvbn, and the rundeck-config.properties vs rundeck-configuration.properties inconsistency. Nothing removed.

Method: documentation only; no commands were run.
