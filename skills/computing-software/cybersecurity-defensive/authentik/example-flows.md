---
id: computing-software.cybersecurity-defensive.authentik.example-flows
name: example-flows
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, example-flows, blueprints, enrollment, recovery, magic-link]
level: practitioner
status: docs-checked
description: "Import the bundled authentik example flow blueprints (enrollment, 2FA login, email magic link, conditional CAPTCHA, recovery, unenrollment) and know what they override."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/flow/flows/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: start from a bundled example flow instead of building one by hand.

Import: **Flows and Stages > Flows > Import**, choose **Local path** and enter the blueprint path, or download the file and use **File upload**. Re-importing restores the blueprint and discards your changes. The examples override the default flows, so review them and export existing flows first.

| Path | Result |
| --- | --- |
| `example/flows-enrollment-2-stage.yaml` | Sign-up prompting username, email, password, name; no verification; user logged in at once |
| `example/flows-enrollment-email-verification.yaml` | Same plus email verification; adjust the Email stage connection details |
| `example/flows-login-2fa.yaml` | Username/email, password, then OTP if configured; force 2FA by editing *Not configured action* on the Authenticator Validation stage |
| `example/flows-login-email-magic-link.yaml` | Passwordless link by email |
| `example/flows-login-conditional-captcha.yaml` | CAPTCHA shown based on IP and username reputation; uses CAPTCHA test keys by default |
| `example/flows-recovery-email-mfa-verification.yaml` | Recovery email, MFA check, new password, login |
| `example/flows-recovery-email-verification.yaml` | Recovery without MFA, not recommended |
| `example/flows-unenrollment.yaml` | User deletes own account, with no warning |

## Gotchas
- Magic link needs global email settings configured and valid user emails, and should be used only if inbox access is an acceptable factor. It uses the built-in account confirmation template; a custom email template can replace it.
- Conditional CAPTCHA: get a production key from Google reCAPTCHA.
- Recovery flows do not reject inactive users. The example recovery blueprints enable **Activate user on success** on the Email stage, so a valid link reactivates the user. Disable that if reactivation must be admin-only, and add a policy plus Deny stage after identification to block inactive users (this discloses account state).

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/add-secure-apps/flows-stages/flow/flows/ (read in full).
