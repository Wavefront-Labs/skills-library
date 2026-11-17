---
id: computing-software.cybersecurity-defensive.authelia.totp-settings-and-compatibility
name: totp-settings-and-compatibility
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, totp, one-time-password, authenticator-app, skew, period, digits, algorithm]
level: practitioner
status: docs-checked
description: "Tune Authelia TOTP settings (issuer, algorithm, digits, period, skew, secret size), understand compatibility limits and the code reuse policy."
sources:
  - https://www.authelia.com/configuration/second-factor/time-based-one-time-password/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
totp:
  disable: false
  issuer: 'authelia.com'
  algorithm: 'sha1'
  digits: 6
  period: 30
  skew: 1
  secret_size: 32
  allowed_algorithms: ['SHA1']
  allowed_digits: [6]
  allowed_periods: [30]
  disable_reuse_security_policy: false
```

The defaults favour compatibility: many authenticator apps support only 6 digits and SHA1, and some accept a key but silently ignore the other parameters. Test that the app can both add the key and authenticate against Authelia before changing anything.

- `issuer` is the label apps display for the entry.
- `algorithm` is `sha1`, `sha256` or `sha512`; `digits` is `6` or `8`; `period` is in seconds, 30 recommended and 15 the minimum. Changing any of these affects only newly registered keys.
- `skew` is how many codes either side of the current one are valid. The default of 1 gives 3 valid codes, which is 90 seconds at a 30 second period. Changing skew affects all validations.
- `secret_size` is in bytes: minimum 20, default 32.
- `allowed_*` lists let users choose among options; each always contains the primary setting.
- `disable_reuse_security_policy` turns off the replay protection that blocks reusing a code within its validity window. Leave it off.

Check: register a key, log in once, then submit the same code again and confirm it is rejected.

## Checked

2026-11-08. Read the full Authelia Time-based One-Time Password page. Confirmed algorithm values, digits 6 or 8, period 30 recommended with minimum 15, skew default 1 and its effect, secret_size minimum 20 and default 32, the allowed_* lists, and disable_reuse_security_policy. No claims needed removal.

Method: documentation only; no commands were run.
