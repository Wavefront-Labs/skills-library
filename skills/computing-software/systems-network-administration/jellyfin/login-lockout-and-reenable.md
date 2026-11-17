---
id: computing-software.systems-network-administration.jellyfin.login-lockout-and-reenable
name: login-lockout-and-reenable
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, lockout, failed-login-attempts, disable-user, password-reset, activity-feed]
level: practitioner
status: docs-checked
description: "Set Jellyfin's failed-login lockout threshold, recognise a locked user and re-enable the account from the Dashboard."
sources: ["https://jellyfin.org/docs/general/server/users/adding-managing-users/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Login lockout and re-enabling users

**Threshold.** On a user's profile, `Failed login attempts before user is locked out` sets how many bad attempts are allowed before the account is disabled. `0` inherits the defaults, 3 for non-admins and 5 for admins; `-1` disables lockout.

**What the user sees.** A locked-out user trying to sign in gets the generic message "Connection Failure ... We're unable to connect to the selected server right now".

**What the admin sees.** The lockout appears in the activity feed on the administrator dashboard. On the locked user's profile a banner reads "This user is currently disabled. See below to reenable".

**Unlock.** Unlocking is manual: open the user's profile, go to `Disable this user` in the Additional options section, untick it and press `Save`. The user can log in again.

**Password tab.** Admins can set or change passwords; users can change their own in personal settings. `Reset Password` lets the user log in without giving a password.

If the administrator account itself is locked and the UI route is unavailable, use the database procedure in `computing-software.systems-network-administration.jellyfin.unlock-locked-user-account`.

## Checked

2026-11-03. Confirmed against the Jellyfin Managing Users page: lockout threshold (0 inherits 3 for non-admin and 5 for admin, -1 disables), lockout messages, manual unlock via Disable this user, Password tab and Reset Password. Removed: unsupported advice and the invented check step.

Method: documentation only; no commands were run.
