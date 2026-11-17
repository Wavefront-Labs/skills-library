---
id: computing-software.collaboration-platform-administration.nextcloud.password-policy-options
name: password-policy-options
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [password-policy, haveibeenpwned, password-history, lockout, complexity]
level: practitioner
status: draft
description: "Configure the Nextcloud password policy: minimum length, history, expiry, lockout, common password ban, character classes and breached-password checking."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_password_policy.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: set sensible password rules in one place.

The password policy app adds a section in the Security part of the administrator settings. The options are:
- minimal length, default 10 characters
- password history
- password expiration period
- lockout policy
- forbid common passwords such as `password` or `login`
- require upper and lower case characters
- require numeric characters
- require special characters such as `!` or `:`
- check against the list of breached passwords from haveibeenpwned.com, using a hashed check through its API

Choosing values: keep the settings in this one Security section so the whole policy is visible together. The policy comes from the password policy app, so it must be enabled for these options to appear.
- The breached-password check is a hashed lookup through the haveibeenpwned.com API, so the server contacts an external service. Confirm your network and privacy rules allow that.
- Test every rule you switch on with a throwaway account before announcing the policy, because users meet each rule at password change time.


Check: attempt to set a password of `password` and one that is too short, and confirm both are refused with a clear message.
