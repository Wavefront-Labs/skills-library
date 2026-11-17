---
id: computing-software.it-support-helpdesk.apple-device-management.installomator
name: installomator
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, app-automation, installomator, app-install]
level: practitioner
status: docs-checked
description: "Install and update Mac apps from vendor downloads with the Installomator script, labels and Jamf policy parameters."
sources:
  - "https://github.com/Installomator/Installomator/wiki"
  - "https://github.com/Installomator/Installomator/wiki/Configuration-and-Variables"
  - "https://github.com/Installomator/Installomator/wiki/Using-Installomator"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# installomator

Goal: deploy and update apps from vendor downloads without repackaging.

## Run it
- The first argument is a label from `Labels.txt` (or `version` / `longversion`); variable overrides follow as
  `VARIABLE=value` in any order. It must run as root: `sudo ./Installomator.sh desktoppr DEBUG=0 NOTIFY=silent`.
- Jamf Pro: the script detects Jamf's first three policy arguments and ignores them; give the label as Parameter 4 and
  overrides in later parameters. The wiki also has pages for Mosyle, Addigy, Intune, Workspace ONE and Jamf School.
- A local install lives at `/usr/local/Installomator/Installomator.sh`.
- `DEBUG` defaults to 1 in the script (downloads next to the script, nothing installed); 2 downloads to a temp folder,
  checks blocking processes and the version but does not install; 0 does a full install or update. The installation
  package ships with `DEBUG=0`.

## Useful variables
- `BLOCKING_PROCESS_ACTION`: `ignore`, `silent_fail`, `prompt_user`, `prompt_user_then_kill`, `prompt_user_loop`,
  `tell_user` (default), `tell_user_then_kill`, `kill`. Set `PROMPT_TIMEOUT` (default 86400 seconds) with the prompt
  actions so an unanswered dialog does not hang the MDM process. `prompt_user_loop` can block other management actions.
- `NOTIFY`: `success` (default), `silent`, `all`. `NOTIFY_DIALOG=1` uses swiftDialog 2 or later when installed.
- `INSTALL=force` installs even if the version is the same; otherwise it installs only when newer or different.
- `LOGO` sets the dialog icon (`appstore` default, `jamf`, `microsoft`, `mosyleb`, and others) or a path to an icon.
- `IGNORE_APP_STORE_APPS=no` (default) leaves App Store and VPP installed apps alone.
- `LOGGING=DEBUG` logs everything; use it when overriding label variables or using the `valuesfromarguments` label
  (which needs `name`, `type`, `downloadURL` and `expectedTeamID`).
- `REOPEN=yes` (default) reopens an app that was closed for the update.

## Practice
Review labels before use, test with `DEBUG` 1 or 2 first, and wrap the call in a Jamf policy and Self Service item for
user-driven installs.

## Checked

2026-11-09: confirmed on the Installomator wiki pages Home, Configuration and Variables and Using Installomator (read as
raw markdown): arguments, Jamf parameters, DEBUG modes, variable names and defaults, `valuesfromarguments`. Removed: the
signing and Team ID verification claim wording beyond `expectedTeamID`, the advice to pin a copy rather than pull `main`
(opinion), the claim that stale labels fail silently, and the AutoPkg and Munki wiki sources.

Method: documentation only; no commands were run.

## Verify
The log shows the version installed; rerunning with the same version installs nothing unless `INSTALL=force` is set.
