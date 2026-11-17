---
id: computing-software.devops-ci-cd.verdaccio.two-factor-enrol-and-modes
name: two-factor-enrol-and-modes
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [two-factor, totp, otp, tfa-flag, enable-2fa, auth-and-writes, recovery-codes]
level: advanced
status: docs-checked
description: "Enable TOTP two-factor on Verdaccio 7 with the tfa flag, enrol with npm profile enable-2fa, understand auth-only versus auth-and-writes, and recovery codes."
sources:
  - https://verdaccio.org/docs/two-factor-authentication/
  - https://verdaccio.org/docs/setup-npm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Experimental, 7.x and later (not 6.x). To try it, the two-factor page says `npx --yes verdaccio@next-7` while the npm setup page says the 9.x line `verdaccio@next-9`. Needs a storage plugin that supports tokens (bundled local-storage and memory do; otherwise startup is refused), an authenticator app, and a server clock accurate within about a minute.

```yaml
flags:
  tfa: true
```
Restart. Each user then opts in:
```
npm profile enable-2fa auth-and-writes
npm profile get        # two-factor auth: auth-and-writes
npm profile disable-2fa
```
npm asks for the account password, shows a QR code, then the first code. Save the recovery codes: shown once, each single use; they work wherever an OTP is accepted. To get a fresh set, turn 2FA off and on.

Modes (auth-and-writes is the default):
| Operation | auth-only | auth-and-writes |
|---|---|---|
| login, token create | code | code |
| publish, unpublish, dist-tag | no | code |
| stage approve/reject | no | code |
| stage publish | never | never |

Scripts: `npm publish --otp=123456`; without a TTY or `--otp`, npm fails with EOTP. Yarn prompts by itself.

Verify: `npm profile get`; `pending: true` means enrolment was never confirmed and the account is not protected.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Two-factor authentication and Setup npm. Confirmed: the requirements, the tfa flag, enrolment commands and recovery codes, the mode table, scripting with --otp and EOTP, and pending: true. Removed or corrected: 7.x only corrected to 7.x and later; the pages disagree on the try-it line, noted in the skill.

Method: documentation only; no commands were run.
