---
id: computing-software.cybersecurity-defensive.authelia.password-policy
name: password-policy
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, password-policy, zxcvbn, password-strength, min-length, complexity]
level: practitioner
status: docs-checked
description: "Enforce an Authelia password policy with the standard rules or the zxcvbn strength meter, noting that only one can be enabled and zxcvbn does not block."
sources:
  - https://www.authelia.com/configuration/security/password-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia can enforce rules when users choose a new password. Two policies exist and only one may be enabled at a time.

```yaml
password_policy:
  standard:
    enabled: true
    min_length: 12
    max_length: 0
    require_uppercase: false
    require_lowercase: false
    require_number: false
    require_special: false
  zxcvbn:
    enabled: false
    min_score: 3
```

Standard policy: `min_length` defaults to 8 and `max_length` to 0 (no limit). Each `require_*` flag, all off by default, demands at least one uppercase, lowercase, number or special character.

zxcvbn policy: gives users strength feedback using Dropbox's zxcvbn. Unlike the standard policy it does not restrict what the user enters; it only informs them. `min_score` is 0 to 4:

- 0 too guessable (under 10^3 guesses)
- 1 very guessable (under 10^6)
- 2 somewhat guessable (under 10^8)
- 3 safely unguessable (under 10^10)
- 4 very unguessable (10^10 or more)

Score 0 is not allowed; setting `min_score: 0` falls back to the default of 3.

Pick standard rules when you need a hard floor. Pick zxcvbn when you only want guidance. Both are disabled by default (`enabled: false`), so the example above enables the standard policy explicitly.

Check: try to set a short password through the reset flow and confirm the portal rejects it with the standard policy enabled.

## Checked

2026-11-08. Read the full Authelia Password Policy page. Confirmed the standard and zxcvbn options, defaults (min_length 8, max_length 0, min_score 3, all disabled), the one-policy-at-a-time rule, the score table and the score 0 fallback. Removed an unsourced opinion about length versus composition.

Method: documentation only; no commands were run.
