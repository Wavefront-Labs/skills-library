---
id: computing-software.cybersecurity-defensive.keycloak.required-actions-for-users
name: required-actions-for-users
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, required-actions, update-password, verify-email, configure-otp]
level: practitioner
status: docs-checked
description: "Assign Keycloak required actions (update password, configure OTP, verify email, update profile), know which trigger automatically and which are helper-only."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/users/con-required-actions.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# required actions for users
Required actions are tasks a user must perform after providing credentials at first login; after that they are no longer required. Add them on the *Details* tab of the user.

Examples documented:
- **Update Password**: user must change the password.
- **Configure OTP**: user sets up a one-time password generator on a mobile device with Free OTP or Google Authenticator.
- **Verify Email**: Keycloak emails a validation link; once the user completes it they are allowed to log in.
- **Update Profile**: user must update profile information such as name, address, email and phone number.

Some required actions trigger automatically even if the administrator did not add them. Update password can fire when password policies force a change every X days. Verify profile can require a profile update while some user attributes do not meet the user profile configuration.

Some actions should not be added to a user directly. Update User Locale is a helper action for localisation parameters. Delete Credential is meant to be triggered as a Parameterized AIA (application initiated action), for example by the Account Console; an administrator who wants to delete a user's credential can do it directly in the Admin Console.

## Checked
2026-11-03. Confirmed against server_admin/topics/users/con-required-actions.adoc. Removed: the "Default Action under Authentication > Required actions" instruction, SMTP/disabled-action/brokered-user gotchas and the UPDATE_PASSWORD Verify step, none of which are on the page.
Method: documentation only; no commands were run.
